from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openweather_api_key: str = ""
    database_path: str = "pitmaster.db"
    mc_iterations: int = 5000
    default_altitude_ft: float = 0.0
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    model_config = {"env_file": ".env", "env_prefix": "PITMASTER_"}


settings = Settings()
