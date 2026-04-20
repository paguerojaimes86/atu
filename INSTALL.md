# Manual de Instalación - ATU GPS Bridge

## Requisitos
- Ubuntu 24.04 LTS x86_64
- Python 3.11+
- 4GB RAM mínimo (necesita ~300MB)
- Conexión a internet para reach:
  - 161.132.47.112:8082 (Traccar)
  - devrecepcion.atu.gob.pe:5000 (ATU WebSocket)

---

## 1. Actualizar Sistema

```bash
apt update && apt upgrade -y
```

## 2. Instalar Python y Dependencias

```bash
apt install -y python3 python3-venv python3-pip git
```

## 3. Crear Usuario del Servicio

```bash
useradd -m -s /bin/bash atu-gps
mkdir -p /opt/atu-gps
chown atu-gps:atu-gps /opt/atu-gps
```

## 4. Copiar Proyecto

```bash
# Opción A: Git clone
cd /opt/atu-gps
sudo -u atu-gps git clone https://github.com/paguerojaimes86/atu.git .
sudo -u atu-gps python3 -m venv .venv
sudo -u atu-gps /opt/atu-gps/.venv/bin/pip install -e /opt/atu-gps

# Opción B: Subir archivos manualmente
# Copiar todo el proyecto a /opt/atu-gps/
# Luego instalar dependencias:
sudo -u atu-gps /opt/atu-gps/.venv/bin/pip install -e /opt/atu-gps
```

## 5. Configurar Variables de Entorno

```bash
cp /opt/atu-gps/.env.example /opt/atu-gps/.env
nano /opt/atu-gps/.env
```

Editar con tus credenciales:

```env
ATU_ENDPOINT_TEST=ws://devrecepcion.atu.gob.pe:5000/ws
ATU_TOKEN=tu_token_aqui
ATU_INTERVAL_SECONDS=20
TRACCAR_BASE_URL=http://161.132.47.112:8082
TRACCAR_EMAIL=admin@laocho.com
TRACCAR_PASSWORD=tu_password_traccar
LOG_LEVEL=INFO
```

**Permisos correctos:**
```bash
chown atu-gps:atu-gps /opt/atu-gps/.env
chmod 600 /opt/atu-gps/.env
```

## 6. Crear Servicio systemd

```bash
cp /opt/atu-gps/systemd/atu-gps.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable atu-gps
```

**Editar el servicio para usar el venv correcto:**

```bash
nano /etc/systemd/system/atu-gps.service
```

Cambiar la línea ExecStart:
```ini
ExecStart=/opt/atu-gps/.venv/bin/python -m src.main
```

## 7. Iniciar Servicio

```bash
systemctl start atu-gps
systemctl status atu-gps
journalctl -u atu-gps -f  # Ver logs en tiempo real
```

## 8. Verificar Funcionamiento

```bash
# Ver logs
journalctl -u atu-gps --since "5 minutes ago" | grep codigo

# Debe mostrar codigo=00 para posiciones frescas
```

## 9. Logs y Debug

```bash
# Ver todos los logs
journalctl -u atu-gps -f

# Reiniciar
systemctl restart atu-gps

# Stop
systemctl stop atu-gps
```

---

## Solución de Problemas

### Error "Connection refused" a Traccar
- Verificar que TRACCAR_BASE_URL sea accesible
- Probar: curl -I http://161.132.47.112:8082

### Error "Token inválido" de ATU
- Regenerar token en el panel de ATU
- Actualizar ATU_TOKEN en .env

### codigo=07 (placa inválida)
- Verificar que el IMEI y placa estén en el mapa en src/main.py
- Los 58 dispositivos están configurados para ruta 1060

### codigo=16 (IMEI no registrado)
- El IMEI enviado no coincide con ATU
- Revisar ATU_ROUTE_1060_IMEI_MAP en src/main.py

---

## Comandos Rápidos

```bash
# Start
sudo systemctl start atu-gps

# Stop
sudo systemctl stop atu-gps

# Restart
sudo systemctl restart atu-gps

# Status
sudo systemctl status atu-gps

# Logs
sudo journalctl -u atu-gps -f

# Test manual
sudo -u atu-gps /opt/atu-gps/.venv/bin/python -c "from src.main import ATU_ROUTE_1060_IMEI_MAP; print(f'{len(ATU_ROUTE_1060_IMEI_MAP)} devices')"
```
