import asyncio
import signal
from datetime import datetime, timezone

from .atuc import ATUClient
from .config import get_settings
from .logger import configure_logger
from .payload import ATUPayload, knots_to_kmh
from .retransmit import RetransmitQueue
from .traccar import TraccarClient

ATU_ROUTE_1060_IMEI_MAP = {
    "A0A732": "357073293351009",
    "A0G723": "357073293354292",
    "A0J773": "354018115215430",
    "A0N782": "359633106074136",
    "A0Q756": "357073293354318",
    "A0X725": "863372050922037",
    "A0Y765": "357073290143508",
    "A0Z761": "357073290968375",
    "A1L772": "357073293355224",
    "A1U749": "357073290973052",
    "A2T779": "353201352917154",
    "A3Y702": "357073290972963",
    "A4F747": "357073290018866",
    "A5B720": "357073293351140",
    "A5B749": "352592573942356",
    "A5P729": "357073290087937",
    "A6I703": "357073293355208",
    "A6J721": "357073290016647",
    "A6M726": "357073293353773",
    "A6Q778": "354018110392358",
    "A8P743": "357073290857719",
    "A9D768": "357544375757552",
    "A9O706": "357073293354144",
    "AAR903": "350317170689156",
    "AAS843": "352592576462881",
    "AFT739": "357073293355182",
    "ASU715": "357073290016100",
    "ATG800": "865190072211116",
    "AVL763": "865190072208112",
    "AVL941": "865190072216487",
    "AVS749": "357073293354938",
    "B3B717": "357073293351090",
    "B3D743": "357073290022082",
    "B3F703": "357073293354490",
    "B3I793": "357544375742794",
    "B3V736": "357073293286114",
    "B4B784": "357073293351231",
    "B4B798": "357073293754640",
    "B4K743": "357073290016340",
    "B4Q788": "357073293351793",
    "C0A727": "357073290126164",
    "C2W747": "357073293355075",
    "C8N772": "357073293350944",
    "C8Q081": "357073293357683",
    "C8R796": "350424063791758",
    "D1G787": "357073293354086",
    "D8Y713": "352592573950136",
    "D9B732": "352592573967833",
    "F0E822": "357073293351306",
    "F2N819": "357073290973375",
    "F2W873": "352592573924834",
    "F3B797": "359633109873138",
    "F3B798": "353201352955246",
    "F3B947": "357073293357758",
    "F3J910": "357073293354987",
    "F8J833": "359633109867460",
    "ZDB952": "354017110205875",
    "ZDG967": "352592575768320",
}


def _is_stale(ts_ms: int) -> bool:
    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    age_ms = now_ms - ts_ms
    return age_ms > 10 * 60 * 1000


def _parse_traccar_timestamp(ts_str: str) -> int:
    dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
    return int(dt.timestamp() * 1000)


async def main() -> None:
    settings = get_settings()
    log = configure_logger(settings.log_level)

    log.info("service_starting", endpoint=settings.atu_endpoint_test)

    atuc = ATUClient(settings.atu_endpoint_test, settings.atu_token, log)
    traccar = TraccarClient(
        settings.traccar_base_url,
        settings.traccar_email,
        settings.traccar_password,
        log,
    )
    retransmit_q = RetransmitQueue("retransmit.jsonl", log)

    shutdown_event = asyncio.Event()

    def on_signal(sig: signal.Signals) -> None:
        log.info("shutdown_signal_received", signal=sig.name)
        shutdown_event.set()

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, on_signal, sig)

    try:
        await atuc.connect()
        await traccar.authenticate()

        devices_resp = await traccar.get_devices()
        device_map = {d["id"]: {"uniqueId": d.get("uniqueId", ""), "name": d.get("name", "")} for d in devices_resp}

        while not shutdown_event.is_set():
            try:
                positions = await traccar.get_positions()
                for pos in positions:
                    try:
                        device_id = pos.get("deviceId")
                        dev_info = device_map.get(device_id, {})
                        raw_name = dev_info.get("name", "")

                        if raw_name.startswith("(ANTIGUO)"):
                            continue

                        if " " in raw_name:
                            device_name = raw_name.split(" ", 1)[1]
                        elif "/" in raw_name:
                            device_name = raw_name.split("/", 1)[1]
                        else:
                            device_name = raw_name

                        if device_name not in ATU_ROUTE_1060_IMEI_MAP:
                            continue

                        unique_id = ATU_ROUTE_1060_IMEI_MAP[device_name].zfill(15)

                        traccar_ts_ms = _parse_traccar_timestamp(pos["fixTime"])
                        now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)

                        payload = ATUPayload(
                            imei=unique_id,
                            latitude=pos["latitude"],
                            longitude=pos["longitude"],
                            route_id="1060",
                            ts=now_ms,
                            license_plate=device_name or "ABC123",
                            speed=knots_to_kmh(pos["speed"]),
                            direction_id=0,
                            driver_id="LA8CHO",
                            tsinitialtrip=now_ms,
                            identifier=pos.get("attributes", {}).get("identifier"),
                        )

                        if _is_stale(traccar_ts_ms):
                            retransmit_q.write(payload.model_dump())
                            log.info("retransmit_stale", imei=payload.imei, ts_age_ms=traccar_ts_ms)
                        else:
                            resp = await atuc.send(payload)
                            log.info(
                                "atu_payload_sent_response",
                                imei=payload.imei,
                                codigo=resp.codigo,
                                descrip=resp.descrip,
                            )

                    except Exception as exc:
                        log.error("payload_processing_error", error=str(exc))

            except Exception as exc:
                log.error("polling_error", error=str(exc))
                await atuc.reconnect_with_backoff()

            await asyncio.sleep(settings.atu_interval_seconds)

    finally:
        await atuc.close()
        await traccar.close()
        log.info("service_stopped")


if __name__ == "__main__":
    asyncio.run(main())
