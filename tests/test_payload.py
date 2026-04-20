import json

import pytest

from src.payload import ATUPayload, knots_to_kmh


class TestATUPayload:
    def test_valid_payload_from_fixture(self):
        with open("tests/fixtures/valid_payload.json") as f:
            data = json.load(f)
        payload = ATUPayload(**data)
        assert payload.imei == "435654321239569"
        assert payload.direction_id == 1

    def test_imei_too_short(self):
        with open("tests/fixtures/invalid_payload.json") as f:
            data = json.load(f)
        with pytest.raises(ValueError):
            ATUPayload(**data["invalid_imei_too_short"])

    def test_imei_too_long(self):
        with open("tests/fixtures/invalid_payload.json") as f:
            data = json.load(f)
        with pytest.raises(ValueError):
            ATUPayload(**data["invalid_imei_too_long"])

    def test_latitude_out_of_range_high(self):
        with open("tests/fixtures/invalid_payload.json") as f:
            data = json.load(f)
        with pytest.raises(ValueError):
            ATUPayload(**data["invalid_latitude_out_of_range"])

    def test_longitude_out_of_range_low(self):
        with open("tests/fixtures/invalid_payload.json") as f:
            data = json.load(f)
        with pytest.raises(ValueError):
            ATUPayload(**data["invalid_longitude_out_of_range"])

    def test_speed_too_high(self):
        with open("tests/fixtures/invalid_payload.json") as f:
            data = json.load(f)
        with pytest.raises(ValueError):
            ATUPayload(**data["invalid_speed_too_high"])

    def test_direction_id_invalid(self):
        with open("tests/fixtures/invalid_payload.json") as f:
            data = json.load(f)
        with pytest.raises(ValueError):
            ATUPayload(**data["invalid_direction_id"])

    def test_identifier_present_but_empty(self):
        with open("tests/fixtures/invalid_payload.json") as f:
            data = json.load(f)
        with pytest.raises(ValueError):
            ATUPayload(**data["invalid_identifier_empty"])


class TestHelpers:
    def test_knots_to_kmh(self):
        assert knots_to_kmh(10.0) == 18.52
        assert knots_to_kmh(77.5) == 143.53
        assert knots_to_kmh(0.0) == 0.0
        assert knots_to_kmh(100.0) == 185.2
