#!/bin/bash
# ATU GPS Service — manual start/stop script
# Usage: ./run.sh [start|stop|status|restart|logs]

set -e
cd "$(dirname "$0")"

VENV="./.venv/bin/python"
MODULE="src.main"
PID_FILE="/tmp/atu-gps.pid"
LOG_FILE="/tmp/atu-gps.log"

start() {
    if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
        echo "ATU GPS already running (PID $(cat $PID_FILE))"
        return 1
    fi
    echo "Starting ATU GPS..."
    $VENV -m $MODULE >> "$LOG_FILE" 2>&1 &
    echo $! > "$PID_FILE"
    echo "Started (PID $(cat $PID_FILE)) — logs: $LOG_FILE"
}

stop() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            echo "Stopping ATU GPS (PID $PID)..."
            kill "$PID"
            rm -f "$PID_FILE"
            echo "Stopped"
        else
            echo "Process $PID not running"
            rm -f "$PID_FILE"
        fi
    else
        echo "Not running (no PID file)"
    fi
}

status() {
    if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
        PID=$(cat "$PID_FILE")
        echo "ATU GPS running (PID $PID)"
    else
        echo "ATU GPS not running"
    fi
}

logs() {
    tail -f "$LOG_FILE"
}

case "${1:-start}" in
    start)   start ;;
    stop)    stop ;;
    status)  status ;;
    restart) stop; sleep 1; start ;;
    logs)    logs ;;
    *)       echo "Usage: $0 {start|stop|status|restart|logs}" ;;
esac
