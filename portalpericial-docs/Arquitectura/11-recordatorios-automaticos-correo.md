# Recordatorios automáticos de charlas por correo

## 1. Objetivo

El sistema envía dos recordatorios individuales a las personas inscriptas:

- aproximadamente 24 horas antes de una charla;
- aproximadamente una hora antes de una charla.

El mensaje incluye:

- nombre de la persona;
- título de la charla;
- fecha y hora en Argentina;
- modalidad online;
- enlace privado de Zoom.

La solución utiliza el correo profesional de Portal Pericial configurado en
Donweb. No incorpora un proveedor de correo adicional.

---

## 2. Arquitectura

El envío no se expone como una operación pública del sitio. Se ejecuta mediante
un comando interno de Flask que puede ser iniciado manualmente o por `cron` en
el servidor.

```text
cron
  |
  v
comando Flask enviar-recordatorios
  |
  v
eventos dentro de la ventana de anticipación elegida
  |
  v
personas con inscripción activa
  |
  v
control de recordatorios ya enviados
  |
  v
mensaje text/plain + text/html
  |
  v
SMTP profesional de Donweb
  |
  v
registro del resultado en la tabla correos
```

No se coloca un botón de envío masivo en la parte pública porque una operación
de ese tipo requiere autenticación administrativa, permisos y protección
contra ejecuciones accidentales.

---

## 3. Componentes

### Comando

`PortalPericial/app/correos/commands.py`

Coordina el proceso, ofrece los modos de simulación y prueba, y muestra un
resumen de eventos, envíos, simulaciones, omisiones y errores.

### Eventos

`PortalPericial/app/eventos/repository.py`

Busca eventos activos cuya fecha de inicio esté dentro de la ventana
configurada.

`PortalPericial/app/eventos/service.py`

Expone al comando la búsqueda por ventana horaria y la búsqueda por ID.

### Inscripciones

`PortalPericial/app/inscripciones/repository.py`

Selecciona personas activas cuyas inscripciones estén en estado `INSCRIPTO` o
`CONFIRMADO`. No selecciona inscripciones `CANCELADO`, `ASISTIO` ni `AUSENTE`.

### Correo

`PortalPericial/app/correos/service.py`

Genera el contenido, controla duplicados, abre la conexión SMTP y registra el
resultado en PostgreSQL.

### Registro del comando

`PortalPericial/app/__init__.py`

Registra el comando para que Flask reconozca `enviar-recordatorios`.

---

## 4. Ventana de 24 horas

Los valores predeterminados son:

```text
desdehoras = 23.5
hastahoras = 24.5
```

La consulta utiliza parámetros de Psycopg:

```sql
AND fechainicio >= (
    CURRENT_TIMESTAMP + (%s * INTERVAL '1 hour')
)
AND fechainicio < (
    CURRENT_TIMESTAMP + (%s * INTERVAL '1 hour')
)
```

Los parámetros se entregan en el mismo orden:

```python
(desdehoras, hastahoras)
```

Por lo tanto:

```text
primer %s  = desdehoras
segundo %s = hastahoras
```

Si el comando se ejecuta el viernes a las 10:00, la ventana va desde el sábado
a las 09:30 hasta el sábado a las 10:30. Una charla del sábado a las 10:00 queda
incluida.

Los parámetros se mantienen separados del texto SQL para que Psycopg haga la
conversión correctamente y para evitar concatenar valores dentro de la
consulta.

### Ventana de una hora

Al ejecutar:

```bash
.venv/bin/python -m flask --app run:app \
  enviar-recordatorios --anticipacion una-hora
```

los valores predeterminados son:

```text
desdehoras = 0.5
hastahoras = 1.5
```

Si el comando se ejecuta a las 09:00, busca eventos que comiencen entre las
09:30 y las 10:30. Por lo tanto, encuentra una charla de las 10:00.

El valor predeterminado de `--anticipacion` es `un-dia`, de modo que el comando
y el cron existentes conservan su comportamiento.

---

## 5. Control de duplicados

Antes de enviar, el servicio consulta la tabla `correos` utilizando:

- persona;
- evento;
- destinatario;
- asunto del recordatorio;
- estado `ENVIADO`.

