# Fase 7 - Módulo de correos

## Objetivo

Implementar un módulo de envío de correos desacoplado del resto de la aplicación, con auditoría completa de todos los envíos.

---

# Arquitectura

Se creó un nuevo módulo:

app/
└── correos/
    ├── __init__.py
    ├── controller.py
    ├── dto.py
    ├── repository.py
    └── service.py

Responsabilidades:

- Repository
    - Acceso a PostgreSQL.
    - Alta de correos.
    - Actualización de estado.

- Service
    - Construcción del mensaje.
    - Conexión SMTP.
    - Envío.
    - Registro del resultado.

---

# Configuración SMTP

Toda la configuración quedó en el archivo .env.

Variables:

SMTP_HOST
SMTP_PORT
SMTP_USUARIO
SMTP_PASSWORD
SMTP_REMITENTE
SMTP_NOMBRE
SMTP_USAR_TLS
SMTP_USAR_SSL

El Config carga automáticamente estos valores.

---

# Tabla correos

Se creó la tabla:

public.correos

Campos principales:

- correoid
- personaid
- eventoid
- remitente
- destinatario
- asunto
- cuerpohtml
- fechacreacion
- fechaenviosmtp
- estado
- intentos
- error
- messageid

Estados:

PENDIENTE
ENVIADO
ERROR

Se decidió no utilizar ENUM de PostgreSQL.

---

# Repository

Métodos implementados

crear()

- Inserta el registro.
- Estado inicial:
    PENDIENTE

marcarenviado()

Actualiza:

- estado
- fechaenviosmtp
- intentos
- messageid

La fecha se obtiene mediante:

CURRENT_TIMESTAMP

para que siempre provenga del servidor PostgreSQL.

marcarerror()

Actualiza:

- estado
- intentos
- error

obtenerporid()

Obtiene un correo por su id.

---

# Service

Flujo implementado

crear registro
↓

SMTP

↓

si OK

↓

marcarenviado()

↓

si ERROR

↓

marcarerror()

↓

relanza la excepción

De esta forma siempre queda auditoría incluso si el servidor SMTP falla.

---

# Endpoint de prueba

Se creó temporalmente:

GET /correos/prueba

Su finalidad es probar:

- inserción
- SMTP
- actualización de estado

---

# Pruebas realizadas

Prueba completa exitosa.

Verificado:

✓ inserción en public.correos

✓ envío SMTP

✓ actualización a estado ENVIADO

✓ fechaenviosmtp

✓ intentos

✓ recepción del correo

---

# Incidente encontrado

Error:

permission denied for table correos

Causa:

El usuario utilizado por Flask no tenía permisos sobre la nueva tabla.

Solución:

GRANT sobre:

- tabla correos

y sobre la secuencia Identity correspondiente.

Una vez otorgados los permisos el módulo funcionó correctamente.

---

# Estado

Fase completamente terminada.

No quedaron tareas pendientes en el módulo de correos.