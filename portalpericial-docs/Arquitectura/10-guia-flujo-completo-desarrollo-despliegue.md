# Guía práctica: desarrollo, prueba y despliegue

## Portal Pericial

**Versión:** 1.0
**Última actualización:** 2026-07-24

---

# 1. Objetivo

Este tutorial resume el flujo completo para:

1. actualizar el proyecto local;
2. modificarlo en una rama;
3. probar la landing y el backend localmente;
4. publicar los cambios en GitHub;
5. desplegarlos en el servidor;
6. verificar producción y controlar la caché.

Para instalar el proyecto en una computadora nueva, consultar:

```text
portalpericial-docs/Arquitectura/09-guia-trabajo-local-colaboradores.md
```

---

# 2. Reglas importantes

- GitHub es la fuente oficial del código.
- Los cambios se hacen localmente, no directamente en `htdocs`.
- Se trabaja en una rama y se integra en `main` antes de desplegar.
- Nunca se agrega `PortalPericial/.env` a Git.
- Antes de desplegar se crean respaldos.
- Siempre se simula `rsync` antes de ejecutarlo realmente.
- Una eliminación inesperada debe investigarse.
- No usar `git reset --hard`, `push --force` ni compartir claves privadas.

---

# 3. Actualizar el proyecto local

Abrir una terminal PowerShell:

```powershell
cd "C:\Users\Mariana\Dropbox\Sistemas\CursoPeritos"
git switch main
git pull --ff-only
```

Verificar:

```powershell
git status
git branch --show-current
```

No continuar si aparecen modificaciones que no se reconocen.

Crear una rama:

```powershell
git switch -c feature/descripcion-corta
```

Ejemplos:

```text
feature/boton-whatsapp
fix/hora-correo
docs/guia-despliegue
```

---

# 4. Probar localmente

Se utilizan tres terminales que deben permanecer abiertas.

## Terminal 1: túnel de PostgreSQL

```powershell
ssh -N -L 5433:127.0.0.1:5432 -p 5650 portalpericial-campus@149.50.152.230
```

El túnel conecta:

```text
127.0.0.1:5433 → PostgreSQL del servidor
```

Un colaborador debe usar su propio usuario SSH autorizado.

## Terminal 2: backend Flask

```powershell
cd "C:\Users\Mariana\Dropbox\Sistemas\CursoPeritos\PortalPericial"
.\.venv\Scripts\Activate.ps1
python run.py
```

El backend queda en:

```text
http://127.0.0.1:5000
```

Probar:

```text
http://127.0.0.1:5000/api/eventos
```

Debe responder JSON con los eventos públicos.

## Terminal 3: landing

```powershell
cd "C:\Users\Mariana\Dropbox\Sistemas\CursoPeritos\LandingPage"
python -m http.server 8080 --bind 127.0.0.1
```

Abrir:

```text
http://127.0.0.1:8080
```

## No abrir `index.html` directamente

No utilizar una dirección como:

```text
C:/Users/Mariana/.../LandingPage/index.html
```

ni una URL `file:///...`.

En ese modo la consulta a la API puede mostrar:

```text
Failed to fetch
```

La landing debe abrirse mediante `http://127.0.0.1:8080`.

## Comprobar los puertos

```powershell
netstat -ano | Select-String ':5433|:5000|:8080'
```

Los tres deben aparecer como `LISTENING`.

| Problema | Causa habitual |
|---|---|
| `Failed to fetch` | Se abrió el HTML como archivo o el backend está apagado |
| `ERR_CONNECTION_REFUSED` en `8080` | No se levantó la landing |
| Error de PostgreSQL | El túnel está apagado o usa otro puerto |

---

# 5. Precaución durante las pruebas

El entorno local se conecta a la base de datos y al SMTP reales.

Una prueba manual puede:

- crear personas e inscripciones;
- guardar auditorías;
- enviar correos reales.

Usar una dirección controlada. Para varias pruebas pueden utilizarse alias:

```text
nombre+prueba1@gmail.com
nombre+prueba2@gmail.com
```

Cada alias es considerado un correo diferente.

Ejecutar también las pruebas automáticas:

```powershell
cd "C:\Users\Mariana\Dropbox\Sistemas\CursoPeritos\PortalPericial"
python -m pytest -q
```

Las pruebas automáticas no deben enviar correos reales.