Si ya existe un recordatorio enviado con esa combinación, la persona se
contabiliza como omitida y no recibe otro.

Los recordatorios utilizan asuntos diferentes:

```text
Recordatorio: mañana es la charla | Portal Pericial
En una hora comienza la charla | Portal Pericial
```

Por eso, el recordatorio enviado el día anterior no impide el recordatorio de
una hora. Cada tipo mantiene su propio control de duplicados.

Cada intento se registra inicialmente como `PENDIENTE`. Después del intento
SMTP pasa a:

- `ENVIADO`, con fecha y `Message-ID`; o
- `ERROR`, con el detalle técnico.

Si un destinatario falla, el comando registra el error y continúa procesando a
los demás.

---

## 6. Formato del mensaje

El mensaje usa `multipart/alternative` y contiene:

1. una parte `text/plain`;
2. una parte `text/html`.

La versión de texto plano conserva el enlace de Zoom entre paréntesis. La
versión HTML contiene el botón visual.

El `Message-ID` utiliza el dominio obtenido de `SMTP_REMITENTE`, por ejemplo:

```text
<identificador@portalpericial.com>
```

Esto evita generar identificadores con el nombre local de la computadora.

---

## 7. Modos de ejecución

Todos los comandos deben ejecutarse desde:

```bash
cd /home/portalpericial-curso/apps/CursoPeritos/PortalPericial
```

El servicio utiliza el ejecutable:

```text
/home/portalpericial-curso/apps/CursoPeritos/PortalPericial/.venv/bin/python
```

### Simulación general

```bash
.venv/bin/python -m flask --app run:app \
  enviar-recordatorios --simular
```

### Simulación del recordatorio de una hora

```bash
.venv/bin/python -m flask --app run:app \
  enviar-recordatorios --anticipacion una-hora --simular
```

Consulta eventos e inscripciones y muestra los destinatarios. No abre SMTP y no
registra correos.

### Simulación de un evento

```bash
.venv/bin/python -m flask --app run:app \
  enviar-recordatorios --evento-id 1 --simular
```

`--evento-id` ignora la ventana de 24 horas y limita el proceso al evento
seleccionado.

### Correo controlado de prueba

```bash
.venv/bin/python -m flask --app run:app \
  enviar-recordatorios \
  --evento-id 1 \
  --destinatario-prueba correo-controlado@ejemplo.com \
  --nombre-prueba Mariana \
  --anticipacion una-hora
```

Este modo:

- envía como máximo un correo por evento;
- utiliza exclusivamente la dirección indicada;
- no envía a los participantes;
- no asocia el correo con la persona usada como referencia;
- agrega `PRUEBA` al asunto y un aviso visible en el cuerpo.

`--simular` y `--destinatario-prueba` no pueden utilizarse juntos.
`--nombre-prueba` requiere `--destinatario-prueba`.

### Envío real

```bash
.venv/bin/python -m flask --app run:app enviar-recordatorios
```

Este comando puede enviar correos reales a todas las inscripciones activas de
los eventos comprendidos en la ventana horaria. No debe ejecutarse para
explorar o probar.

---

## 8. Autenticación y entregabilidad

El SMTP de Donweb firma y transporta los mensajes del dominio.

En la prueba con Gmail se verificó:

```text
SPF:   PASS
DKIM:  PASS
DMARC: PASS
TLS:   1.3
```

También se verificó:

```text
X-Spam-Flag: NO
BAYES_HAM: 100%
```

La política DMARC actual está en modo de observación:

```text
p=NONE
```

No se modificaron DNS, SPF, DKIM ni DMARC durante este desarrollo. Cualquier
cambio futuro de política DMARC debe considerar primero todos los servicios
que envían correo con `portalpericial.com`.

---

## 9. Qué es cron

`cron` es el programador de tareas tradicional de Linux. Ejecuta comandos
automáticamente según una expresión de cinco campos:

```text
┌──────── minuto, de 0 a 59
│ ┌────── hora, de 0 a 23
│ │ ┌──── día del mes, de 1 a 31
│ │ │ ┌── mes, de 1 a 12
│ │ │ │ ┌ día de la semana, de 0 a 7
│ │ │ │ │
0 10 * * *
```

