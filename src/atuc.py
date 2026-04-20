import asyncio
import json
from typing import Any

import websockets


from .payload import ATUPayload, ATUResponse


class ATUClient:
    def __init__(self, uri: str, token: str, logger: Any):
        self.uri = uri
        self.token = token
        self.logger = logger
        self._conn: Any = None
        self._backoff = 1.0
        self._max_backoff = 60.0
        self._ping_interval = 30.0

    async def connect(self) -> None:
        full_uri = f"{self.uri}?token={self.token}"
        self._conn = await websockets.connect(full_uri, ping_interval=self._ping_interval)
        self._backoff = 1.0
        self.logger.info("atu_client_connected", uri=self.uri)

    async def send(self, payload: ATUPayload) -> ATUResponse:
        if self._conn is None:
            raise ConnectionError("Not connected to ATU")

        data = payload.model_dump_json()
        await self._conn.send(data)
        self.logger.info(
            "atu_payload_sent",
            imei=payload.imei,
            route_id=payload.route_id,
            direction_id=payload.direction_id,
        )

        raw = await self._conn.recv()
        resp_data = json.loads(raw)
        response = ATUResponse(**resp_data)

        self.logger.info(
            "atu_response_received",
            codigo=response.codigo,
            identifier=response.identifier,
            timestamp=response.timestamp,
        )
        return response

    async def close(self) -> None:
        if self._conn:
            await self._conn.close()
            self._conn = None
            self.logger.info("atu_client_disconnected")

    async def reconnect_with_backoff(self) -> None:
        self.logger.warning("atu_reconnecting", backoff_seconds=self._backoff)
        await asyncio.sleep(self._backoff)
        try:
            await self.connect()
        except Exception as exc:
            self.logger.error("atu_reconnect_failed", error=str(exc))
            self._backoff = min(self._backoff * 2, self._max_backoff)
            await self.reconnect_with_backoff()
