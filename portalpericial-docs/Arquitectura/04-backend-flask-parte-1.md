# 04 - Backend Flask - Parte 1

## Versión

1.0

## Fecha

2026-07-18

---

# Objetivo

Implementar la infraestructura base del backend Flask y dejar operativo el primer módulo funcional (`eventos`), validando la arquitectura definida para el proyecto.

---

# Estructura implementada

Se creó la estructura inicial del proyecto basada en módulos funcionales.

```
app/
│
├── config/
│   ├── config.py
│   └── database.py
│
├── eventos/
│   ├── controller.py
│   ├── repository.py
│   ├── service.py
│   └── dto.py
│
├── personas/
├── inscripciones/
├── mail/
└── shared/
```

Se decidió mantener una arquitectura por módulos en lugar de separar globalmente controllers, repositories y services.

Cada módulo contiene todas las capas necesarias para mantener alta cohesión y bajo acoplamiento.

---

# Configuración

Se incorporó un archivo `.env` para almacenar la configuración sensible.

Variables utilizadas:

```
DB_HOST
DB_PORT
DB_NAME
DB_USER
DB_PASSWORD
```

Para el entorno de desarrollo se utiliza:

```
DB_HOST=localhost
DB_PORT=5433
```

El puerto 5433 corresponde al túnel SSH local utilizado para acceder al PostgreSQL del servidor.

---

# Clase Config

Se creó:

```
app/config/config.py
```

Responsabilidades:

- cargar variables desde `.env`
- exponer la configuración mediante una clase `Config`

Actualmente administra la configuración de conexión a PostgreSQL.

---

# Clase Database

Se implementó:

```
app/config/database.py
```

Características:

- Context Manager (`with Database()`)
- apertura automática de conexión
- commit automático
- rollback automático ante errores
- cierre automático de la conexión

Métodos implementados:

- ejecutar()
- obteneruno()
- obtenertodos()

Se utiliza `psycopg` con `dict_row` para obtener resultados como diccionarios.

---

# Patrón Repository

Se decidió centralizar todo el acceso a datos mediante Repository Pattern.

La arquitectura queda definida de la siguiente forma:

```
Controller
        │
        ▼
Service
        │
        ▼
Repository
        │
        ▼
Database
        │
        ▼
PostgreSQL
```

De esta forma:

- el Controller no conoce SQL
- el Service no conoce detalles de conexión
- el Repository concentra todas las consultas SQL

---

# Módulo Eventos

Se implementó el primer módulo funcional del sistema.

Capas creadas:

- controller
- service
- repository

Consulta implementada:

```
obtenerpublicosproximos()
```

La consulta devuelve únicamente eventos:

- activos
- visibles
- cuya fecha de inicio sea posterior al momento actual

Ordenados por fecha de inicio.

---

# Endpoint implementado

Se publicó el endpoint:

```
GET /eventos
```

El endpoint devuelve un JSON con los eventos públicos próximos.

Prueba realizada satisfactoriamente.

---

# Inicialización de Flask

Se creó:

```
run.py
```

y la fábrica de aplicación:

```
app/__init__.py
```

Responsabilidades:

- crear la aplicación Flask
- cargar la configuración
- registrar los Blueprints

---

# Pruebas realizadas

## Conexión a PostgreSQL

Se creó:

```
testconexion.py
```

Resultado:

- conexión exitosa
- autenticación correcta
- lectura de datos correcta

---

## Endpoint REST

Se verificó:

```
GET /eventos
```

Resultado:

- Flask operativo
- acceso a PostgreSQL correcto
- respuesta JSON correcta

---

# Decisiones técnicas

Se ratifican las siguientes decisiones de arquitectura:

- Flask como framework web.
- psycopg como acceso a PostgreSQL.
- SQL escrito manualmente.
- Repository Pattern.
- Arquitectura por módulos.
- Configuración mediante `.env`.
- Sin ORM.

---

# Estado del proyecto

Finalizado:

- infraestructura Flask
- configuración
- conexión PostgreSQL
- clase Database
- Repository Pattern
- módulo Eventos
- primer endpoint REST operativo

Próximo objetivo:

Implementar el módulo Personas siguiendo la misma arquitectura.