import re
from typing import Any

import aiohttp


class TraccarClient:
    def __init__(self, base_url: str, email: str, password: str, logger: Any):
        self.base_url = base_url.rstrip("/")
        self.email = email
        self.password = password
        self.logger = logger
        self._session: aiohttp.ClientSession | None = None
        self._jsessionid: str | None = None

    async def authenticate(self) -> None:
        self._session = aiohttp.ClientSession()
        resp = await self._session.post(
            f"{self.base_url}/api/session",
            data={"email": self.email, "password": self.password},
        )
        resp.raise_for_status()
        await resp.json()

        for k, v in resp.headers.items():
            if k.lower() == "set-cookie":
                m = re.match(r"(JSESSIONID=[^;]+)", v)
                if m:
                    cookie_val = m.group(1)
                    name, val = cookie_val.split("=", 1)
                    self._session.cookie_jar.update_cookies({name: val})
                    self._jsessionid = val

        self.logger.info("traccar_authenticated")

    async def get_devices(self) -> list[dict[str, Any]]:
        if self._session is None:
            raise ConnectionError("Not authenticated to Traccar")

        async with self._session.get(f"{self.base_url}/api/devices") as resp:
            resp.raise_for_status()
            devices = await resp.json()
            self.logger.info("traccar_devices_fetched", count=len(devices))
            return devices

    async def get_positions(self) -> list[dict[str, Any]]:
        if self._session is None:
            raise ConnectionError("Not authenticated to Traccar")

        async with self._session.get(f"{self.base_url}/api/positions") as resp:
            resp.raise_for_status()
            positions = await resp.json()
            self.logger.info("traccar_positions_fetched", count=len(positions))
            return positions

    async def close(self) -> None:
        if self._session:
            await self._session.close()
            self._session = None
