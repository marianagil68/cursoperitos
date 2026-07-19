# Portal Pericial

# 00 - Contexto del proyecto

## Versión

1.0

## Última actualización

2026-07-18

---

# 1. Objetivo

Portal Pericial es una plataforma web destinada a la gestión integral de pericias informáticas.

El sistema permitirá administrar expedientes, clientes, organismos, documentación, evidencias, informes periciales y toda la información relacionada con la actividad profesional del perito.

El proyecto se desarrolla como una aplicación propia, priorizando una arquitectura mantenible, escalable y con bajo acoplamiento.

---

# 2. Objetivos técnicos

- Desarrollar una aplicación mantenible.
- Separar claramente las responsabilidades de cada capa.
- Utilizar una arquitectura simple y fácil de comprender.
- Evitar dependencias innecesarias.
- Mantener el control total sobre las consultas SQL.
- Facilitar futuras ampliaciones del sistema.

---

# 3. Tecnologías

Backend

- Python
- Flask

Base de datos

- PostgreSQL

Acceso a datos

- psycopg

Frontend

- HTML5
- Bootstrap
- JavaScript

Control de versiones

- Git
- GitHub

---

# 4. Principios del proyecto

Durante todo el desarrollo deberán respetarse los siguientes principios.

- Arquitectura por capas.
- Repository Pattern.
- SQL escrito manualmente.
- Sin ORM.
- Bajo acoplamiento.
- Alta cohesión.
- Código simple y legible.
- Comentarios en español.
- Antes de implementar una solución se analiza completamente el diseño para minimizar refactorizaciones posteriores.

---

# 5. Estado actual

Actualmente se encuentra finalizado:

- Configuración del entorno de desarrollo.
- Configuración del servidor.
- PostgreSQL operativo.
- Conexión mediante túnel SSH.
- Conexión desde DBeaver.
- Estructura inicial del proyecto.

Próximo objetivo:

Implementar la capa de acceso a datos comenzando por la clase Database.

---

# 6. Documentación

La documentación del proyecto se encuentra organizada en los siguientes documentos.

01 - Entorno de desarrollo

02 - Arquitectura

03 - Base de datos

04 - Backend Flask

05 - Frontend

06 - API

07 - Decisiones técnicas

08 - Roadmap

09 - Diario de desarrollo

10 - Git

99 - Contexto para ChatGPT

---

# 7. Metodología de trabajo

Cada funcionalidad seguirá el siguiente ciclo:

1. Analizar el problema.
2. Definir la solución.
3. Implementar.
4. Probar.
5. Documentar.
6. Realizar commit.
7. Continuar con la siguiente funcionalidad.

La documentación forma parte del desarrollo y debe mantenerse actualizada durante todo el proyecto.