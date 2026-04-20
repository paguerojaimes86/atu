import pytest
from unittest.mock import AsyncMock, MagicMock

from src.atuc import ATUClient
from src.payload import ATUPayload


class TestATUClient:
    @pytest.mark.asyncio
    async def test_send_payload(self):
        mock_logger = MagicMock()
        client = ATUClient("ws://devrecepcion.atu.gob.pe:5000/ws", "test-token", mock_logger)
        client._conn = AsyncMock()
        client._conn.send = AsyncMock()
        client._conn.recv = AsyncMock(return_value='{"codigo":"00","identifier":"test","timestamp":"2026-04-20 18:00:00"}')

        payload = ATUPayload(
            imei="435654321239569",
            latitude=-12.228012,
            longitude=-76.931337,
            route_id="1180",
            ts=1757119795000,
            license_plate="ABC123",
            speed=77.5,
            direction_id=1,
            driver_id="12345678",
            tsinitialtrip=1757097480000,
        )

        response = await client.send(payload)
        assert response.codigo == "00"
