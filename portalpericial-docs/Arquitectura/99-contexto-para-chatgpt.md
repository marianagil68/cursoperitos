# Contexto para ChatGPT

## Objetivo

Este documento permite retomar el desarrollo del proyecto Portal Pericial en un nuevo chat sin perder el contexto técnico ni las decisiones de arquitectura ya tomadas.

Antes de proponer cambios o escribir código, leer este documento completo junto con:

- 00-contexto-proyecto.md
- 01-entorno-desarrollo.md
- 02-arquitectura.md

---

# Descripción del proyecto

Portal Pericial es una aplicación web para la gestión integral de pericias informáticas.

El objetivo es administrar clientes, organismos, expedientes, evidencias, documentación, informes periciales y demás procesos relacionados con la actividad profesional del perito informático.

El proyecto se desarrolla desde cero y se prioriza la calidad de la arquitectura por sobre la velocidad de implementación.

---

# Tecnologías

Backend

- Python
- Flask

Base de datos

- PostgreSQL

Acceso a datos

- psycopg

Frontend

- HTML
- Bootstrap
- JavaScript

Control de versiones

- Git
- GitHub

---

# Decisiones ya tomadas

Estas decisiones ya fueron analizadas y no deben replantearse salvo que exista un motivo técnico importante.

- No utilizar ORM.
- Todas las consultas SQL se escribirán manualmente.
- Utilizar Repository Pattern.
- Centralizar el acceso a la base de datos mediante una clase Database.
- Separar claramente la lógica de acceso a datos, la lógica de negocio y la presentación.
- Mantener una arquitectura simple y fácil de mantener.
- Priorizar código claro antes que soluciones excesivamente sofisticadas.

---

# Forma de trabajo

Durante el desarrollo seguir siempre esta metodología.

1. Analizar el problema completo antes de escribir código.
2. Proponer la solución.
3. Esperar confirmación cuando sea necesario.
4. Implementar.
5. Probar.
6. Continuar con el siguiente paso.

Evitar refactorizaciones innecesarias.

No modificar decisiones ya aprobadas sin justificar el cambio.

---

# Estado actual

Actualmente se encuentra implementado y probado:

## Infraestructura

- Entorno de desarrollo completo.
- PostgreSQL operativo.
- Flask configurado.
- psycopg funcionando.
- Clase Database con context manager.
- Conexión mediante DBeaver.
- Git y GitHub configurados.

## Arquitectura

Se utiliza la arquitectura:

Controller
↓
Service
↓
Repository
↓
Database
↓
PostgreSQL

No se utiliza ORM.

Todas las consultas SQL se escriben manualmente.

## Backend

Ya se encuentran implementados:

- Personas.
- Eventos.
- Inscripciones.
- Correos.
- Consultas.

Cada módulo mantiene la separación:

controller.py
service.py
repository.py
dto.py

## Eventos

Se implementaron:

- obtenerTodos()
- obtenerPublicosProximos()
- obtenerPorId()

Los eventos almacenan la URL de acceso (Zoom) que luego será enviada por correo al inscripto.

## Correos

Se implementó un módulo independiente para el envío de correos.

Estructura:

app/
└── correos/
    ├── controller.py
    ├── dto.py
    ├── repository.py
    └── service.py

Características:

- SMTP mediante Ferozo.
- Configuración desde .env.
- Auditoría completa en PostgreSQL.
- Registro de errores.
- Manejo de intentos.
- Estados:
    - PENDIENTE
    - ENVIADO
    - ERROR

El envío fue probado correctamente.

## Tabla correos

Existe la tabla:

public.correos

con auditoría completa de todos los envíos.

La fecha de envío se registra mediante:

CURRENT_TIMESTAMP

desde PostgreSQL.

## Pruebas realizadas

Se verificó correctamente:

- inserción del correo
- envío SMTP
- actualización de estado
- almacenamiento de fecha de envío
- incremento de intentos
- recepción del correo

## Fase 8 finalizada

La landing pública se encuentra integrada con Flask.

Se implementó:

- carga dinámica de charlas desde `GET /api/eventos`;
- formulario de inscripción mediante `POST /api/inscripciones`;
- creación o reutilización de personas por correo electrónico;
- prevención de inscripciones duplicadas;
- envío de confirmación con el enlace privado de Zoom;
- formulario de consultas mediante `POST /api/consultas`;
- aviso al administrador y acuse de recibo al participante;
- auditoría completa de correos;
- aviso visual cuando la persona ya estaba inscripta;
- reenvío de confirmación mediante `POST /api/inscripciones/reenviar-correo`;
- límite de cinco minutos entre reenvíos;
- honeypot en formularios públicos;
- CORS restringido al entorno local en modo `debug`;
- eliminación del mecanismo PHP anterior.

El endpoint `GET /correos/prueba` se conserva para pruebas manuales, pero solo funciona con `debug=True`. En producción responde `404`.

La implementación y las pruebas se documentan en:

```text
08-fase-8-integracion-landing.md
```

## Próximo objetivo

Preparar la puesta en producción:

- desplegar Flask con Gunicorn;
- configurar el reverse proxy `/api` en Nginx;
- publicar la landing;
- realizar una prueba completa sobre el dominio público.

# Estilo de código

- Comentarios en español.
- Código compacto.
- Nombres claros.
- Evitar complejidad innecesaria.
- Mantener consistencia en todo el proyecto.

---

# Cómo continuar

Antes de comenzar una nueva funcionalidad revisar la documentación existente.

Si una decisión importante cambia, actualizar la documentación correspondiente antes de continuar.

Este documento debe mantenerse actualizado para que cualquier nuevo chat pueda continuar el proyecto con el menor contexto posible.
