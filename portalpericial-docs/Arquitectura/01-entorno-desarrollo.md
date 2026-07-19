# Portal Pericial

# 01 - Entorno de desarrollo

## Versión

1.0

## Última actualización

2026-07-18

---

# 1. Objetivo

Este documento describe el entorno de desarrollo utilizado para Portal Pericial, incluyendo las herramientas, el acceso al servidor, la conexión a PostgreSQL y los procedimientos necesarios para comenzar a desarrollar.

---

# 2. Equipo de desarrollo

Sistema operativo:

- Windows 11

Editor:

- Visual Studio Code

Terminal:

- PowerShell

Cliente SSH:

- OpenSSH para Windows

Cliente de Base de Datos:

- DBeaver

Control de versiones:

- Git

Repositorio remoto:

- GitHub

---

# 3. Entorno Python

Python se ejecuta localmente utilizando un entorno virtual (venv).

Antes de comenzar a trabajar se debe activar el entorno virtual.

```powershell
.\venv\Scripts\activate
```

---

# 4. Servidor

Proveedor:

- DonWeb Cloud Server

Sistema Operativo:

- Ubuntu Server

Panel:

- CloudPanel

Servidor Web:

- Nginx

Aplicación:

- Flask

---

# 5. Acceso SSH

Servidor

```
149.50.152.230
```

Puerto

```
5650
```

Usuario

```
portalpericial-campus
```

Método de autenticación

- Clave ED25519

Conexión

```powershell
ssh -p 5650 portalpericial-campus@149.50.152.230
```

---

# 6. PostgreSQL

Motor

- PostgreSQL

Ubicación

- Docker sobre el servidor

Acceso desde desarrollo

- Mediante túnel SSH

---

# 7. Túnel SSH

Comando

```powershell
ssh -N -L 5433:127.0.0.1:5432 -p 5650 portalpericial-campus@149.50.152.230
```

Mientras la ventana permanezca abierta, el túnel estará activo.

Puerto local

```
5433
```

Puerto remoto PostgreSQL

```
5432
```

---

# 8. DBeaver

Configuración

Host

```
127.0.0.1
```

Puerto

```
5433
```

Usuario

```
postgres
```

La contraseña corresponde al usuario PostgreSQL configurado en el servidor.

---

# 9. Git

Repositorio alojado en GitHub.

Los cambios se realizan desde Visual Studio Code.

Flujo habitual

```text
Modificar archivos

↓

Commit

↓

Push
```

---

# 10. Problemas conocidos

## Exceeded MaxStartups

Síntoma

El servidor rechaza nuevas conexiones SSH.

Solución

Reiniciar el servicio SSH y volver a conectar.

---

## Permission denied (publickey)

Verificaciones realizadas

- authorized_keys
- permisos de .ssh
- fingerprint ED25519
- configuración efectiva de sshd

Resultado

Conexión restablecida correctamente.

---

## DBeaver intenta conectarse al puerto 5432

La conexión local debe realizarse al puerto:

```
5433
```

correspondiente al túnel SSH.

---

# 11. Verificación rápida

Antes de comenzar una sesión comprobar:

- El entorno virtual está activado.
- La conexión SSH funciona.
- El túnel SSH está activo.
- DBeaver conecta correctamente.
- PostgreSQL responde.
- Git está sincronizado con GitHub.