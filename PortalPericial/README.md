# Recordatorios automáticos de charlas

La explicación técnica y operativa completa se encuentra en
`../portalpericial-docs/Arquitectura/11-recordatorios-automaticos-correo.md`.

El backend puede enviar, mediante el SMTP profesional configurado, un correo
individual a cada persona inscripta y activa aproximadamente 24 horas antes de
la charla. El correo vuelve a incluir la fecha y el enlace privado de Zoom.

Ejecutar manualmente desde `PortalPericial`:

```bash
flask --app run:app enviar-recordatorios
```

Antes de habilitar el envío real, consultar los eventos y destinatarios sin
conectarse al SMTP:

```bash
flask --app run:app enviar-recordatorios --simular
```

Para enviar como máximo un mensaje de prueba por evento, únicamente a una
dirección controlada:

```bash
flask --app run:app enviar-recordatorios --evento-id 1 --destinatario-prueba correo@ejemplo.com --nombre-prueba Mariana
```

El correo de prueba lleva un asunto y un aviso visibles de prueba, no se asocia
al participante utilizado para personalizarlo y nunca se envía más de uno por
evento en cada ejecución.

`--evento-id` evita depender de la ventana de 24 horas y limita tanto la
simulación como la prueba al evento seleccionado.

La ventana predeterminada incluye eventos que comienzan entre 23 horas y
30 minutos y 24 horas y 30 minutos después de la ejecución. Cada recordatorio
enviado queda registrado en `correos`, por lo que una nueva ejecución lo omite.

Para una charla el sábado a las 10:00, configurar en el servidor este `cron`
para ejecutar la revisión todos los días a las 10:00:

```cron
0 10 * * * /usr/bin/flock -n /home/portalpericial-curso/recordatorios.lock /bin/bash -c 'cd /home/portalpericial-curso/apps/CursoPeritos/PortalPericial && exec .venv/bin/python -m flask --app run:app enviar-recordatorios' >> /home/portalpericial-curso/logs/recordatorios.log 2>&1
```

El cron pertenece al usuario `portalpericial-curso`. El servidor usa la zona
horaria `America/Argentina/Buenos_Aires` y el servicio utiliza el entorno
virtual `PortalPericial/.venv`.
