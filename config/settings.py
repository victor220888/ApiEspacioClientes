# config/settings.py

from pydantic import Field # type: ignore
from pydantic_settings import BaseSettings, SettingsConfigDict # type: ignore

class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_host: str
    db_service: str

    # Mapeo de tu .env: las vars ORACLE_POOL_* ahora se asocian por alias
    oracle_min:                  int = Field(2, alias="ORACLE_POOL_MIN")
    oracle_max:                  int = Field(10, alias="ORACLE_POOL_MAX")
    oracle_increment:            int = Field(1, alias="ORACLE_POOL_INC")
    
    secret_key:                  str = Field(..., alias="SECRET_KEY")
    algorithm:                   str = Field("HS256", alias="ALGORITHM")
    access_token_expire_minutes: int = Field(30, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    #allowed_origins:            list[str] = Field([], alias="ALLOWED_ORIGINS")    
    allowed_origins:             list[str] = Field(["http://localhost:8000"], alias="ALLOWED_ORIGINS")
    # Definir el entorno (esto lo puedes modificar para adaptarlo a producción o pruebas)
    environment: str = "development"  # "development" o "production"
    #environment:                 str       = Field("development", alias="ENVIRONMENT")

    # Carga el .env y descarta cualquier ENV adicional
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

# Instancia única para toda la app
settings = Settings()
