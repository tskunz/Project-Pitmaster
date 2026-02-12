from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from .enums import (
    ConfidenceTier,
    CookState,
    CutType,
    EquipmentType,
    MeatCategory,
    QualityRating,
    WrapType,
)


# --- Request models ---

class CookSetupRequest(BaseModel):
    meat_category: MeatCategory
    cut_type: CutType
    weight_lbs: float = Field(gt=0, le=30)
    thickness_inches: float = Field(gt=0, le=12)
    equipment_type: EquipmentType = EquipmentType.OFFSET
    smoker_temp_f: float = Field(default=250.0, ge=180, le=400)
    target_temp_f: float = Field(default=203.0, ge=140, le=212)
    dinner_time: Optional[datetime] = None
    altitude_ft: float = Field(default=0.0, ge=0, le=15000)
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class ProbeReadingRequest(BaseModel):
    temp_f: float = Field(ge=32, le=212)
    smoker_temp_f: Optional[float] = Field(default=None, ge=100, le=500)


class WrapRequest(BaseModel):
    wrap_type: WrapType


class LidOpenRequest(BaseModel):
    duration_seconds: float = Field(default=30.0, ge=1, le=600)


class FinishCookRequest(BaseModel):
    quality_rating: Optional[QualityRating] = None
    quality_notes: str = ""


# --- Response models ---

class PredictionResponse(BaseModel):
    p10_minutes: float
    p50_minutes: float
    p90_minutes: float
    p10_time: Optional[datetime] = None
    p50_time: Optional[datetime] = None
    p90_time: Optional[datetime] = None
    confidence: ConfidenceTier
    current_state: CookState
    stall_probability: float
    readings_count: int


class StateResponse(BaseModel):
    current_state: CookState
    confidence: ConfidenceTier
    stall_active: bool
    stall_duration_minutes: float
    wrap_type: WrapType
    readings_count: int
    elapsed_minutes: float


class CookSetupResponse(BaseModel):
    session_id: str
    prediction: PredictionResponse
    backward_plan: Optional["BackwardPlanResponse"] = None


class BackwardPlanResponse(BaseModel):
    dinner_time: datetime
    fire_start_time: datetime
    meat_on_time: datetime
    estimated_cook_minutes_p90: float
    rest_minutes: float
    preheat_minutes: float


class ReadingResponse(BaseModel):
    elapsed_minutes: float
    prediction: PredictionResponse
    state: StateResponse


class WrapResponse(BaseModel):
    wrap_type: WrapType
    prediction: PredictionResponse
    message: str


class ReportResponse(BaseModel):
    session_id: str
    total_cook_minutes: float
    final_temp_f: float
    stall_occurred: bool
    stall_duration_minutes: float
    was_wrapped: bool
    wrap_type: WrapType
    prediction_accuracy_minutes: float
    readings_count: int
    lid_opens_count: int
    quality_rating: Optional[QualityRating] = None
    quality_notes: str
    predicted_temps: list[float]
    actual_temps: list[float]
    residuals: list[float]


class EquipmentPresetResponse(BaseModel):
    equipment_type: EquipmentType
    name: str
    temp_variance: float
    recovery_time_min: float
    temp_drop_on_lid_open: float
    insulation_factor: float


class WeatherResponse(BaseModel):
    ambient_temp_f: float
    wind_speed_mph: float
    humidity_pct: float


class HealthResponse(BaseModel):
    status: str = "ok"
    version: str = "1.0.0"
