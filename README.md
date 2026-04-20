# ATU GPS WebSocket Integration

Python async service bridging GPS telemetry from Traccar to ATU SICM via WebSocket.

## Stack

- Python 3.11+, `asyncio`
- `websockets` — ATU WebSocket client
- `aiohttp` — Traccar REST polling
- `pydantic` v2 — payload validation
- `structlog` — structured logging

## Estructura

```
atu/
├── src/
│   ├── __init__.py
│   ├── config.py      # Configuración desde env vars
│   ├── logger.py      # structlog setup
│   ├── payload.py     # ATUPayload model + validators
│   ├── atuc.py        # ATU WebSocket client
│   ├── traccar.py     # Traccar REST client
│   ├── retransmit.py  # Retransmission JSONL queue
│   └── main.py        # Service entry point
├── tests/
│   ├── fixtures/
│   └── test_*.py
├── pyproject.toml
├── .env.example
└── README.md
```

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Configuración

Copiar `.env.example` a `.env` y completar:

```bash
ATU_ENDPOINT_TEST=ws://devrecepcion.atu.gob.pe:5000/ws
ATU_TOKEN=<token-de-pruebas>
ATU_INTERVAL_SECONDS=20
TRACCAR_BASE_URL=https://tu-traccar.com
TRACCAR_EMAIL=<user>
TRACCAR_PASSWORD=<pass>
LOG_LEVEL=INFO
```

## Ejecución

```bash
python -m src.main
```

## Tests

```bash
pytest tests/
```

## Endpoints

| Env | Endpoint |
|-----|----------|
| Test | `ws://devrecepcion.atu.gob.pe:5000/ws?token=TOKEN` |
| Prod | TBD por ATU |

## Logs

Logs structurados JSON a stdout. Campos clave:

- `atu_client_connected` / `atu_client_disconnected`
- `atu_payload_sent` — imei, route_id, direction_id
- `atu_response_received` — code, identifier, timestamp
- `retransmit_queue_write` — ts de la posición

## Payload ATU

11 campos obligatorios según manual SICM. IMEI se serializa como string (15 dígitos).

## Flags de validación

| Campo | Validación |
|-------|------------|
| imei | string, 15 dígitos exactos |
| latitude | -90 a 90 |
| longitude | -180 a 180 |
| speed | 0 a 999.99 km/h |
| direction_id | 0 (ida) o 1 (vuelta) |

## Retransmisión

Datos con `ts` mayor a 10 minutos se encolan en `retransmit.jsonl`. Endpoint de retransmisión pendiente de definición por ATU.
