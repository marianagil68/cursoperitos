# Configuración de correo y autorregistro en Moodle

Fecha: Julio 2026

## Objetivo

Configurar el envío de correos de Moodle utilizando casillas del dominio
`portalpericial.com` y dejar preparado el autorregistro de alumnos.

------------------------------------------------------------------------

# 1. Decisión de infraestructura

Después de evaluar Google Workspace y Zoho, se optó por utilizar el
servicio de correo de DonWeb con un dominio independiente:

-   Dominio web del campus: `campus.portalpericial.com.ar`
-   Dominio de correo: `portalpericial.com`

Esto permitió desacoplar el correo del hosting del sitio.

------------------------------------------------------------------------

# 2. Casillas creadas

Se definió una separación por funciones:

  -----------------------------------------------------------------------
  Casilla                                       Uso
  --------------------------------------------- -------------------------
  `campus.info@portalpericial.com`              Contacto general

  `campus.registro@portalpericial.com`          Autenticación SMTP de
                                                Moodle

  `campus.no-reply@portalpericial.com`          Remitente de mensajes
                                                automáticos

  `campus.soporte@portalpericial.com`           Atención de consultas de
                                                alumnos
												
												
												
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# 3. Configuración SMTP en Moodle

Administración del sitio → Servidor → Correo saliente

Configurar:

-   Host SMTP: servidor Ferozo de DonWeb
-   Puerto SMTP: 465
-   Seguridad: SSL/TLS
-   Usuario SMTP: `campus.registro@portalpericial.com`
-   Contraseña: contraseña de la casilla
-   Dirección No Reply: `campus.no-reply@portalpericial.com`
-   Prefijo del asunto: `[Campus Portal Pericial]`

Guardar cambios.

------------------------------------------------------------------------

# 4. Prueba de correo

Administración del sitio → Servidor → Correo saliente → Probar
configuración.

Completar:

-   Destinatario: dirección de prueba.
-   Remitente: `campus.registro@portalpericial.com`

Resultado:

-   Envío correcto.
-   Gmail recibió correctamente el mensaje.
-   TLS funcionando.
-   SPF/DKIM correctos.

------------------------------------------------------------------------

# 5. Autorregistro

Administración del sitio → Plugins → Identificación → Gestionar
autenticación

Habilitar:

-   Identificación basada en Email.

Luego:

Administración del sitio → Seguridad → Configuración de acceso

En:

**Registrarse a sí mismo**

Seleccionar:

-   Identificación basada en Email.

Se probó creando un usuario nuevo.

Resultado:

-   Moodle creó correctamente la cuenta.
-   Se envió el correo de confirmación.
-   El enlace de activación funcionó correctamente.

------------------------------------------------------------------------

# 6. Personalización del remitente

Configuraciones utilizadas:

Nombre del remitente:

    Soporte Campus Portal Pericial

Dirección No Reply:

    campus.no-reply@portalpericial.com

El correo llega como:

    Soporte Campus Portal Pericial
    <campus.no-reply@portalpericial.com>

------------------------------------------------------------------------

# 7. Contacto de soporte

Administración del sitio → Servidor → Contacto de soporte

Configurar:

-   Nombre: `Soporte Campus Portal Pericial`

-   Email: `campus.soporte@portalpericial.com`

Esto reemplaza el nombre mostrado al final de los mensajes automáticos
de Moodle.

------------------------------------------------------------------------

# 8. Pie de página del tema

Se detectó que el correo del footer no provenía de la configuración de
soporte sino del tema **Trema**.

Ruta:

Administración → Apariencia → Trema → Pie de página

Allí se modificó el HTML del footer reemplazando el correo anterior por
la nueva dirección institucional.

------------------------------------------------------------------------

# 9. Resultado final

Estado alcanzado:

-   SMTP funcionando.
-   Autorregistro funcionando.
-   Confirmación por correo funcionando.
-   Remitente personalizado.
-   No Reply configurado.
-   Soporte separado del SMTP.
-   Footer actualizado con el correo institucional.

La plataforma quedó lista para continuar con la implementación del
plugin de Mercado Pago.
