"""Weather service: async OpenWeather API client with local cache fallback."""

import httpx
from datetime import datetime, timedelta
from typing import Optional

from ..config import settings
from ..models.dataclasses import WeatherSnapshot


# Cache weather for 30 minutes
CACHE_TTL_MINUTES = 30

_weather_cache: dict[str, tuple[WeatherSnapshot, datetime]] = {}


async def fetch_weather(
    latitude: float, longitude: float
) -> Optional[WeatherSnapshot]:
    """Fetch current weather from OpenWeather API.

    Falls back to cached data if API call fails or key is not configured.

    Args:
        latitude: Location latitude.
        longitude: Location longitude.

    Returns:
        WeatherSnapshot or None if unavailable.
    """
    cache_key = f"{latitude:.2f},{longitude:.2f}"

    # Check cache first
    if cache_key in _weather_cache:
        snapshot, cached_at = _weather_cache[cache_key]
        if datetime.utcnow() - cached_at < timedelta(minutes=CACHE_TTL_MINUTES):
            return snapshot

    if not settings.openweather_api_key:
        # No API key — return cached or default
        if cache_key in _weather_cache:
            return _weather_cache[cache_key][0]
        return _default_weather()

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={
                    "lat": latitude,
                    "lon": longitude,
                    "appid": settings.openweather_api_key,
                    "units": "imperial",
                },
            )
            resp.raise_for_status()
            data = resp.json()

            snapshot = WeatherSnapshot(
                ambient_temp_f=data["main"]["temp"],
                wind_speed_mph=data["wind"]["speed"],
                humidity_pct=data["main"]["humidity"],
            )

            _weather_cache[cache_key] = (snapshot, datetime.utcnow())
            return snapshot

    except Exception:
        # Fallback to cache or default
        if cache_key in _weather_cache:
            return _weather_cache[cache_key][0]
        return _default_weather()


def _default_weather() -> WeatherSnapshot:
    """Return default weather assumptions when API is unavailable."""
    return WeatherSnapshot(
        ambient_temp_f=75.0,
        wind_speed_mph=5.0,
        humidity_pct=50.0,
    )
