import pytest

from src.config import Settings


class TestConfig:
    def test_default_values(self):
        s = Settings()
        assert s.atu_endpoint_test == "ws://devrecepcion.atu.gob.pe:5000/ws"
        assert s.atu_interval_seconds == 20
        assert s.retransmission_interval_seconds == 60
        assert s.log_level == "INFO"

    def test_env_override(self, monkeypatch):
        monkeypatch.setenv("ATU_TOKEN", "test-token-123")
        monkeypatch.setenv("ATU_INTERVAL_SECONDS", "10")
        s = Settings()
        assert s.atu_token == "test-token-123"
        assert s.atu_interval_seconds == 10
