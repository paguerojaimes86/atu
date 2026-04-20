# Tests — ATU GPS WebSocket Integration

## Estructura

```
tests/
├── __init__.py
├── conftest.py              # Fixtures compartidas
├── test_payload.py          # Validación de payloads ATU
├── test_config.py           # Configuración desde env vars
├── test_atuc.py             # Cliente ATU WebSocket (mocked)
├── test_traccar.py          # Cliente Traccar REST (mocked)
├── test_retransmit.py       # Cola retransmisión JSONL
├── test_integration.py      # Flujo completo (pendiente)
└── fixtures/
    ├── valid_payload.json
    └── invalid_payload.json
```

## Cómo correr

```bash
# Todos los tests
pytest tests/

# Un módulo específico
pytest tests/test_payload.py -v

# Con coverage
pytest tests/ --cov=src --cov-report=term-missing
```

##Fixtures

- `valid_payload.json` — payload válido según spec ATU
- `invalid_payload.json` — casos inválidos por campo

## Casos cubiertos

| Test | Qué verifica |
|------|-------------|
| `test_valid_payload_from_fixture` | Payload correcto pasa validación |
| `test_imei_too_short` | IMEI < 15 dígitos → rejected |
| `test_imei_too_long` | IMEI > 15 dígitos → rejected |
| `test_latitude_out_of_range_high` | lat > 90 → rejected |
| `test_longitude_out_of_range_low` | lon < -180 → rejected |
| `test_speed_too_high` | speed > 999.99 → rejected |
| `test_direction_id_invalid` | direction_id != 0,1 → rejected |
| `test_identifier_present_but_empty` | identifier "" → rejected |
| `test_knots_to_kmh` | Conversión correcta 1 knot = 1.852 km/h |
| `test_write_and_read` | JSONL queue write/read round-trip |
| `test_default_values` | Config carga defaults correctos |
| `test_env_override` | Env vars sobreescriben defaults |
