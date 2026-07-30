# Recordatorios automáticos de charlas por correo

## 1. Objetivo

El sistema envía un recordatorio individual a las personas inscriptas
aproximadamente 24 horas antes de una charla.

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
eventos que comienzan dentro de aproximadamente 24 horas
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

En los ejemplos, `/ruta/real/python` debe reemplazarse por el ejecutable Python
del entorno virtual utilizado por el servicio.

### Simulación general

```bash
/ruta/real/python -m flask --app run:app \
  enviar-recordatorios --simular
```

Consulta eventos e inscripciones y muestra los destinatarios. No abre SMTP y no
registra correos.

### Simulación de un evento

```bash
/ruta/real/python -m flask --app run:app \
  enviar-recordatorios --evento-id 1 --simular
```

`--evento-id` ignora la ventana de 24 horas y limita el proceso al evento
seleccionado.

### Correo controlado de prueba

```bash
/ruta/real/python -m flask --app run:app \
  enviar-recordatorios \
  --evento-id 1 \
  --destinatario-prueba correo-controlado@ejemplo.com \
  --nombre-prueba Mariana
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
/ruta/real/python -m flask --app run:app enviar-recordatorios
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
/ruta/del/entorno/bin/python
```

No se debe depender de que cron encuentre `python` o `flask` mediante `PATH`.

---

## 12. Instalar el cron

Editar el cron del usuario que ejecutará la tarea:

```bash
crontab -e
```

Ejemplo para un servidor configurado con hora argentina:

```cron
0 10 * * * cd /home/portalpericial-curso/apps/CursoPeritos/PortalPericial && /ruta/real/python -m flask --app run:app enviar-recordatorios >> /var/log/portalpericial-recordatorios.log 2>&1
```

Elementos de la línea:

- `0 10 * * *`: horario;
- `cd .../PortalPericial`: directorio desde el que se carga `.env`;
- `/ruta/real/python`: Python del entorno virtual;
- `-m flask --app run:app`: carga la aplicación;
- `enviar-recordatorios`: ejecuta el proceso;
- `>> archivo.log`: agrega la salida al log;
- `2>&1`: agrega también los errores.

Verificar la instalación:

```bash
crontab -l
```

La ruta del log debe ser escribible por el usuario que ejecuta cron. Si el
servicio utiliza un usuario sin permiso sobre `/var/log`, se debe elegir una
ruta dentro de su directorio o configurar previamente el archivo y sus
permisos.

---

## 13. Lista de comprobación previa

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

---

## 14. Operación y diagnóstico

### Ver la salida de cron

```bash
tail -n 100 /var/log/portalpericial-recordatorios.log
```

### Verificar el servicio

```bash
systemctl is-active portalpericial-curso.service
journalctl -u portalpericial-curso.service -n 100 --no-pager
```

### Verificar cron

```bash
crontab -l
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

## 15. Despliegue

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

## 16. Retirar la automatización

Para detener futuros envíos automáticos:

```bash
crontab -e
```

Eliminar únicamente la línea de `enviar-recordatorios`, guardar y verificar:

```bash
crontab -l
```

Quitar el cron no elimina inscripciones, eventos ni registros históricos de la
tabla `correos`.
