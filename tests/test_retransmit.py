import json
import tempfile
from unittest.mock import MagicMock

import pytest

from src.retransmit import RetransmitQueue


class TestRetransmitQueue:
    def test_write_and_read(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
            path = f.name

        mock_logger = MagicMock()
        q = RetransmitQueue(path, logger=mock_logger)
        entry = {"imei": "435654321239569", "ts": 1757119795000}
        q.write(entry)

        pending = q.read_pending()
        assert len(pending) == 1
        assert pending[0]["imei"] == "435654321239569"

        q.clear()

    def test_read_empty_nonexistent(self):
        mock_logger = MagicMock()
        q = RetransmitQueue("/nonexistent/path.jsonl", logger=mock_logger)
        assert q.read_pending() == []
