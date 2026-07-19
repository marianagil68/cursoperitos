# 07. Seguridad

**Proyecto:** Portal Pericial  
**Versión:** 1.0  
**Última actualización:** 12/07/2026

---

# Índice

1. Objetivo
2. Principios de seguridad
3. Servicios publicados
4. SSH
5. Claves Ed25519
6. Configuración de SSH
7. Firewall
8. HTTPS
9. PostgreSQL
10. pgAdmin
11. Problemas encontrados
12. Buenas prácticas
13. Referencias

---

# 1. Objetivo

Este documento describe las políticas de seguridad adoptadas para proteger la infraestructura del proyecto Portal Pericial.

Las medidas implementadas tienen como objetivo reducir la superficie de ataque sin afectar la administración del servidor.

---

# 2. Principios de seguridad

La infraestructura se basa en los siguientes principios:

- Publicar únicamente los servicios necesarios.
- Utilizar HTTPS en todos los accesos web.
- Mantener PostgreSQL inaccesible desde Internet.
- Administrar PostgreSQL únicamente mediante pgAdmin.
- Utilizar autenticación SSH mediante claves.
- Documentar cualquier modificación de seguridad.

---

# 3. Servicios publicados

Actualmente los únicos puertos publicados son:

| Puerto | Servicio |
|---------|----------|
| 80 | HTTP (redirección) |
| 443 | HTTPS |
| 5650 | SSH |

No existen otros servicios accesibles desde Internet.

---

# 4. SSH

La administración remota se realiza mediante SSH.

Puerto configurado:

```
5650
```

Acceso desde Windows:

```powershell
ssh -p 5650 root@IP_DEL_SERVIDOR
```

No es necesario utilizar PuTTY.

Windows incorpora OpenSSH de forma nativa.

---

# 5. Claves Ed25519

La autenticación utiliza claves Ed25519.

Generación de la clave:

```powershell
ssh-keygen -t ed25519 -C "mariana@portalpericial"
```

Archivos generados:

```text
id_ed25519
id_ed25519.pub
```

La clave pública se instala en:

```text
~/.ssh/authorized_keys
```

Permisos recomendados:

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

---

# 6. Configuración de SSH

Archivo de configuración:

```text
/etc/ssh/sshd_config
```

Configuración utilizada:

```text
PermitRootLogin yes
PasswordAuthentication no
```

Antes de reiniciar el servicio siempre verificar:

```bash
sudo sshd -t
```

Reiniciar:

```bash
sudo systemctl restart ssh
```

---

# 7. Firewall

Los únicos servicios accesibles desde Internet son:

- HTTP
- HTTPS
- SSH

Verificar puertos abiertos:

```bash
ss -lntp
```

---

# 8. HTTPS

Todos los sitios utilizan certificados Let's Encrypt administrados por CloudPanel.

Dominios configurados:

| Dominio | Servicio |
|----------|----------|
| portalpericial.com.ar | Portal |
| campus.portalpericial.com.ar | Moodle |
| pgadmin.portalpericial.com.ar | pgAdmin |
| cloudpanel.portalpericial.com.ar | CloudPanel |

---

# 9. PostgreSQL

PostgreSQL escucha únicamente en:

```text
127.0.0.1:5432
```

No acepta conexiones externas.

---

# 10. pgAdmin

pgAdmin escucha únicamente en:

```text
127.0.0.1:5050
```

CloudPanel publica el servicio mediante Reverse Proxy.

No se expone el puerto 5050.

---

# 11. Problemas encontrados

## Acceso SSH

Inicialmente se utilizaba autenticación mediante contraseña.

Se migró a autenticación mediante claves Ed25519.

---

## Puerto PostgreSQL

Inicialmente PostgreSQL estaba publicado hacia Internet.

Se restringió a:

```text
127.0.0.1:5432
```

---

## Certificado HTTPS

Chrome mostraba:

```
No seguro
```

La causa fue una política HSTS almacenada localmente.

Se solucionó eliminando dicha política del navegador.

---

# 12. Buenas prácticas

- Mantener PasswordAuthentication deshabilitado.
- Utilizar claves con passphrase.
- No compartir claves privadas.
- Mantener Docker actualizado.
- Mantener Ubuntu actualizado.
- No publicar PostgreSQL.
- No publicar pgAdmin directamente.
- Verificar periódicamente los certificados SSL.

---

# 13. Referencias

- 02-CloudPanel.md
- 03-Docker.md
- 04-PostgreSQL.md
- 05-pgAdmin.md
- Documentación oficial de OpenSSH