---

# 6. Revisar, guardar y publicar los cambios

Volver a la raíz:

```powershell
cd "C:\Users\Mariana\Dropbox\Sistemas\CursoPeritos"
```

Revisar:

```powershell
git status --short
git diff
git diff --check
```

Agregar solamente los archivos de la tarea:

```powershell
git add ruta-del-archivo
```

Ejemplo:

```powershell
git add LandingPage/index.html LandingPage/css/styles.css
```

Comprobar lo preparado:

```powershell
git status --short
git diff --cached --check
git diff --cached --stat
```

Crear el commit y publicar la rama:

```powershell
git commit -m "Describe brevemente el cambio"
git push -u origin feature/descripcion-corta
```

El aviso `LF will be replaced by CRLF` es habitual en Windows y no implica por
sí mismo un error.

---

# 7. Integrar en `main`

Después de revisar y aprobar la rama, puede utilizarse un Pull Request.

Para una integración local controlada:

```powershell
git switch main
git pull --ff-only
git merge feature/descripcion-corta
git push origin main
```

`Fast-forward` indica que se integró sin conflictos.

Verificar:

```powershell
git status -sb
git log -2 --oneline --decorate
```

No desplegar hasta que el cambio aparezca en `origin/main`.

---

# 8. Conectarse al servidor

```powershell
ssh -p 5650 root@149.50.152.230
```

La terminal debe mostrar algo semejante a:

```text
[root@vps-6154810-x ~] #
```

Si Git informa `detected dubious ownership`:

```bash
git config --global --add safe.directory /home/portalpericial-curso/apps/CursoPeritos
```

Ocurre porque el repositorio pertenece a `portalpericial-curso`, mientras que
la administración se realiza como `root`.

---

# 9. Revisar y respaldar antes del `pull`

Primero comprobar que nadie haya modificado el servidor:

```bash
cd /home/portalpericial-curso/apps/CursoPeritos
git status --short
git branch --show-current
git log -1 --oneline
```

El estado debe estar limpio y la rama debe ser `main`.

Si aparecen cambios, no hacer `pull` ni descartarlos. Primero hay que determinar
quién los hizo y guardarlos.

Respaldar el repositorio:

```bash
respaldo_repositorio="/home/portalpericial-curso/backups/CursoPeritos-antes-despliegue-$(date +%Y%m%d-%H%M%S)"
```

```bash
cp -a /home/portalpericial-curso/apps/CursoPeritos "$respaldo_repositorio"
ls -ld "$respaldo_repositorio"
```

Actualizar:

```bash
cd /home/portalpericial-curso/apps/CursoPeritos
git pull origin main
git log -1 --oneline --decorate
```

Respaldar la landing publicada:

```bash
respaldo_landing="/home/portalpericial-curso/backups/landing-antes-despliegue-$(date +%Y%m%d-%H%M%S)"
```

```bash
cp -a /home/portalpericial-curso/htdocs/curso.portalpericial.com.ar "$respaldo_landing"
ls -ld "$respaldo_landing"
```

---

# 10. Simular y realizar el despliegue

## Simulación

```bash
rsync -avhn --delete --itemize-changes \
  --exclude='.well-known/' \
  --exclude='README.md' \
  /home/portalpericial-curso/apps/CursoPeritos/LandingPage/ \
  /home/portalpericial-curso/htdocs/curso.portalpericial.com.ar/
```

La opción `-n` significa que no modifica nada.

Revisar especialmente las líneas `*deleting`. Si aparece un archivo
desconocido, comprobar si se utiliza:

```bash
grep -R "nombre-del-archivo" /home/portalpericial-curso/htdocs/curso.portalpericial.com.ar
```

No continuar hasta comprender cada eliminación.

## Despliegue real

Cuando la simulación sea correcta, ejecutar el mismo comando sin `-n`:

```bash
rsync -avh --delete --itemize-changes \
  --exclude='.well-known/' \
  --exclude='README.md' \
  /home/portalpericial-curso/apps/CursoPeritos/LandingPage/ \
  /home/portalpericial-curso/htdocs/curso.portalpericial.com.ar/
```

Si solamente cambió la landing, no es necesario reiniciar el backend.

Si cambió el backend:

```bash
systemctl restart portalpericial-curso.service
systemctl is-active portalpericial-curso.service
```

