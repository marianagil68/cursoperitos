# 08. Backup y Restauración

**Proyecto:** Portal Pericial  
**Versión:** 1.0  
**Última actualización:** 12/07/2026

---

# Índice

1. Objetivo
2. Estrategia de backup
3. Componentes a respaldar
4. Backup de PostgreSQL
5. Backup de Moodle
6. Backup de Docker
7. Backup de la documentación
8. Restauración
9. Verificaciones
10. Buenas prácticas
11. Referencias

---

# 1. Objetivo

Definir el procedimiento de respaldo y recuperación del servidor para minimizar la pérdida de información ante una falla del sistema, un error humano o una migración de infraestructura.

El objetivo es poder reconstruir completamente el servidor utilizando esta documentación y los backups almacenados.

---

# 2. Estrategia de backup

Se distinguen dos tipos de información.

## Datos

- Bases de datos PostgreSQL.
- moodledata.
- Archivos cargados por los usuarios.

---

## Configuración

- CloudPanel.
- Docker Compose.
- Variables de entorno.
- Configuración de Moodle.
- Scripts propios.
- Documentación.

---

# 3. Componentes a respaldar

| Componente | Método |
|------------|--------|
| PostgreSQL | pg_dump |
| Código Moodle | Copia de archivos |
| moodledata | Copia de archivos |
| config.php | Copia de archivo |
| Docker Compose | Copia de archivos |
| .env | Copia de archivo |
| Documentación | Repositorio Git |

---

# 4. Backup de PostgreSQL

Se recomienda utilizar siempre:

```bash
pg_dump
```

o realizar el backup desde pgAdmin.

No copiar directamente los archivos internos del volumen Docker.

---

# 5. Backup de Moodle

Respaldar los siguientes elementos:

- Código fuente.
- config.php.
- moodledata.
- Base de datos PostgreSQL.

Los cuatro componentes son indispensables para una restauración completa.

---

# 6. Backup de Docker

Respaldar el contenido del directorio:

```text
/opt/postgresql
```

Incluyendo:

```text
.env
docker-compose.yml
docker-compose.yml.bak
```

---

# 7. Backup de la documentación

Toda la documentación técnica debe mantenerse bajo control de versiones.

Se recomienda almacenarla en un repositorio Git.

Además, conservar una copia fuera del servidor.

---

# 8. Restauración

El orden recomendado es:

1. Restaurar Ubuntu.
2. Instalar CloudPanel.
3. Instalar Docker.
4. Restaurar la configuración Docker.
5. Iniciar PostgreSQL.
6. Restaurar las bases de datos.
7. Restaurar Moodle.
8. Restaurar moodledata.
9. Restaurar aplicaciones.
10. Verificar el funcionamiento.

El procedimiento detallado se encuentra en:

**10-Reconstruccion-Servidor.md**

---

# 9. Verificaciones

Después de una restauración comprobar:

- Acceso SSH.
- Acceso a CloudPanel.
- Acceso a pgAdmin.
- Acceso a Moodle.
- Integridad de las bases de datos.
- Funcionamiento de HTTPS.
- Correcta resolución DNS.

---

# 10. Buenas prácticas

- Mantener al menos dos copias de los backups.
- Conservar una copia fuera del servidor.
- Verificar periódicamente la restauración.
- Documentar cualquier cambio en la estrategia de respaldo.
- Realizar un backup antes de cualquier actualización importante.

---

# 11. Referencias

- 03-Docker.md
- 04-PostgreSQL.md
- 06-Moodle.md
- 09-Mantenimiento.md
- 10-Reconstruccion-Servidor.md