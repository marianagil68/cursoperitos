# Fase 8 - Puesta en producción

## Objetivo

Migrar el plugin desde el entorno Sandbox de Mercado Pago al entorno de Producción y validar el flujo completo con una transacción real.

---

## Configuración realizada

### Moodle

En la configuración de la cuenta de pago Mercado Pago se realizaron los siguientes cambios:

- Environment: Production
- Access Token: reemplazado por el Access Token de producción.
- Webhook Secret: se mantuvo el mismo configurado en Mercado Pago, ya que no fue regenerado.
- Se verificó que el webhook apuntara al entorno de producción.

---

### Mercado Pago

Se confirmó que:

- La aplicación tenía credenciales de producción activas.
- El webhook de producción estaba configurado.
- La URL del webhook era:

https://campus.portalpericial.com.ar/payment/gateway/mercadopago/webhook.php?accountid=1

- El evento "Pagos" estaba habilitado.

---

## Consideración importante

Mercado Pago no permite que la misma cuenta utilizada como vendedor realice pagos sobre sus propias preferencias.

Durante la validación se comprobó que:

- utilizando la misma cuenta el botón "Pagar" permanece deshabilitado;
- la prueba debe realizarse utilizando una cuenta compradora diferente.

---

## Resultado de la prueba

Se realizó una transacción real en producción.

Resultado:

- Checkout Pro abrió correctamente.
- El pago fue aprobado.
- El webhook fue recibido.
- La firma del webhook fue validada correctamente.
- El pago fue confirmado mediante la API de Mercado Pago.
- Moodle registró la transacción.
- El alumno fue matriculado automáticamente.
- El curso quedó disponible inmediatamente luego del pago.

---

## Estado final

Se considera finalizada la implementación del plugin de pago Mercado Pago para Moodle.

Se validó satisfactoriamente el funcionamiento tanto en Sandbox como en Producción.