"""Weather API endpoint — proxies OpenWeather to keep key server-side."""

from fastapi import APIRouter, Query

from ..models.schemas import WeatherResponse
from ..services.weather_service import fetch_weather

router = APIRouter(prefix="/api/v1/weather", tags=["weather"])


@router.get("", response_model=WeatherResponse)
async def get_weather(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
):
    """Fetch current weather conditions."""
    snapshot = await fetch_weather(lat, lon)
    return WeatherResponse(
        ambient_temp_f=snapshot.ambient_temp_f,
        wind_speed_mph=snapshot.wind_speed_mph,
        humidity_pct=snapshot.humidity_pct,
    )
