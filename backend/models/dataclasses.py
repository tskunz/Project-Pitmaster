from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from .enums import (
    CookState,
    ConfidenceTier,
    CutType,
    EquipmentType,
    MeatCategory,
    QualityRating,
    WrapType,
)


@dataclass
class ThermalProperties:
    """Thermal diffusivity properties for a specific protein/cut."""
    base_diffusivity: float  # mm²/s
    cv: float = 0.08  # coefficient of variation (~8%)
    density: float = 1050.0  # kg/m³
    specific_heat: float = 3400.0  # J/(kg·K)


@dataclass
class EquipmentProfile:
    """Smoker equipment characteristics."""
    equipment_type: EquipmentType
    name: str
    temp_variance: float  # °F std dev of smoker temp fluctuations
    recovery_time_min: float  # minutes to recover after lid open
    temp_drop_on_lid_open: float  # °F drop when lid is opened
    insulation_factor: float = 1.0  # multiplier on heat loss


@dataclass
class WeatherSnapshot:
    """Current weather conditions relevant to BBQ."""
    ambient_temp_f: float
    wind_speed_mph: float
    humidity_pct: float
    altitude_ft: float = 0.0


@dataclass
class ProbeReading:
    """A single temperature reading from the meat probe."""
    id: Optional[int] = None
    session_id: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    temp_f: float = 0.0
    smoker_temp_f: Optional[float] = None
    elapsed_minutes: float = 0.0


@dataclass
class PredictionResult:
    """Output of a Monte Carlo simulation run."""
    id: Optional[int] = None
    session_id: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    p10_minutes: float = 0.0  # optimistic (10th percentile)
    p50_minutes: float = 0.0  # median
    p90_minutes: float = 0.0  # conservative (90th percentile)
    confidence: ConfidenceTier = ConfidenceTier.LOW
    current_state: CookState = CookState.SETUP
    stall_probability: float = 0.0
    readings_count: int = 0


@dataclass
class LidOpenEvent:
    """Records when the user opened the lid."""
    id: Optional[int] = None
    session_id: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    duration_seconds: float = 30.0  # assumed default


@dataclass
class InterventionEvent:
    """Records a wrap or other intervention."""
    id: Optional[int] = None
    session_id: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    wrap_type: WrapType = WrapType.NONE
    temp_at_wrap_f: float = 0.0
    elapsed_minutes: float = 0.0


@dataclass
class StallState:
    """Tracks stall detection status."""
    in_stall: bool = False
    stall_start_temp_f: Optional[float] = None
    stall_start_minutes: Optional[float] = None
    stall_duration_minutes: float = 0.0
    slope_history: list[float] = field(default_factory=list)


@dataclass
class CookSession:
    """The main domain object representing an active cook."""
    id: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    meat_category: MeatCategory = MeatCategory.BEEF
    cut_type: CutType = CutType.BRISKET
    weight_lbs: float = 10.0
    thickness_inches: float = 5.0
    equipment_type: EquipmentType = EquipmentType.OFFSET
    smoker_temp_f: float = 250.0
    target_temp_f: float = 203.0
    dinner_time: Optional[datetime] = None
    altitude_ft: float = 0.0
    wrap_type: WrapType = WrapType.NONE
    current_state: CookState = CookState.SETUP
    confidence: ConfidenceTier = ConfidenceTier.LOW
    readings: list[ProbeReading] = field(default_factory=list)
    predictions: list[PredictionResult] = field(default_factory=list)
    lid_events: list[LidOpenEvent] = field(default_factory=list)
    interventions: list[InterventionEvent] = field(default_factory=list)
    stall: StallState = field(default_factory=StallState)
    weather: Optional[WeatherSnapshot] = None
    is_finished: bool = False


@dataclass
class BackwardPlan:
    """Result of backward planning from dinner time."""
    dinner_time: datetime = field(default_factory=datetime.utcnow)
    estimated_cook_minutes_p90: float = 0.0
    rest_minutes: float = 30.0
    fire_start_time: datetime = field(default_factory=datetime.utcnow)
    meat_on_time: datetime = field(default_factory=datetime.utcnow)
    preheat_minutes: float = 30.0


@dataclass
class PostCookReport:
    """Summary generated after a cook is finished."""
    session_id: str = ""
    total_cook_minutes: float = 0.0
    final_temp_f: float = 0.0
    stall_occurred: bool = False
    stall_duration_minutes: float = 0.0
    was_wrapped: bool = False
    wrap_type: WrapType = WrapType.NONE
    prediction_accuracy_minutes: float = 0.0  # P50 vs actual delta
    readings_count: int = 0
    lid_opens_count: int = 0
    quality_rating: Optional[QualityRating] = None
    quality_notes: str = ""
    predicted_temps: list[float] = field(default_factory=list)
    actual_temps: list[float] = field(default_factory=list)
    residuals: list[float] = field(default_factory=list)


@dataclass
class HoldPhaseResult:
    """Result of rest/hold phase calculation."""
    carryover_peak_f: float = 0.0
    time_to_serving_temp_minutes: float = 0.0
    recommended_rest_minutes: float = 30.0
