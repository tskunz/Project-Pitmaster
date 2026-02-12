"""1D heat diffusion solver using finite differences (Fourier's Law).

The meat is modeled as a 1D slab of thickness L. We discretize into N spatial
nodes and march forward in time using an explicit finite-difference scheme
with convective (Robin) boundary conditions.

Evaporative cooling from the stall is applied per-timestep inside the solver
so the stall model is *coupled*, not post-hoc.
"""

import numpy as np
from ..models.enums import CutType, WrapType
from .altitude import boiling_point_at_altitude

# Thermal diffusivity lookup table (mm²/s) per cut type.
# Values calibrated so a 5" brisket at 250°F takes ~10-14 hours.
THERMAL_DIFFUSIVITY: dict[CutType, float] = {
    CutType.BRISKET: 0.130,
    CutType.PORK_BUTT: 0.125,
    CutType.PORK_RIBS: 0.140,
    CutType.BEEF_RIBS: 0.135,
    CutType.CHICKEN_WHOLE: 0.145,
    CutType.TURKEY_BREAST: 0.140,
    CutType.LEG_OF_LAMB: 0.132,
}

# Evaporative cooling magnitude at stall peak (°F/min effective cooling rate).
# This represents the heat extracted by surface moisture evaporation during the stall.
# Higher values = longer stall plateau.
BASE_EVAP_RATE = 1.0

# Wrap type reduction of evaporative cooling.
WRAP_EVAP_REDUCTION: dict[WrapType, float] = {
    WrapType.NONE: 0.0,
    WrapType.FOIL: 0.95,
    WrapType.BUTCHER_PAPER: 0.60,
    WrapType.FOIL_BOAT: 0.45,
}

# Spatial discretization
N_NODES = 50

# Biot number: ratio of surface convection to internal conduction.
# Small Biot (~0.1-0.5) means the surface heats slowly relative to
# internal conduction, which is realistic for BBQ (hot air → meat surface).
BIOT_NUMBER = 0.3


