"""Monte Carlo simulation engine.

Runs N iterations of the physics kernel with stochastic sampling of:
- Thermal diffusivity (biological variation)
- Smoker temperature fluctuations (equipment variation)
- Wind/humidity perturbations (weather variation)

Outputs P10/P50/P90 finish times and confidence level.
Uses NumPy broadcasting for performance — target < 5s for 5000 iterations.
"""

import numpy as np
from ..models.enums import ConfidenceTier, CookState, CutType, EquipmentType, WrapType
from ..models.dataclasses import (
    CookSession,
    PredictionResult,
    WeatherSnapshot,
)
from .physics import solve_1d_heat
from .biological_noise import sample_diffusivity, sample_smoker_temp_noise
from .stall_model import stall_probability

# Equipment temp variance defaults (°F std dev)
EQUIPMENT_TEMP_VARIANCE: dict[EquipmentType, float] = {
    EquipmentType.OFFSET: 15.0,
    EquipmentType.PELLET: 5.0,
    EquipmentType.KAMADO: 8.0,
    EquipmentType.WSM: 10.0,
    EquipmentType.CUSTOM: 12.0,
}


def run_monte_carlo(
    session: CookSession,
    n_iterations: int = 5000,
    seed: int | None = None,
) -> PredictionResult:
    """Run Monte Carlo simulation for a cook session.

    Args:
        session: Current cook session with all parameters.
        n_iterations: Number of MC iterations.
        seed: Random seed for reproducibility.

    Returns:
        PredictionResult with P10/P50/P90 finish times.
    """
    rng = np.random.default_rng(seed)

    # Determine current state from readings
    current_temp = 40.0  # default fridge temp
    elapsed = 0.0
    if session.readings:
        current_temp = session.readings[-1].temp_f
        elapsed = session.readings[-1].elapsed_minutes

    # Sample parameters
    diffusivities = sample_diffusivity(
        session.cut_type, n_samples=n_iterations, rng=rng
    )

    temp_variance = EQUIPMENT_TEMP_VARIANCE.get(session.equipment_type, 12.0)
    max_remaining = 1800 - int(elapsed)
    if max_remaining < 60:
        max_remaining = 60
    n_steps = int(max_remaining)

    smoker_noise = sample_smoker_temp_noise(
        n_steps=n_steps,
        temp_variance=temp_variance,
        n_samples=n_iterations,
        rng=rng,
    )

    # Weather perturbations
    wind_factors = np.ones(n_iterations)
    humidity_factors = np.ones(n_iterations)
    if session.weather:
        wind_base = max(0.5, 1.0 + (session.weather.wind_speed_mph - 5.0) * 0.02)
        wind_factors = rng.normal(wind_base, 0.1, size=n_iterations)
        wind_factors = np.clip(wind_factors, 0.3, 2.0)

        humid_base = max(0.5, 1.0 + (session.weather.humidity_pct - 50.0) * 0.005)
        humidity_factors = rng.normal(humid_base, 0.05, size=n_iterations)
        humidity_factors = np.clip(humidity_factors, 0.3, 2.0)

    # Wrap parameters
    wrap_temp = None
    if session.interventions:
        wrap_temp = session.interventions[-1].temp_at_wrap_f

    # Run iterations
    finish_times = np.full(n_iterations, np.inf)

    for i in range(n_iterations):
        _, finish_time = solve_1d_heat(
            cut_type=session.cut_type,
            thickness_inches=session.thickness_inches,
            smoker_temp_f=session.smoker_temp_f,
            initial_temp_f=current_temp,
            target_temp_f=session.target_temp_f,
            diffusivity_mm2s=float(diffusivities[i]),
            wrap_type=session.wrap_type,
            wrap_temp_f=wrap_temp,
            altitude_ft=session.altitude_ft,
            smoker_temp_noise=smoker_noise[i],
            wind_factor=float(wind_factors[i]),
            humidity_factor=float(humidity_factors[i]),
            dt_minutes=1.0,
            max_minutes=max_remaining,
        )
        finish_times[i] = finish_time + elapsed

    # Filter out infinite values (didn't finish in time)
    valid = finish_times[np.isfinite(finish_times)]
    if len(valid) < n_iterations * 0.5:
        # More than half didn't finish — very uncertain
        p10 = float(np.percentile(finish_times[np.isfinite(finish_times)], 10)) if len(valid) > 0 else max_remaining + elapsed
        p50 = float(np.percentile(finish_times[np.isfinite(finish_times)], 50)) if len(valid) > 0 else max_remaining + elapsed
        p90 = max_remaining + elapsed
        confidence = ConfidenceTier.VERY_LOW
    else:
        p10 = float(np.percentile(valid, 10))
        p50 = float(np.percentile(valid, 50))
        p90 = float(np.percentile(valid, 90))
        confidence = _compute_confidence(valid, session)

    # Compute stall probability from current temp
    stall_prob = stall_probability(current_temp)

    return PredictionResult(
        session_id=session.id,
        p10_minutes=round(p10, 1),
        p50_minutes=round(p50, 1),
        p90_minutes=round(p90, 1),
        confidence=confidence,
        current_state=session.current_state,
        stall_probability=round(stall_prob, 3),
        readings_count=len(session.readings),
    )


def _compute_confidence(
    valid_times: np.ndarray, session: CookSession
) -> ConfidenceTier:
    """Determine confidence tier based on spread and data."""
    spread = float(np.percentile(valid_times, 90) - np.percentile(valid_times, 10))
    n_readings = len(session.readings)

    if n_readings >= 10 and spread < 60:
        return ConfidenceTier.HIGH
    elif n_readings >= 5 and spread < 120:
        return ConfidenceTier.MODERATE
    elif n_readings >= 2 and spread < 240:
        return ConfidenceTier.LOW
    else:
        return ConfidenceTier.VERY_LOW
