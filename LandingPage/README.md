# Landing Page de Portal Pericial

## Estado actual

La landing pública está integrada con el backend Flask de Portal Pericial.

La versión anterior enviaba los formularios mediante archivos PHP y se conectaba directamente al servidor SMTP. Ese mecanismo fue reemplazado por la API del backend y los archivos PHP fueron eliminados.

El frontend conserva el diseño y los estilos originales. Las charlas informativas se obtienen dinámicamente desde PostgreSQL a través del backend.

## Arquitectura

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

La landing nunca recibe ni muestra el enlace de Zoom en la respuesta pública de eventos. El backend obtiene ese enlace desde la base de datos únicamente cuando debe construir el correo de confirmación.

## Funcionalidades integradas

### Charlas informativas

- Las tarjetas se cargan desde `GET /api/eventos`.
- Se muestran únicamente eventos públicos, activos y próximos.
- Las fechas y horas se presentan en la zona horaria de Buenos Aires.
- El enlace de Zoom no se expone en el navegador.

### Inscripción a una charla

El formulario envía un JSON a:

```http
POST /api/inscripciones
```

Flujo:

```text
Seleccionar charla
        ↓
Completar formulario
        ↓
Buscar o crear persona por correo electrónico
        ↓
Crear inscripción si todavía no existe
        ↓
Enviar aviso al administrador
        ↓
Enviar confirmación al participante con el enlace de Zoom
        ↓
Redirigir a gracias.html
```

El correo electrónico es la clave de negocio utilizada para reconocer a una persona. La comparación no distingue entre mayúsculas y minúsculas.

### Inscripción repetida

Una persona no puede inscribirse dos veces a la misma charla.

Cuando el backend informa que la inscripción ya existía, el frontend no redirige automáticamente. Muestra un aviso y permite elegir entre:

- reenviar el correo con los datos de acceso;
- cerrar el formulario.

El reenvío utiliza:

```http
POST /api/inscripciones/reenviar-correo
```

Características:

- solo se envía el correo al participante;
- no se repite el aviso al administrador;
- cada intento queda auditado en `public.correos`;
- se admite un reenvío cada cinco minutos;
- si se intenta antes, el backend responde con HTTP `429`.

### Formulario de consultas

El formulario de contacto envía un JSON a:

```http
POST /api/consultas
```

El backend:

- busca o crea la persona;
- envía la consulta al administrador;
- envía un acuse de recibo al participante;
- registra ambos correos en la auditoría;
- redirige a `gracias.html` cuando la operación finaliza correctamente.

### Protección contra bots

Los formularios incluyen un campo oculto `_honey`.

Si ese campo es completado, el backend devuelve una respuesta neutra sin crear personas, inscripciones ni correos.

## Configuración de la API

La URL base se determina automáticamente en `js/main.js`.

En desarrollo local:

```text
http://127.0.0.1:5000/api
```

En producción:

```text
/api
```

En producción, Nginx debe redirigir las solicitudes de `/api` hacia la aplicación Flask. La landing y la API quedan así bajo el mismo dominio y no necesitan CORS.

## Prueba local

### 1. Abrir el túnel SSH de PostgreSQL

El backend local utiliza PostgreSQL remoto mediante el puerto local `5433`. El túnel debe permanecer abierto durante toda la prueba.

El comando se encuentra documentado en:

```text
portalpericial-docs/Arquitectura/01-entorno-desarrollo.md
```

### 2. Levantar el backend

Desde `PortalPericial`:

```powershell
.\.venv\Scripts\Activate.ps1
python run.py
```

El backend queda disponible en:

```text
http://127.0.0.1:5000
```

### 3. Levantar la landing

Desde `LandingPage`:

```powershell
python -m http.server 8080 --bind 127.0.0.1
```

Abrir en el navegador:

```text
http://127.0.0.1:8080
```

El backend habilita CORS únicamente en modo de desarrollo para:

- `http://127.0.0.1:8080`
- `http://localhost:8080`

## Pruebas realizadas

Se verificó correctamente:

- carga dinámica de dos charlas desde PostgreSQL;
- presentación de horarios en la zona horaria correcta;
- ausencia del enlace de Zoom en la API pública;
- creación de persona e inscripción;
- prevención de personas e inscripciones duplicadas;
- envío del aviso al administrador;
- envío de la confirmación al participante;
- auditoría de correos enviados y fallidos;
- reenvío solicitado por el participante;
- límite de cinco minutos entre reenvíos;
- ausencia de un segundo aviso al administrador durante el reenvío;
- formulario de consultas;
- redirección a `gracias.html`;
- funcionamiento visual del modal de inscripción repetida;
- ausencia de errores y advertencias en el navegador.

## Archivos principales

```text
LandingPage/
├── index.html
├── gracias.html
├── README.md
├── assets/
├── css/
│   └── styles.css
└── js/
    └── main.js
```

## Seguridad

- No deben guardarse contraseñas SMTP ni credenciales de PostgreSQL en esta carpeta.
- El frontend no se conecta directamente a PostgreSQL ni al servidor SMTP.
- Toda validación sensible se realiza nuevamente en el backend.
- El enlace privado de Zoom solo se incluye en los correos enviados por el backend.
