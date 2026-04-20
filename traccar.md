Analiza el archivo OpenAPI que te adjunto y dame únicamente la información exacta y verificable de la spec para estos 3 casos:

1. Obtener el token
2. Listar datos del vehículo
3. Obtener la última ubicación GPS actualizada del vehículo

Quiero que respondas en español y con formato técnico claro.

Instrucciones obligatorias:
- No inventes endpoints ni parámetros.
- Usa solo lo que exista literalmente en la spec.
- Indica el método HTTP y la ruta exacta de cada endpoint.
- Indica base URL o servers definidos en la spec, si existen.
- Indica el tipo de autenticación requerido para cada endpoint.
- Indica headers obligatorios.
- Indica query params, path params o body requeridos y opcionales.
- Indica el content-type correcto.
- Indica el tipo de respuesta y los campos importantes de la respuesta.
- Si hay varias formas de autenticar, explícalas.
- Si para obtener la última ubicación GPS hay que hacer más de un paso, explícalo paso a paso.
- Señala restricciones importantes, validaciones, errores comunes y advertencias operativas.
- Si hay una forma incorrecta pero tentadora de consultar la última ubicación, aclara por qué no conviene usarla.
- Incluye ejemplos listos para usar en cURL.
- Sé muy preciso con campos como: id, deviceId, uniqueId, positionId, lastUpdate, latitude, longitude, speed, fixTime, serverTime, valid, address.
- Si el endpoint devuelve muchos campos, prioriza los importantes pero menciona también el esquema general.

Quiero la salida exactamente con esta estructura:

# 1) Obtener token
- Endpoint:
- Método:
- Autenticación:
- Headers:
- Body / Params:
- Respuesta:
- Ejemplo cURL:
- Notas importantes:

# 2) Listar datos del vehículo
- Endpoint:
- Método:
- Autenticación:
- Headers:
- Query params:
- Respuesta:
- Campos importantes del vehículo:
- Ejemplo cURL:
- Notas importantes:

# 3) Última ubicación GPS actualizada del vehículo
- Endpoint correcto:
- Método:
- Autenticación:
- Headers:
- Params:
- Flujo correcto paso a paso:
- Respuesta:
- Campos importantes de ubicación:
- Ejemplo cURL:
- Error común a evitar:
- Notas importantes:

Al final agrega una sección:

# Resumen operativo final
con los 3 endpoints exactos y el flujo mínimo necesario para implementarlo.

Importante:
quiero exactitud de nivel implementación. No quiero una explicación genérica de telemetría ni de APIs REST. Quiero lo que dice la spec y cualquier detalle clave que me pueda romper la integración.