`0 10 * * *` significa:

```text
ejecutar todos los días a las 10:00
```

El comando diario solo encuentra eventos que comienzan aproximadamente 24
horas después. Si no encuentra ninguno, termina sin enviar correos.

`0 * * * *` significa ejecutar una vez por hora, en el minuto cero. Se utiliza
para buscar eventos que comienzan aproximadamente una hora después.

---

## 10. Zona horaria

Antes de instalar el cron se debe revisar:

```bash
timedatectl
date
```

Si el servidor usa `America/Argentina/Buenos_Aires`, las 10:00 se expresan como:

```cron
0 10 * * *
```

Si el servidor usa UTC, las 10:00 de Argentina corresponden a las 13:00 UTC:

```cron
0 13 * * *
```

No se debe instalar el cron hasta confirmar la zona horaria real del servidor.

---

## 11. Encontrar el Python del servicio

Consultar la definición:

```bash
systemctl cat portalpericial-curso.service
```

Revisar especialmente:

```text
WorkingDirectory=
ExecStart=
User=
```

El ejecutable que aparece en `ExecStart` permite identificar el entorno virtual.
Para cron es preferible utilizar una ruta absoluta como:

```text
/home/portalpericial-curso/apps/CursoPeritos/PortalPericial/.venv/bin/python
```

No se debe depender de que cron encuentre `python` o `flask` mediante `PATH`.

En la instalación verificada:

```text
User=portalpericial-curso
WorkingDirectory=/home/portalpericial-curso/apps/CursoPeritos/PortalPericial
ExecStart=.../PortalPericial/.venv/bin/gunicorn
```

---

## 12. Instalar el cron

Editar el cron del usuario que ejecutará la tarea:

```bash
crontab -u portalpericial-curso -e
```

Líneas para el servidor configurado con hora argentina:

```cron
0 10 * * * /usr/bin/flock -n /home/portalpericial-curso/recordatorios.lock /bin/bash -c 'cd /home/portalpericial-curso/apps/CursoPeritos/PortalPericial && exec .venv/bin/python -m flask --app run:app enviar-recordatorios' >> /home/portalpericial-curso/logs/recordatorios.log 2>&1
0 * * * * /usr/bin/flock -n /home/portalpericial-curso/recordatorios-una-hora.lock /bin/bash -c 'cd /home/portalpericial-curso/apps/CursoPeritos/PortalPericial && exec .venv/bin/python -m flask --app run:app enviar-recordatorios --anticipacion una-hora' >> /home/portalpericial-curso/logs/recordatorios.log 2>&1
```

Elementos de la línea:

- `0 10 * * *`: ejecuta el recordatorio del día anterior a las 10:00;
- `0 * * * *`: revisa cada hora el recordatorio de una hora;
- `/usr/bin/flock -n`: evita ejecuciones simultáneas;
- cada tarea tiene un archivo de bloqueo diferente para no impedir que la otra
  se ejecute;
- `/bin/bash -c`: ejecuta el bloque de comandos;
- `cd .../PortalPericial`: directorio desde el que se carga `.env`;
- `.venv/bin/python`: Python del entorno virtual;
- `-m flask --app run:app`: carga la aplicación;
- `enviar-recordatorios`: ejecuta el proceso;
- `>> archivo.log`: agrega la salida al log;
- `2>&1`: agrega también los errores.

Verificar la instalación:

```bash
crontab -u portalpericial-curso -l
```

La ruta `/home/portalpericial-curso/logs` pertenece al usuario del servicio y
es escribible por él.

---

## 13. Probar la infraestructura de cron sin enviar

Después de instalar la tarea, se puede validar el usuario, `flock`, el entorno
virtual, PostgreSQL y el log mediante una simulación.

La prueba utiliza archivos diferentes a los de la tarea real:

```bash
sudo -u portalpericial-curso /bin/bash -c \
  "/usr/bin/flock -n /home/portalpericial-curso/recordatorios-prueba.lock \
  /bin/bash -c 'cd /home/portalpericial-curso/apps/CursoPeritos/PortalPericial && exec .venv/bin/python -m flask --app run:app enviar-recordatorios --evento-id 1 --simular' \
  >> /home/portalpericial-curso/logs/recordatorios-prueba.log 2>&1"
```

