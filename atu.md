Actúa como un arquitecto de software senior y desarrollador backend senior especializado en integraciones en tiempo real, WebSocket, telemetría GPS, validación de payloads, resiliencia, observabilidad y documentación técnica.

Necesito que diseñes y desarrolles una solución completa para transmitir tramas GPS a la ATU mediante WebSocket, cumpliendo estrictamente el manual técnico que te resumiré abajo. No omitas ningún requisito. Si detectas inconsistencias en el manual, no las ignores: documéntalas, toma una decisión técnica razonable y deja esa decisión parametrizable.

## Contexto funcional

La solución debe enviar información de dispositivos GPS de vehículos de transporte público regular al Sistema Integrado de Control y Monitoreo (SICM) de la ATU mediante WebSocket.

La autenticación se realiza con un token único por empresa.

Hay dos fases:

1. Fase de pruebas
- La empresa solicita token temporal al correo: sicm.gps@atu.gob.pe
- Asunto del correo: "Solicitud de credenciales WebSocket"
- Debe adjuntarse un archivo Excel por cada ruta autorizada con:
  - PLACA
  - Código IMEI
- También se envían datos de contacto:
  - nombre
  - correo electrónico
  - celular
  - persona o empresa de coordinación para la fase de pruebas
- En pruebas se debe transmitir la trama de al menos 15 dispositivos GPS por cada ruta autorizada
- Endpoint de pruebas:
  ws://devrecepcion.atu.gob.pe:5000/ws?token=TOKEN_DE_EMPRESA

2. Fase de transmisión en tiempo real
- Luego de aprobar pruebas, ATU entrega token definitivo y endpoint definitivo
- En producción debe transmitirse la totalidad de dispositivos GPS del listado enviado por cada ruta autorizada
- Si la empresa requiere más de un token definitivo, debe sustentar la solicitud al correo sicm.gps@atu.gob.pe

## Reglas operativas obligatorias

- Solo se debe transmitir durante la prestación del servicio, es decir, cuando el vehículo esté en viaje de ida o de vuelta
- Cada vehículo debe actualizar su información como máximo cada 20 segundos
- Los datos con antigüedad mayor a 10 minutos son retransmisión y deben enviarse por otro endpoint, el cual está "en desarrollo"; por tanto, debes dejar esa lógica desacoplada y configurable
- La verificación del estado de transmisión se realiza en SICM:
  https://soluciones.atu.gob.pe/sicm/login
- El usuario y contraseña son los mismos de la Plataforma Virtual de Trámites (PVT)
- En SICM, en el menú "Flota Vehicular", se revisa el estado de transmisión
- La actualización de IMEI también se hace en SICM, en "Flota Vehicular", opción "Editar" del campo IMEI GPS

## Payload WebSocket requerido

La estructura de la trama es JSON y debe incluir:

- imei
- latitude
- longitude
- route_id
- ts
- license_plate
- speed
- direction_id
- driver_id
- tsinitialtrip
- identifier (opcional)

## Tipos y restricciones

Implementa validaciones estrictas antes del envío:

- imei: obligatorio; el manual lo tipa como number, pero el ejemplo JSON lo envía como string; valida 15 caracteres y deja configurable la serialización final
- latitude: obligatorio, decimal, rango válido -90 a 90
- longitude: obligatorio, decimal, rango válido -180 a 180
- route_id: obligatorio, string, máximo 10 caracteres
- ts: obligatorio, timestamp en milisegundos, POSIX UTC+0
- license_plate: obligatorio, string, máximo 7 caracteres, puede incluir guion
- speed: obligatorio, decimal, rango 0 a 999.99 km/h
- direction_id: obligatorio, number, solo 0 para ida y 1 para vuelta
- driver_id: obligatorio, string, máximo 20 caracteres
- tsinitialtrip: obligatorio, timestamp en milisegundos, POSIX UTC+0
- identifier: opcional, string alfanumérico, máximo 50 caracteres; si se envía, no puede estar vacío

## Ejemplo de trama de referencia

{
  "imei": "435654321239569",
  "latitude": -12.228012,
  "longitude": -76.931337,
  "route_id": "1180",
  "ts": 1757119795000,
  "license_plate": "ABC123",
  "speed": 77.5,
  "direction_id": 1,
  "driver_id": "12345678",
  "tsinitialtrip": 1757097480000,
  "identifier": "m3d3dqfvdfr2ed2d"
}

## Respuesta esperada del servidor por cada trama

La respuesta contiene:
- Código
- Identifier
- Timestamp

Debes manejar al menos estos códigos:

- 00: trama recepcionada correctamente
- 01: verificar el formato de la trama enviada
- 03: InvalidToken
- 05: identificador vacío
- 06: IMEI inválido
- 07: placa inválida
- 08: coordenadas inválidas
- 09: velocidad inválida
- 10: operador inválido
- 11: identificador inválido
- 12: ID de ruta inválido
- 13: ID de dirección inválido
- 14: ID de conductor inválido

