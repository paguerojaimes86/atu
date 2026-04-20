from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    atu_endpoint_test: str = "ws://devrecepcion.atu.gob.pe:5000/ws"
    atu_endpoint_prod: str = ""
    atu_token: str = ""
    atu_interval_seconds: int = 20

    traccar_base_url: str = ""
    traccar_email: str = ""
    traccar_password: str = ""

    retransmission_endpoint: str = ""
    retransmission_interval_seconds: int = 60

    log_level: str = "INFO"


def get_settings() -> Settings:
    return Settings()
