"""Stochastic variability in meat thermal properties.

Accounts for biological variation between individual cuts of meat.
Each MC iteration samples a different diffusivity from a log-normal
distribution with ~8% coefficient of variation.
"""

import numpy as np

from ..models.enums import CutType
from .physics import THERMAL_DIFFUSIVITY


def sample_diffusivity(
    cut_type: CutType,
    n_samples: int = 1,
    cv: float = 0.08,
    rng: np.random.Generator | None = None,
) -> np.ndarray:
    """Sample thermal diffusivity values from a log-normal distribution.

    Args:
        cut_type: Type of cut to get base diffusivity for.
        n_samples: Number of samples to draw.
        cv: Coefficient of variation (default 8%).
        rng: NumPy random generator for reproducibility.

    Returns:
        Array of diffusivity values (mm²/s).
    """
    if rng is None:
        rng = np.random.default_rng()

    base = THERMAL_DIFFUSIVITY.get(cut_type, 0.130)
    sigma = base * cv

    # Log-normal parameters from desired mean and std
    mu_ln = np.log(base**2 / np.sqrt(sigma**2 + base**2))
    sigma_ln = np.sqrt(np.log(1 + (sigma / base) ** 2))

    return rng.lognormal(mu_ln, sigma_ln, size=n_samples)


def sample_smoker_temp_noise(
    n_steps: int,
    temp_variance: float = 10.0,
    n_samples: int = 1,
    rng: np.random.Generator | None = None,
) -> np.ndarray:
    """Generate per-timestep smoker temperature noise.

    Models the natural fluctuations of a smoker around its set point.

    Args:
        n_steps: Number of time steps.
        temp_variance: Standard deviation of temperature fluctuations (°F).
        n_samples: Number of MC iterations.
        rng: NumPy random generator.

    Returns:
        Array of shape (n_samples, n_steps) with temperature offsets.
    """
    if rng is None:
        rng = np.random.default_rng()

    return rng.normal(0.0, temp_variance, size=(n_samples, n_steps))
