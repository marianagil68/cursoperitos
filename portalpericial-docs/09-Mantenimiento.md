# 09. Mantenimiento

**Proyecto:** Portal Pericial  
**Versión:** 1.0  
**Última actualización:** 12/07/2026

---

# Índice

1. Objetivo
2. Frecuencia de mantenimiento
3. Estado general del servidor
4. Ubuntu
5. Docker
6. PostgreSQL
7. CloudPanel
8. Moodle
9. Certificados SSL
10. Espacio en disco
11. Logs
12. Checklist de mantenimiento
13. Buenas prácticas
14. Referencias

---

# 1. Objetivo

Definir las tareas periódicas necesarias para mantener el servidor actualizado, seguro y funcionando correctamente.

Este documento está orientado al mantenimiento preventivo de la infraestructura.

---

# 2. Frecuencia de mantenimiento

| Frecuencia | Actividades |
|------------|-------------|
| Diaria | Verificar servicios y backups |
| Semanal | Revisar logs y estado general |
| Mensual | Actualizar software y comprobar espacio en disco |
| Antes de cambios importantes | Realizar backup completo |

---

# 3. Estado general del servidor

Verificar carga del sistema.

```bash
top
```

o

```bash
htop
```

Si `htop` no está instalado:

```bash
sudo apt install htop
```

Consultar memoria disponible.

```bash
free -h
```

Consultar espacio en disco.

```bash
df -h
```

---

# 4. Ubuntu

Actualizar índices de paquetes.

```bash
sudo apt update
```

Actualizar paquetes instalados.

```bash
sudo apt upgrade
```

Eliminar paquetes obsoletos.

```bash
sudo apt autoremove
```

Reiniciar únicamente cuando sea necesario.

```bash
sudo reboot
```

---

# 5. Docker

Verificar estado de los contenedores.

```bash
docker compose ps
```

Consultar logs.

```bash
docker compose logs
```

Actualizar imágenes.

```bash
docker compose pull
docker compose up -d
```

Eliminar imágenes sin uso.

```bash
docker image prune
```

---

# 6. PostgreSQL

Verificar que el contenedor esté funcionando.

```bash
docker compose ps
```

Consultar logs.

```bash
docker compose logs postgres
```

Verificar acceso desde pgAdmin.

---

# 7. CloudPanel

Comprobar acceso.

```
https://cloudpanel.portalpericial.com.ar:8443
```

Verificar:

- Sitios.
- PHP.
- Reverse Proxy.
- Certificados.

---

# 8. Moodle

Verificar:

- Acceso al sitio.
- Inicio de sesión.
- Creación de cursos.
- Subida de archivos.

URL:

```
https://campus.portalpericial.com.ar
```

---

# 9. Certificados SSL

CloudPanel renueva automáticamente los certificados Let's Encrypt.

Verificar periódicamente que los certificados continúen vigentes.

---

# 10. Espacio en disco

Consultar utilización.

```bash
df -h
```

Localizar directorios con mayor consumo.

```bash
du -sh /*
```

No permitir que el disco supere aproximadamente el 80 % de utilización.

---

# 11. Logs

Consultar logs del sistema.

```bash
journalctl -xe
```

Consultar logs de PHP.

```bash
journalctl -u php8.4-fpm
```

Consultar logs de Docker.

```bash
docker compose logs
```

Consultar logs de SSH.

```bash
journalctl -u ssh
```

---

# 12. Checklist de mantenimiento

## Diario

- Verificar acceso SSH.
- Verificar acceso a Moodle.
- Verificar acceso a pgAdmin.
- Confirmar ejecución de los backups.

---

## Semanal

- Revisar logs.
- Verificar espacio en disco.
- Revisar uso de memoria.
- Confirmar estado de Docker.

---

## Mensual

- Actualizar Ubuntu.
- Actualizar Docker.
- Actualizar imágenes de contenedores.
- Verificar certificados SSL.
- Revisar esta documentación.

---

# 13. Buenas prácticas

- No actualizar varios componentes críticos simultáneamente.
- Realizar un backup antes de cualquier actualización.
- Verificar el funcionamiento completo después de cada intervención.
- Registrar cualquier modificación realizada sobre el servidor.

---

# 14. Referencias

- 02-CloudPanel.md
- 03-Docker.md
- 04-PostgreSQL.md
- 06-Moodle.md
- 08-Backup-y-Restore.md
- 10-Reconstruccion-Servidor.md