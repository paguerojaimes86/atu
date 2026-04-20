# ATU GPS Bridge - La Ocho Ruta 1060

Servicio Python que puentea datos GPS de Traccar al WebSocket de ATU SICM para la empresa La Ocho, ruta 1060.

## Características

- **58 vehículos validados** registrados en ATU ruta 1060
- Extracción automática de placa desde `deviceName` de Traccar
- Uso de timestamp actual (ATU rechaza posiciones con más de ~1 minuto de edad)
- Cola de retransmisión para posiciones stale (>10 min)
- Logging estructurado JSON

## Stack

- Python 3.11+, `asyncio`
- `websockets` — cliente WebSocket ATU
- `aiohttp` — cliente REST Traccar
- `pydantic` v2 — validación de payloads
- `structlog` — logging estructurado

## Estructura

```
atu/
├── src/
│   ├── __init__.py
│   ├── config.py      # Configuración desde env vars
│   ├── logger.py      # structlog setup
│   ├── payload.py     # ATUPayload model + validators
│   ├── atuc.py        # Cliente WebSocket ATU
│   ├── traccar.py     # Cliente REST Traccar (JSESSIONID auth)
│   ├── retransmit.py  # Cola JSONL para retransmisión
│   └── main.py        # Punto de entrada + mapa de dispositivos
├── tests/             # 17 tests passing
├── systemd/           # Unit file para systemd
├── INSTALL.md         # Manual de instalación
└── README.md
```

## Instalación

Ver [INSTALL.md](./INSTALL.md) para instrucciones completas de instalación en Ubuntu 24.04.

## Configuración

Copiar `.env.example` a `.env`:

```env
ATU_ENDPOINT_TEST=ws://devrecepcion.atu.gob.pe:5000/ws
ATU_TOKEN=<token-de-atu>
ATU_INTERVAL_SECONDS=20
TRACCAR_BASE_URL=http://161.132.47.112:8082
TRACCAR_EMAIL=admin@laocho.com
TRACCAR_PASSWORD=<password>
LOG_LEVEL=INFO
```

## Ejecución

```bash
# Development
python -m src.main

# Con systemd
systemctl start atu-gps
journalctl -u atu-gps -f
```

## Tests

```bash
pytest tests/ -v
```

## Códigos de Respuesta ATU

| Código | Significado |
|--------|-------------|
| `00` | Trama aceptada correctamente |
| `07` | Placa inválida (no coincide con IMEI en ATU) |
| `16` | IMEI no registrado o no vinculado a ruta |

## Logs

Logs JSON a stdout. Eventos clave:

- `atu_payload_sent_response` — `codigo=00|07|16`
- `retransmit_stale` — posición encolada por ser muy antigua
- `polling_error` — error al conectar con Traccar

## Dispositivos Validados

Los 58 dispositivos están hardcodeados en `src/main.py:ATU_ROUTE_1060_IMEI_MAP` con el IMEI exacto que ATU tiene registrado para cada placa.

Dispositivos no reconocidos son ignorados silenciosamente.

## Endpoints

| Entorno | Endpoint |
|---------|----------|
| Test ATU | `ws://devrecepcion.atu.gob.pe:5000/ws?token=TOKEN` |
| Traccar | `http://161.132.47.112:8082/api` |