def solve_1d_heat(
    cut_type: CutType,
    thickness_inches: float,
    smoker_temp_f: float,
    initial_temp_f: float,
    target_temp_f: float,
    diffusivity_mm2s: float | None = None,
    wrap_type: WrapType = WrapType.NONE,
    wrap_temp_f: float | None = None,
    altitude_ft: float = 0.0,
    smoker_temp_noise: np.ndarray | None = None,
    wind_factor: float = 1.0,
    humidity_factor: float = 1.0,
    dt_minutes: float = 1.0,
    max_minutes: int = 1800,
) -> tuple[np.ndarray, float]:
    """Solve 1D heat equation to predict cook time.

    Uses explicit finite differences with convective (Robin) BCs:
      Surface: T[0]_new = T[0] + Fo*(T[1]-T[0]) + Fo*Bi*(T_smoker-T[0])
      Interior: T[i]_new = T[i] + Fo*(T[i-1] - 2*T[i] + T[i+1])
    where Fo = alpha*dt/dx² is the Fourier number.

    Stability requires Fo*(1+Bi) <= 0.5.
    """
    # Convert units
    L = thickness_inches * 25.4  # mm (half-thickness: we model full slab, heat from both sides)
    dx = L / N_NODES  # mm
    dt_s = dt_minutes * 60.0  # seconds

    alpha = diffusivity_mm2s if diffusivity_mm2s else THERMAL_DIFFUSIVITY.get(
        cut_type, 0.130
    )

    Bi = BIOT_NUMBER * wind_factor

    # Compute Fourier number and enforce stability
    Fo = alpha * dt_s / (dx ** 2)
    max_Fo = 0.45 / (1.0 + Bi)  # stability limit
    if Fo > max_Fo:
        # Subdivide time steps to maintain stability
        dt_s = max_Fo * dx ** 2 / alpha
        Fo = max_Fo

    dt_min_actual = dt_s / 60.0
    n_steps = int(max_minutes / dt_min_actual) + 1
    bp = boiling_point_at_altitude(altitude_ft)

    # Initialize temperature field — uniform at initial temp
    T = np.full(N_NODES + 1, initial_temp_f, dtype=np.float64)
    center_idx = N_NODES // 2

    # We'll record center temp at 1-minute intervals for output
    output_interval = max(1, int(1.0 / dt_min_actual))
    n_output = int(max_minutes) + 1
    temp_history = np.zeros(n_output, dtype=np.float64)
    output_idx = 0

    # Evaporative cooling parameters
    stall_low = 140.0
    stall_high = min(185.0, bp)
    evap_base = BASE_EVAP_RATE * humidity_factor
    wrap_reduction = WRAP_EVAP_REDUCTION.get(wrap_type, 0.0)

    finish_time = np.inf

    for step in range(n_steps):
        current_time_min = step * dt_min_actual

        # Effective smoker temperature with noise
        smoker_eff = smoker_temp_f
        if smoker_temp_noise is not None:
            noise_idx = int(current_time_min)  # index by minute
            if noise_idx < len(smoker_temp_noise):
                smoker_eff += smoker_temp_noise[noise_idx]

        # --- Explicit finite difference update ---
        T_new = T.copy()

        # Interior nodes (vectorized)
        T_new[1:N_NODES] = (
            T[1:N_NODES]
            + Fo * (T[0:N_NODES-1] - 2.0 * T[1:N_NODES] + T[2:N_NODES+1])
        )

        # Convective boundary conditions (Robin BC)
        # Left surface (x=0): exposed to smoker
        T_new[0] = T[0] + Fo * (T[1] - T[0]) + Fo * Bi * (smoker_eff - T[0])
        # Right surface (x=L): also exposed to smoker
        T_new[N_NODES] = T[N_NODES] + Fo * (T[N_NODES-1] - T[N_NODES]) + Fo * Bi * (smoker_eff - T[N_NODES])

        # --- Evaporative cooling in stall zone ---
        surface_temp = (T_new[0] + T_new[N_NODES]) / 2.0
        if stall_low <= surface_temp <= stall_high:
            # Determine wrap state
            is_wrapped = wrap_type != WrapType.NONE
            if wrap_temp_f is not None:
                is_wrapped = is_wrapped and surface_temp >= wrap_temp_f

            reduction = wrap_reduction if is_wrapped else 0.0
            effective_evap = evap_base * (1.0 - reduction)

            # Logistic ramp: peaks at midpoint of stall zone
            midpoint = (stall_low + stall_high) / 2.0
            spread = (stall_high - stall_low) / 6.0
            logistic = 1.0 / (1.0 + np.exp(-(surface_temp - midpoint) / spread))
            evap_cooling = effective_evap * logistic * dt_min_actual

            # Scale evap by the driving temperature difference:
            # More heat from smoker → more surface evaporation, but capped
            # so there's always net positive heat flow
            driving_delta = max(smoker_eff - surface_temp, 0.0)
            evap_scaling = min(driving_delta / 100.0, 1.0)  # ramp: full effect at 100°F delta
            evap_cooling *= evap_scaling

            # Apply mostly to surface nodes, diminishing toward center
            for i in range(N_NODES + 1):
                dist_from_surface = min(i, N_NODES - i) / (N_NODES / 2)
                surface_weight = 1.0 - 0.7 * dist_from_surface  # 100% at surface, 30% at center
                T_new[i] -= evap_cooling * surface_weight

        T = T_new

        # Cap at boiling point
        np.minimum(T, bp, out=T)

        center_temp = T[center_idx]

        # Record at output intervals
        if step % output_interval == 0 and output_idx < n_output:
            temp_history[output_idx] = center_temp
            output_idx += 1

        # Check finish condition
        if center_temp >= target_temp_f and finish_time == np.inf:
            finish_time = current_time_min

    return temp_history[:output_idx], finish_time
