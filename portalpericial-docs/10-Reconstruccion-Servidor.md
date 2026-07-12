# 10. Reconstrucción del Servidor

**Proyecto:** Portal Pericial  
**Versión:** 1.0  
**Última actualización:** 12/07/2026

---

# Índice

1. Objetivo
2. Requisitos
3. Orden de reconstrucción
4. Configuración inicial
5. Instalación de CloudPanel
6. Instalación de Docker
7. Restauración de PostgreSQL
8. Restauración de pgAdmin
9. Restauración de Moodle
10. Restauración de aplicaciones
11. Configuración de seguridad
12. Verificaciones finales
13. Referencias

---

# 1. Objetivo

Este documento describe el procedimiento completo para reconstruir la infraestructura del proyecto Portal Pericial sobre un servidor nuevo.

Debe seguirse en el orden indicado.

---

# 2. Requisitos

Antes de comenzar se debe disponer de:

- VPS nuevo.
- Ubuntu 24.04 LTS.
- Acceso SSH.
- Dominio configurado.
- Copias de seguridad.
- Documentación completa del proyecto.

---

# 3. Orden de reconstrucción

La reconstrucción debe realizarse siguiendo esta secuencia:

1. Configurar DNS.
2. Instalar Ubuntu.
3. Instalar CloudPanel.
4. Configurar sitios.
5. Instalar Docker.
6. Restaurar PostgreSQL.
7. Restaurar pgAdmin.
8. Restaurar Moodle.
9. Restaurar aplicaciones propias.
10. Configurar seguridad.
11. Verificar funcionamiento.

No modificar este orden salvo que exista una razón técnica justificada.

---

# 4. Configuración inicial

Verificar:

- Acceso SSH.
- Resolución DNS.
- Hora del servidor.
- Actualización del sistema operativo.

Actualizar Ubuntu.

```bash
sudo apt update
sudo apt upgrade
```

---

# 5. Instalación de CloudPanel

Instalar CloudPanel siguiendo la documentación oficial.

Crear los siguientes sitios:

| Dominio | Tipo |
|----------|------|
| portalpericial.com.ar | PHP |
| campus.portalpericial.com.ar | PHP |
| pgadmin.portalpericial.com.ar | Reverse Proxy |

Configurar los certificados SSL.

Verificar acceso al panel.

---

# 6. Instalación de Docker

Instalar:

- Docker Engine.
- Docker Compose.

Crear el directorio:

```text
/opt/postgresql
```

Restaurar:

```text
.env
docker-compose.yml
```

Iniciar los servicios.

```bash
docker compose up -d
```

Verificar.

```bash
docker compose ps
```

---

# 7. Restauración de PostgreSQL

Verificar que PostgreSQL esté iniciado.

Restaurar las bases de datos utilizando los backups disponibles.

Confirmar:

- Usuarios.
- Bases de datos.
- Permisos.

Verificar conexión desde pgAdmin.

---

# 8. Restauración de pgAdmin

Acceder a:

```
https://pgadmin.portalpericial.com.ar
```

Registrar nuevamente el servidor PostgreSQL.

Configuración recomendada:

| Campo | Valor |
|--------|-------|
| Host | postgres |
| Port | 5432 |
| Maintenance Database | postgres |

Confirmar acceso a las bases de datos.

---

# 9. Restauración de Moodle

Restaurar:

- Código fuente.
- config.php.
- moodledata.

Verificar el Document Root configurado en CloudPanel.

Instalar nuevamente la extensión PostgreSQL para PHP si fuera necesario.

```bash
sudo apt install php8.4-pgsql
```

Reiniciar PHP.

```bash
sudo systemctl restart php8.4-fpm
```

Comprobar acceso a Moodle.

---

# 10. Restauración de aplicaciones

Restaurar:

- Código fuente.
- Variables de entorno.
- Archivos de configuración.
- Servicios necesarios.

Verificar la conexión con PostgreSQL.

---

# 11. Configuración de seguridad

Confirmar:

- SSH mediante claves Ed25519.
- PasswordAuthentication deshabilitado.
- PostgreSQL accesible únicamente desde localhost.
- pgAdmin publicado mediante Reverse Proxy.
- Certificados SSL válidos.

Consultar:

**07-Seguridad.md**

---

# 12. Verificaciones finales

Comprobar el funcionamiento de todos los servicios.

| Servicio | Estado |
|----------|--------|
| SSH | □ |
| CloudPanel | □ |
| Docker | □ |
| PostgreSQL | □ |
| pgAdmin | □ |
| Moodle | □ |
| Portal Principal | □ |
| HTTPS | □ |
| DNS | □ |
| Backups | □ |

Una vez completadas todas las verificaciones, el servidor puede considerarse operativo.

---

# 13. Referencias

- 01-Infraestructura-Servidor.md
- 02-CloudPanel.md
- 03-Docker.md
- 04-PostgreSQL.md
- 05-pgAdmin.md
- 06-Moodle.md
- 07-Seguridad.md
- 08-Backup-y-Restore.md
- 09-Mantenimiento.md