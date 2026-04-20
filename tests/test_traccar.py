import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.traccar import TraccarClient
from src.payload import knots_to_kmh


class TestTraccarClient:
    @pytest.mark.asyncio
    async def test_authenticate_sets_jsessionid(self):
        mock_logger = MagicMock()
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value={"id": 2, "name": "Test User"})
        mock_response.headers = {"Set-Cookie": "JSESSIONID=test123; Path=/"}

        mock_session_instance = MagicMock()
        mock_session_instance.post = AsyncMock(return_value=mock_response)
        mock_session_instance.cookie_jar = MagicMock()

        mock_session_class = MagicMock(return_value=mock_session_instance)

        with patch("aiohttp.ClientSession", mock_session_class):
            client = TraccarClient("https://traccar.example.com", "user@test.com", "password", mock_logger)
            await client.authenticate()
            assert client._jsessionid == "test123"

    @pytest.mark.asyncio
    async def test_get_positions(self):
        mock_logger = MagicMock()
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value=[
            {"id": 1, "latitude": -12.22, "longitude": -76.93, "speed": 10.0, "fixTime": 1757119795000, "serverTime": 1757097480000}
        ])
        mock_response.raise_for_status = AsyncMock()

        mock_session_instance = MagicMock()
        mock_session_instance.get = MagicMock(return_value=MagicMock(
            __aenter__=AsyncMock(return_value=mock_response),
            __aexit__=AsyncMock()
        ))

        client = TraccarClient("https://traccar.example.com", "user@test.com", "password", mock_logger)
        client._session = mock_session_instance
        positions = await client.get_positions()
        assert len(positions) == 1
        assert positions[0]["latitude"] == -12.22


class TestTraccarHelpers:
    def test_knots_to_kmh(self):
        assert knots_to_kmh(10.0) == 18.52
        assert knots_to_kmh(77.5) == 143.53
        assert knots_to_kmh(0.0) == 0.0
        assert knots_to_kmh(100.0) == 185.2
