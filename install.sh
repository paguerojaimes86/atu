#!/bin/bash
set -e

echo "=== ATU GPS Service Installer ==="
echo

SERVICE_FILE="systemd/atu-gps.service"
SYSTEMD_DIR="$HOME/.config/systemd/user"

if [ "$(id -u)" -eq 0 ]; then
    SYSTEMD_DIR="/etc/systemd/system"
    echo "[root] Installing system-wide systemd service..."
else
    echo "[user] Installing user systemd service..."
fi

mkdir -p "$SYSTEMD_DIR"
cp "$SERVICE_FILE" "$SYSTEMD_DIR/"

echo "Copied service file to $SYSTEMD_DIR/atu-gps.service"

if [ "$(id -u)" -eq 0 ]; then
    systemctl daemon-reload
    systemctl enable atu-gps
    systemctl start atu-gps
    echo
    echo "Service enabled and started (systemd)."
    echo "Logs: journalctl -u atu-gps -f"
else
    systemctl --user daemon-reload
    systemctl --user enable atu-gps
    systemctl --user start atu-gps
    echo
    echo "Service enabled and started (user systemd)."
    echo "Logs: journalctl --user -u atu-gps -f"
fi

echo
echo "=== Service Commands ==="
echo "Start:   systemctl start atu-gps"
echo "Stop:    systemctl stop atu-gps"
echo "Restart: systemctl restart atu-gps"
echo "Status:  systemctl status atu-gps"
echo "Logs:    journalctl -u atu-gps -f"