## Lo que debes entregar

Quiero una respuesta completa, estructurada y ejecutable con estas secciones exactas:

### 1. Resumen ejecutivo
Explica en lenguaje claro qué se va a construir, cómo funcionará y cuáles son los riesgos técnicos.

### 2. Supuestos y decisiones técnicas
Lista todas las suposiciones necesarias.
Identifica cualquier inconsistencia del manual, especialmente la tipificación de imei, y define cómo la resolverás sin bloquear la integración.

### 3. Arquitectura de la solución
Incluye:
- componentes
- flujo de datos
- flujo de validación
- flujo de envío
- flujo de respuesta
- manejo de reconexión
- manejo de errores
- separación entre pruebas, producción y retransmisión

### 4. Modelo de datos y contrato JSON
Entrega una tabla precisa con:
- campo
- tipo lógico
- obligatorio
- validaciones
- ejemplo válido
- ejemplo inválido

### 5. Diseño del cliente WebSocket
Debes proponer:
- conexión con token por query string
- reconexión automática con backoff exponencial
- heartbeat o estrategia equivalente si aplica
- control de duplicados
- control de orden de envío
- buffer/cola por vehículo
- timeouts
- idempotencia basada en identifier si conviene

### 6. Reglas de validación
Escribe todas las reglas de validación previas al envío.
Incluye pseudocódigo o código real para cada validación.
Mapea validaciones internas con posibles códigos de respuesta del servidor.

### 7. Diseño de observabilidad y auditoría
Define logs estructurados, métricas y alertas.
Quiero como mínimo:
- conexión / desconexión
- reintentos
- payload rechazado localmente
- payload enviado
- respuesta recibida
- código recibido
- latencia
- vehículo, IMEI, ruta y conductor
- separación entre error de validación, error de transporte y error remoto

### 8. Código fuente base listo para usar
Entrégame código completo, modular y bien organizado.
Elige un stack razonable para backend en tiempo real.
Debes incluir como mínimo:
- archivo de configuración
- cliente WebSocket
- validador de payload
- modelo de datos
- servicio de envío
- parser de respuestas
- logger
- main de arranque
- ejemplos de payload
- manejo de ambientes
- pruebas unitarias iniciales

Si eliges Python, usa una estructura profesional con clases, typing, validaciones y configuración por variables de entorno.
Si eliges Node.js/TypeScript, usa tipado estricto y arquitectura limpia.
Elige solo un stack, el más adecuado, y justifícalo.

### 9. Configuración
Proporciona ejemplo de archivo de configuración o variables de entorno para:
- endpoint_pruebas
- endpoint_produccion
- endpoint_retransmision
- token
- intervalo_segundos
- max_retries
- backoff
- logs
- modo_serializacion_imei
- validaciones habilitadas

### 10. Plan de pruebas
Incluye:
- pruebas unitarias
- pruebas de integración
- pruebas de reconexión
- pruebas de validación
- pruebas con respuestas simuladas 00, 01, 03, 05, 06, 07, 08, 09, 11, 12, 13 y 14
- prueba de cambio de entorno de pruebas a producción
- prueba de retraso > 10 minutos para retransmisión

### 11. Checklist operativo
Incluye checklist antes de pruebas y antes de producción:
- token cargado
- endpoint correcto
- listado IMEI/placa validado
- mínimo 15 dispositivos por ruta en pruebas
- totalidad de dispositivos por ruta en producción
- frecuencia de 20 segundos validada
- monitoreo activo
- SICM verificado

### 12. Manual técnico breve
Explica:
- cómo instalar
- cómo configurar
- cómo ejecutar
- cómo probar
- cómo leer logs
- cómo pasar a producción

### 13. Manual operativo breve
Explica:
- cómo solicitar token
- cómo preparar el Excel por ruta
- cómo revisar transmisión en SICM
- cómo actualizar IMEI en SICM
- cómo reportar incidencias

### 14. Riesgos y mitigaciones
Enumera los principales riesgos:
- token inválido
- datos mal tipados
- desalineación IMEI/placa
- desconexión WebSocket
- envío fuera de frecuencia
- timestamps inválidos
- retransmisión enviada al endpoint incorrecto
- inconsistencias del manual

### 15. Criterios de aceptación
Define criterios claros y verificables para dar por terminado el desarrollo.

## Restricciones de tu respuesta

- No me des una respuesta superficial
- No omitas detalles
- No resumas de forma vaga
- No dejes secciones sin contenido
- Si algo no está explícito en el manual, dilo como supuesto
- Diferencia claramente entre requisito explícito e inferencia técnica
- Produce contenido que sirva tanto para implementar como para revisar técnicamente
- Si das código, debe ser coherente, ejecutable y consistente con la arquitectura propuesta

## Importante

Antes de comenzar, haz una sección llamada:
"Requisitos extraídos del manual"
y enumera uno por uno todos los requisitos que estás usando como base.

Después desarrolla el resto.
