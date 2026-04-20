import json
from pathlib import Path
from typing import Any


class RetransmitQueue:
    def __init__(self, path: str, logger: Any):
        self.path = Path(path)
        self.logger = logger

    def write(self, payload: dict[str, Any]) -> None:
        with self.path.open("a") as f:
            f.write(json.dumps(payload) + "\n")
        ts_age_ms = payload.get("ts", 0)
        self.logger.info(
            "retransmit_queue_write",
            ts=ts_age_ms,
        )

    def read_pending(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        entries = []
        with self.path.open("r") as f:
            for line in f:
                line = line.strip()
                if line:
                    entries.append(json.loads(line))
        return entries

    def clear(self) -> None:
        if self.path.exists():
            self.path.unlink()
        self.logger.info("retransmit_queue_cleared")
