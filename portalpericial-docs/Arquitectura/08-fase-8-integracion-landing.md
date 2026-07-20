# Fase 8 - Integración de la landing pública

## Objetivo

Integrar la landing pública de Portal Pericial con el backend Flask para administrar charlas informativas, inscripciones, consultas y correos desde una única arquitectura.

La integración reemplaza el mecanismo anterior basado en PHP y conexión SMTP directa desde la landing.

---

# Arquitectura

```text
Landing HTML y JavaScript
        ↓
API Flask
        ↓
Controller → Service → Repository
        ↓
PostgreSQL
        ↓
SMTP de Ferozo
```

El frontend no se conecta directamente a PostgreSQL ni al servidor SMTP.

---

# Endpoints públicos

## Eventos

```http
GET /api/eventos
GET /api/eventos/{eventoid}
```

Devuelven únicamente información pública de eventos activos, visibles y próximos.

La propiedad privada `urlacceso`, que contiene el enlace de Zoom, nunca se incluye en estas respuestas.

## Inscripciones

```http
POST /api/inscripciones
```

Responsabilidades:

- validar los datos recibidos;
- buscar o crear la persona por correo electrónico;
- crear la inscripción a la charla;
- evitar personas e inscripciones duplicadas;
- enviar un aviso al administrador;
- enviar la confirmación al participante;
- incluir el enlace de Zoom únicamente en el correo;
- devolver si la inscripción fue creada o ya existía.

El correo electrónico es la clave de negocio de la persona. Se normaliza y se compara sin distinguir mayúsculas y minúsculas.

## Reenvío de confirmación

```http
POST /api/inscripciones/reenviar-correo
```

Solo permite reenviar el correo cuando la persona ya se encuentra inscripta en la charla indicada.

Características:

- envía únicamente al participante;
- no genera otro aviso para el administrador;
- crea un nuevo registro de auditoría;
- utiliza un asunto específico para distinguir el reenvío;
- permite un reenvío cada cinco minutos;
- responde con HTTP `429` cuando se intenta antes del plazo permitido.

## Consultas

```http
POST /api/consultas
```

Responsabilidades:

- validar nombre, correo, WhatsApp y consulta;
- buscar o crear la persona;
- enviar la consulta al administrador;
- enviar un acuse de recibo al participante;
- auditar ambos correos.

---

# Landing pública

Las tarjetas de las charlas se construyen dinámicamente con JavaScript a partir de `GET /api/eventos`.

Las fechas se presentan usando la zona horaria:

```text
America/Argentina/Buenos_Aires
```

El formulario de inscripción conserva el diseño original de la landing y utiliza `fetch()` para comunicarse con la API.

## Inscripción nueva

Cuando el backend devuelve `inscripcioncreada: true`, el frontend redirige a:

```text
gracias.html
```

## Inscripción repetida

Cuando devuelve `inscripcioncreada: false`, el formulario se oculta y se informa que la persona ya estaba inscripta.

El usuario puede:

- solicitar el reenvío del correo;
- cerrar el modal.

Los mensajes de error y el límite de reenvío se muestran dentro del mismo modal.

---

# Protección contra bots

Los formularios utilizan un campo honeypot llamado `_honey`.

Si el campo contiene un valor, el backend devuelve una respuesta neutra sin crear personas, inscripciones ni correos.

---

# CORS de desarrollo

En modo `debug`, el backend permite solicitudes desde:

```text
http://127.0.0.1:8080
http://localhost:8080
```

La habilitación no se aplica en producción.

En producción, la landing utiliza `/api` bajo el mismo dominio y Nginx debe redirigir esas solicitudes hacia Flask.

---

# Endpoint de prueba de correo

Se conserva:

```http
GET /correos/prueba
```

El endpoint solo está disponible con `debug=True`.

En producción responde `404` antes de crear auditoría o conectarse al servidor SMTP.

El destinatario se obtiene de `SMTP_DESTINATARIO_ADMIN`; no existen direcciones personales escritas en el código.

---

# Eliminación del mecanismo PHP

Se eliminaron de la landing:

- `enviar.php`;
- `config_smtp.php`;
- `SimpleSmtpMailer.php`;
- documentación específica de PHP y SMTP directo.

La landing ya no contiene credenciales ni configuración SMTP.

---

# Pruebas realizadas

Se verificó correctamente:

- carga dinámica de eventos;
- ocultamiento del enlace de Zoom en la API pública;
- horarios en la zona horaria correcta;
- creación y reutilización de personas;
- creación y prevención de inscripciones duplicadas;
- envío de avisos al administrador;
- envío de confirmaciones al participante;
- auditoría de correos enviados y fallidos;
- formulario de consultas;
- respuesta visual para inscripción repetida;
- reenvío real de una confirmación;
- bloqueo de un segundo reenvío dentro de cinco minutos;
- ausencia de un nuevo aviso al administrador durante el reenvío;
- protección del endpoint de prueba en producción;
- ausencia de errores y advertencias en el navegador.

Las pruebas automáticas del backend finalizaron con:

```text
8 passed
```

---

# Estado

La integración funcional de la Fase 8 se encuentra terminada y probada en el entorno local contra PostgreSQL y SMTP reales.

Pendiente para producción:

- desplegar el backend Flask;
- configurar Gunicorn;
- configurar el reverse proxy `/api` en Nginx;
- publicar la landing actualizada;
- ejecutar una prueba completa sobre el dominio público.
