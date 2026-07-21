# CursoPeritos

Este repositorio funciona como un **monorepo** y reúne los distintos proyectos relacionados con Portal Pericial, la plataforma de capacitación y el plugin de pagos para Moodle.

## Estructura del repositorio

```text
CursoPeritos/
├── LandingPage/
├── PortalPericial/
├── mercadopago-docs/
├── portalpericial-docs/
└── ...
```

## Proyectos

### LandingPage

Sitio web público de Portal Pericial.

**Tecnologías:**

- HTML5
- CSS3
- JavaScript
- Bootstrap

**Contenido principal:**

- Landing de presentación y venta
- Página de agradecimiento
- Recursos gráficos
- Integración con el acceso al campus

### PortalPericial

Sistema principal desarrollado en Flask.

**Tecnologías:**

- Python
- Flask
- PostgreSQL
- psycopg
- Bootstrap

**Arquitectura:**

- Repository Pattern
- SQL manual, sin ORM
- Organización por módulos funcionales
- Separación entre controller, service y repository

**Módulos actuales:**

- Eventos
- Personas
- Inscripciones
- Mail
- Shared

### mercadopago-docs

Documentación técnica del desarrollo del plugin `paygw_mercadopago` para Moodle.

Incluye:

- Decisiones de arquitectura
- Fases de desarrollo
- Implementación
- Configuración
- Pruebas
- Puesta en producción

### portalpericial-docs

Documentación técnica del proyecto Portal Pericial.

Está organizada en dos áreas principales.

#### Infraestructura

Contiene documentación sobre:

- Servidor
- CloudPanel
- Docker
- PostgreSQL
- pgAdmin
- Moodle
- Seguridad
- Backup y restauración
- Mantenimiento
- Reconstrucción del servidor
- Configuración de correo

#### Arquitectura

Contiene documentación sobre:

- Contexto general del proyecto
- Entorno de desarrollo
- Decisiones técnicas
- Arquitectura del backend Flask
- Contexto para continuar el desarrollo en nuevos chats

## Organización del repositorio

Cada proyecto mantiene su propia estructura interna, pero todos comparten el mismo repositorio Git.

Los commits se realizan procurando separar los cambios por proyecto o responsabilidad.

Ejemplos:

```text
PortalPericial: agrega módulo personas
PortalPericial: implementa inscripción a eventos
LandingPage: actualiza formulario de contacto
MercadoPago: documenta puesta en producción
Docs: reorganiza documentación de infraestructura
```

## Autores

**Gerardo Petraglia y Mariana Gil**  
