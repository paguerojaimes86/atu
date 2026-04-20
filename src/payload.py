from typing import Annotated, Literal

from pydantic import AfterValidator, BaseModel, Field, StringConstraints


def _check_nonempty_if_present(v: str | None) -> str | None:
    if v is not None and v == "":
        raise ValueError("identifier, if present, must not be empty")
    return v


class ATUPayload(BaseModel):
    imei: Annotated[str, StringConstraints(min_length=15, max_length=15, pattern=r"^\d{15}$")]
    latitude: Annotated[float, Field(gt=-90.0, lt=90.0)]
    longitude: Annotated[float, Field(gt=-180.0, lt=180.0)]
    route_id: Annotated[str, StringConstraints(max_length=10)]
    ts: Annotated[int, Field(gt=0)]
    license_plate: Annotated[str, StringConstraints(max_length=7)]
    speed: Annotated[float, Field(ge=0.0, le=999.99)]
    direction_id: Literal[0, 1]
    driver_id: Annotated[str, StringConstraints(max_length=20)]
    tsinitialtrip: Annotated[int, Field(gt=0)]
    identifier: Annotated[str | None, AfterValidator(_check_nonempty_if_present)] = None


class ATUResponse(BaseModel):
    codigo: str
    descrip: str | None = None
    identifier: str | None = None
    timestamp: str | None = None


def knots_to_kmh(knots: float) -> float:
    return round(knots * 1.852, 2)
