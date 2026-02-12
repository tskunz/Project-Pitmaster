"""Trust system: 4-tier confidence evaluator with anomaly detection.

Confidence tiers:
- HIGH: 10+ consistent readings, narrow MC spread (<60 min)
- MODERATE: 5+ readings, moderate spread (<120 min)
- LOW: 2+ readings, wide spread (<240 min)
- VERY_LOW: few readings, anomalies detected, or very wide spread

Anomaly rules:
- Temperature decreased by >5°F between consecutive readings
- Temperature jumped by >20°F between consecutive readings
- Smoker temp is >50°F away from set point

Freeze condition: if anomaly detected, hold confidence at VERY_LOW
until 3 consecutive normal readings.
"""

from ..models.enums import ConfidenceTier
from ..models.dataclasses import CookSession, PredictionResult, ProbeReading


class TrustEvaluator:
    """Evaluates and manages confidence in predictions."""

    def __init__(self):
        self.anomaly_count: int = 0
        self.consecutive_normal: int = 0
        self.frozen: bool = False

    def evaluate(
        self, session: CookSession, prediction: PredictionResult
    ) -> ConfidenceTier:
        """Evaluate confidence tier based on current session state.

        Args:
            session: Current cook session.
            prediction: Latest MC prediction result.

        Returns:
            Updated confidence tier.
        """
        # Check for anomalies first
        if self._check_anomalies(session):
            self.anomaly_count += 1
            self.consecutive_normal = 0
            self.frozen = True
            return ConfidenceTier.VERY_LOW

        self.consecutive_normal += 1
        if self.frozen and self.consecutive_normal >= 3:
            self.frozen = False

        if self.frozen:
            return ConfidenceTier.VERY_LOW

        # Use prediction's computed confidence as baseline
        return prediction.confidence

    def _check_anomalies(self, session: CookSession) -> bool:
        """Check for anomalous readings."""
        readings = session.readings
        if len(readings) < 2:
            return False

        last = readings[-1]
        prev = readings[-2]
        delta = last.temp_f - prev.temp_f

        # Temperature dropped significantly
        if delta < -5.0:
            return True

        # Temperature jumped unrealistically
        if delta > 20.0:
            return True

        # Smoker temp way off set point
        if last.smoker_temp_f is not None:
            smoker_delta = abs(last.smoker_temp_f - session.smoker_temp_f)
            if smoker_delta > 50.0:
                return True

        return False

    def reset(self) -> None:
        """Reset trust state."""
        self.anomaly_count = 0
        self.consecutive_normal = 0
        self.frozen = False