Debe responder `active`.

---

# 11. Verificar producción

Backend:

```bash
systemctl is-active portalpericial-curso.service
```

API interna:

```bash
curl -i http://127.0.0.1:8001/api/eventos
```

API pública:

```bash
curl -i https://curso.portalpericial.com.ar/api/eventos
```

Landing:

```bash
curl -I https://curso.portalpericial.com.ar/
```

Abrir:

```text
https://curso.portalpericial.com.ar/
```

Comprobar:

- carga la versión nueva;
- aparecen las charlas;
- las fechas y horas son correctas;
- cargan las imágenes;
- los enlaces nuevos son correctos;
- los formularios abren;
- no hay errores en la consola.

Si cambió el flujo de inscripción o correo, realizar además una prueba real con
una dirección controlada.

---

# 12. Caché del navegador

## Solución inmediata

Si incógnito muestra la versión nueva pero el navegador habitual muestra la
anterior:

```text
Ctrl + F5
```

## Configuración permanente para el HTML

El archivo de Nginx es:

```text
/etc/nginx/sites-enabled/curso.portalpericial.com.ar.conf
```

Respaldarlo:

```bash
cp -a /etc/nginx/sites-enabled/curso.portalpericial.com.ar.conf \
  /home/portalpericial-curso/backups/curso-nginx-antes-cache-$(date +%Y%m%d-%H%M%S).conf
```

En el bloque `location /`, inmediatamente después de `proxy_pass`, incluir:

```nginx
  location / {
    proxy_pass http://127.0.0.1:8080;

    add_header Cache-Control "no-cache, no-store, must-revalidate" always;
    add_header Pragma "no-cache" always;
    add_header Expires "0" always;

    # Continúa el resto de la configuración existente.
  }
```

Validar y aplicar:

```bash
nginx -t
systemctl reload nginx
systemctl is-active nginx
```

Verificar:

```bash
curl -I https://curso.portalpericial.com.ar/
```

La respuesta debe contener:

```text
cache-control: no-cache, no-store, must-revalidate
pragma: no-cache
expires: 0
```

## Versionar recursos estáticos

Cuando se reemplaza un CSS, JavaScript o imagen conservando el mismo nombre,
cambiar su versión en el HTML:

```html
<link rel="stylesheet" href="css/styles.css?v=20260724-1">
<script src="js/main.js?v=20260724-1"></script>
<img src="assets/mariana-gil.png?v=20260724-1" alt="Mariana Gil">
```

Así el navegador vuelve a descargar el recurso.

---

# 13. Cerrar las terminales

Al terminar las pruebas:

- landing local: `Ctrl + C`;
- backend local: `Ctrl + C`;
- túnel SSH: `Ctrl + C`;
- sesión del servidor: `exit`.

Cerrar estos procesos locales no afecta producción. El sitio público utiliza
Nginx, Gunicorn y systemd en el servidor.

---

# 14. Resumen del flujo

```text
Pull de main
    ↓
Crear rama
    ↓
Túnel + run.py + servidor 8080
    ↓
Modificar y probar
    ↓
Pytest
    ↓
Commit y push
    ↓
Integrar y subir main
    ↓
Revisar y respaldar el servidor
    ↓
Pull en el servidor
    ↓
Simular rsync
    ↓
Desplegar
    ↓
Probar API, landing y caché
```

---

# 15. Lista de control

## Antes del commit

- [ ] Se trabajó en una rama.
- [ ] Túnel, backend y landing funcionaron.
- [ ] La landing se abrió desde `http://127.0.0.1:8080`.
- [ ] Las pruebas finalizaron correctamente.
- [ ] No se incluyó `.env`.
- [ ] Se agregaron solamente archivos de la tarea.

## Antes del despliegue

- [ ] El cambio está en `origin/main`.
- [ ] El repositorio del servidor está limpio.
- [ ] Se respaldó el repositorio.
- [ ] Se respaldó la landing publicada.
- [ ] Se revisó el `dry run` de `rsync`.
- [ ] Se comprendieron todas las eliminaciones.

## Después del despliegue

- [ ] El backend está activo.
- [ ] La API responde HTTP 200.
- [ ] La landing muestra la versión nueva.
- [ ] Las charlas y recursos cargan.
- [ ] No hay errores visibles.
- [ ] Las cabeceras de caché son correctas.