Revisar el resumen:

```bash
tail -n 1 /home/portalpericial-curso/logs/recordatorios-prueba.log
```

El resultado esperado tiene cero envíos y cero errores:

```text
Eventos: 1 | Enviados: 0 | Simulados: N | Omitidos: 0 | Errores: 0
```

La simulación escribe nombres y direcciones en su log. Después de verificarla,
eliminar únicamente los archivos temporales:

```bash
rm \
  /home/portalpericial-curso/recordatorios-prueba.lock \
  /home/portalpericial-curso/logs/recordatorios-prueba.log
```

No eliminar:

```text
/home/portalpericial-curso/recordatorios.lock
/home/portalpericial-curso/recordatorios-una-hora.lock
/home/portalpericial-curso/logs/recordatorios.log
```

---

## 14. Lista de comprobación previa

Antes de activar cron:

- [ ] Los tests automáticos pasan.
- [ ] El servidor tiene el código actualizado.
- [ ] El backend fue reiniciado y está activo.
- [ ] El evento tiene `urlacceso`.
- [ ] La simulación encuentra el evento esperado.
- [ ] La cantidad de destinatarios es correcta.
- [ ] El correo controlado de prueba llega correctamente.
- [ ] SPF, DKIM y DMARC pasan.
- [ ] Se confirmó la zona horaria.
- [ ] Se confirmó el Python del entorno virtual.
- [ ] Se confirmó que el usuario de cron puede escribir el log.
- [ ] La prueba completa de cron con `--simular` termina sin errores.
- [ ] El recordatorio `una-hora` tiene asunto y texto propios.
- [ ] Las dos líneas de cron aparecen en el crontab.

---

## 15. Operación y diagnóstico

### Ver la salida de cron

```bash
tail -n 100 /home/portalpericial-curso/logs/recordatorios.log
```

### Verificar el servicio

```bash
systemctl is-active portalpericial-curso.service
journalctl -u portalpericial-curso.service -n 100 --no-pager
```

### Verificar cron

```bash
crontab -u portalpericial-curso -l
systemctl is-active cron
```

Según la distribución, el servicio puede llamarse `crond`:

```bash
systemctl is-active crond
```

### Estados en la tabla correos

- `PENDIENTE`: registro creado antes de completar SMTP;
- `ENVIADO`: SMTP confirmó el envío;
- `ERROR`: el intento falló y contiene detalle técnico.

No se debe repetir manualmente un envío sin revisar antes la tabla `correos`,
porque podría producir duplicados.

### Problemas frecuentes

`No existe el evento con id ...`

: El ID no corresponde a un evento almacenado.

`La charla no tiene configurado un enlace de acceso`

: Falta `urlacceso` en el evento.

`No pudimos enviar el correo`

: Revisar credenciales, host, puerto, TLS/SSL, conectividad y el campo `error`
  de la tabla `correos`.

`Eventos: 0`

: No hay eventos dentro de la ventana de 23,5 a 24,5 horas.

---

## 16. Despliegue

Este cambio afecta solamente al backend. No requiere:

- migraciones de base de datos;
- publicación mediante `rsync` de la landing;
- modificación de DNS.

El procedimiento es:

1. ejecutar tests locales;
2. revisar y versionar únicamente los archivos del backend;
3. subir el commit a GitHub;
4. comprobar que el repositorio del servidor esté limpio;
5. crear un respaldo;
6. ejecutar `git pull origin main`;
7. ejecutar los tests en el servidor;
8. reiniciar `portalpericial-curso.service`;
9. ejecutar una simulación;
10. instalar cron;
11. verificar el log después de la primera ejecución.

---

## 17. Retirar la automatización

Para detener futuros envíos automáticos:

```bash
crontab -u portalpericial-curso -e
```

Eliminar únicamente la línea de `enviar-recordatorios`, guardar y verificar:

```bash
crontab -u portalpericial-curso -l
```

Quitar el cron no elimina inscripciones, eventos ni registros históricos de la
tabla `correos`.
