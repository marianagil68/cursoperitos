import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import make_msgid
from html import escape
from zoneinfo import ZoneInfo

from app.config.config import Config
from app.correos.repository import CorreoRepository
from app.shared.exceptions import ErrorEnvioCorreo
from app.shared.exceptions import ErrorReenvioReciente


class CorreoService:

    ZONA_HORARIA = ZoneInfo(
        "America/Argentina/Buenos_Aires"
    )

    ASUNTO_CONFIRMACION_CHARLA = (
        "Tu lugar está reservado | Portal Pericial"
    )

    ASUNTO_CONFIRMACION_CONSULTA = (
        "Recibimos tu consulta | Portal Pericial"
    )

    ASUNTO_REENVIO_CONFIRMACION_CHARLA = (
        "Reenvío: datos de acceso a la charla | Portal Pericial"
    )

    MINUTOS_ENTRE_REENVIOS = 5

    def __init__(self):
        self.repository = CorreoRepository()

    def enviar(
        self,
        personaid,
        eventoid,
        destinatario,
        asunto,
        html,
        replyto=None
    ):
        correoid = self.repository.crear(
            personaid=personaid,
            eventoid=eventoid,
            remitente=Config.SMTP_REMITENTE,
            destinatario=destinatario,
            asunto=asunto,
            cuerpohtml=html
        )

        mensaje = MIMEMultipart("alternative")
        messageid = make_msgid()

        mensaje["From"] = (
            f"{Config.SMTP_NOMBRE} <{Config.SMTP_REMITENTE}>"
        )
        mensaje["To"] = destinatario
        mensaje["Subject"] = asunto
        mensaje["Message-ID"] = messageid

        if replyto:
            mensaje["Reply-To"] = replyto

        mensaje.attach(
            MIMEText(html, "html", "utf-8")
        )

        servidor = None

        try:
            if Config.SMTP_USAR_SSL:
                servidor = smtplib.SMTP_SSL(
                    Config.SMTP_HOST,
                    Config.SMTP_PORT,
                    timeout=20
                )
            else:
                servidor = smtplib.SMTP(
                    Config.SMTP_HOST,
                    Config.SMTP_PORT,
                    timeout=20
                )

            servidor.ehlo()

            if Config.SMTP_USAR_TLS:
                servidor.starttls()
                servidor.ehlo()

            servidor.login(
                Config.SMTP_USUARIO,
                Config.SMTP_PASSWORD
            )

            servidor.send_message(mensaje)

            self.repository.marcarenviado(
                correoid,
                messageid
            )

            return {
                "correoid": correoid,
                "estado": "ENVIADO"
            }

        except Exception as error:
            self.repository.marcarerror(
                correoid,
                error
            )

            raise ErrorEnvioCorreo(
                "No pudimos enviar el correo de confirmación."
            ) from error

        finally:
            if servidor is not None:
                try:
                    servidor.quit()
                except Exception:
                    pass

    def enviarcorreosinscripcion(self, persona, evento):
        eventoid = evento["eventoid"]
        destinatario = persona["email"]
        asuntoadmin = (
            f"Nueva reserva de charla - "
            f"{persona['nombre']} {persona['apellido']}"
        )

        if not self._fueenviado(
            persona["personaid"],
            eventoid,
            Config.SMTP_DESTINATARIO_ADMIN,
            asuntoadmin
        ):
            self.enviar(
                personaid=persona["personaid"],
                eventoid=eventoid,
                destinatario=Config.SMTP_DESTINATARIO_ADMIN,
                asunto=asuntoadmin,
                html=self._crearhtmlavisoreserva(persona, evento),
                replyto=destinatario
            )

        if not self._fueenviado(
            persona["personaid"],
            eventoid,
            destinatario,
            self.ASUNTO_CONFIRMACION_CHARLA
        ):
            self.enviar(
                personaid=persona["personaid"],
                eventoid=eventoid,
                destinatario=destinatario,
                asunto=self.ASUNTO_CONFIRMACION_CHARLA,
                html=self._crearhtmlconfirmacioncharla(
                    persona,
                    evento
                )
            )

    def reenviarconfirmacioncharla(self, persona, evento):
        eventoid = evento["eventoid"]
        destinatario = persona["email"]
        asunto = self.ASUNTO_REENVIO_CONFIRMACION_CHARLA

        if self.repository.hayenviadoreciente(
            persona["personaid"],
            eventoid,
            destinatario,
            asunto,
            self.MINUTOS_ENTRE_REENVIOS
        ):
            raise ErrorReenvioReciente(
                "Ya solicitaste el reenvío. Revisá tu correo o "
                "intentá nuevamente dentro de unos minutos."
            )

        return self.enviar(
            personaid=persona["personaid"],
            eventoid=eventoid,
            destinatario=destinatario,
            asunto=asunto,
            html=self._crearhtmlconfirmacioncharla(
                persona,
                evento
            )
        )

    def enviarcorreosconsulta(self, persona, consulta):
        destinatario = persona["email"]
        asuntoadmin = (
            f"Nueva consulta desde el sitio - "
            f"{persona['nombre']} {persona['apellido']}"
        )

        self.enviar(
            personaid=persona["personaid"],
            eventoid=None,
            destinatario=Config.SMTP_DESTINATARIO_ADMIN,
            asunto=asuntoadmin,
            html=self._crearhtmlavisoconsulta(
                persona,
                consulta
            ),
            replyto=destinatario
        )

        self.enviar(
            personaid=persona["personaid"],
            eventoid=None,
            destinatario=destinatario,
            asunto=self.ASUNTO_CONFIRMACION_CONSULTA,
            html=self._crearhtmlconfirmacionconsulta(persona)
        )

    def _fueenviado(
        self,
        personaid,
        eventoid,
        destinatario,
        asunto
    ):
        correo = self.repository.obtenerenviado(
            personaid,
            eventoid,
            destinatario,
            asunto
        )

        return correo is not None

    def _crearhtmlavisoreserva(self, persona, evento):
        fecha = self._formatearfecha(evento["fechainicio"])

        return f"""
            <div style="font-family:Arial,sans-serif;color:#10213d;max-width:680px;margin:auto">
                <h2 style="color:#0b2d57">Nueva reserva de charla informativa</h2>
                <p><b>Nombre:</b> {escape(persona['nombre'])} {escape(persona['apellido'])}</p>
                <p><b>Correo:</b> {escape(persona['email'])}</p>
                <p><b>WhatsApp:</b> {escape(persona['whatsapp'] or 'No informado')}</p>
                <p><b>Charla:</b> {escape(evento['titulo'])}</p>
                <p><b>Fecha:</b> {escape(fecha)}</p>
            </div>
        """

    def _crearhtmlconfirmacioncharla(self, persona, evento):
        fecha = self._formatearfecha(evento["fechainicio"])
        urlacceso = evento.get("urlacceso")

        if not isinstance(urlacceso, str) or not urlacceso.strip():
            raise ErrorEnvioCorreo(
                "La charla no tiene configurado un enlace de acceso."
            )

        urlacceso = escape(urlacceso.strip(), quote=True)

        return f"""
            <div style="font-family:Arial,sans-serif;color:#10213d;max-width:680px;margin:auto;border:1px solid #dce3ec;border-radius:14px;overflow:hidden">
                <div style="background:#071a33;color:white;padding:26px;text-align:center">
                    <h1 style="margin:0;font-size:25px">¡Tu lugar quedó reservado!</h1>
                </div>
                <div style="padding:28px">
                    <p>Hola <b>{escape(persona['nombre'])}</b>,</p>
                    <p>Confirmamos tu inscripción a la charla informativa gratuita de Portal Pericial.</p>
                    <div style="background:#f4f7fb;border-left:5px solid #d5a742;padding:18px;margin:20px 0">
                        <b>Encuentro:</b> {escape(evento['titulo'])}<br>
                        <b>Fecha:</b> {escape(fecha)}<br>
                        <b>Modalidad:</b> Online por Zoom<br>
                        <b>Duración:</b> 45 minutos más un espacio para preguntas
                    </div>
                    <p style="text-align:center;margin:28px 0">
                        <a href="{urlacceso}" style="display:inline-block;background:#0b63ce;color:white;text-decoration:none;padding:14px 24px;border-radius:9px;font-weight:bold">INGRESAR A LA CHARLA POR ZOOM</a>
                    </p>
                    <p>Guardá este mensaje para acceder al encuentro.</p>
                    <p style="margin-top:28px">Equipo de <b>Portal Pericial</b></p>
                </div>
            </div>
        """

    def _crearhtmlavisoconsulta(self, persona, consulta):
        consultasegura = escape(consulta).replace("\n", "<br>")

        return f"""
            <div style="font-family:Arial,sans-serif;color:#10213d;max-width:680px;margin:auto">
                <h2 style="color:#0b2d57">Nueva consulta desde el sitio</h2>
                <p><b>Nombre:</b> {escape(persona['nombre'])} {escape(persona['apellido'])}</p>
                <p><b>Correo:</b> {escape(persona['email'])}</p>
                <p><b>WhatsApp:</b> {escape(persona['whatsapp'] or 'No informado')}</p>
                <p><b>Consulta:</b></p>
                <div style="background:#f4f7fb;padding:18px;border-radius:10px">{consultasegura}</div>
            </div>
        """

    def _crearhtmlconfirmacionconsulta(self, persona):
        return f"""
            <div style="font-family:Arial,sans-serif;color:#10213d;max-width:680px;margin:auto;border:1px solid #dce3ec;border-radius:14px;overflow:hidden">
                <div style="background:#071a33;color:white;padding:26px;text-align:center">
                    <h1 style="margin:0;font-size:25px">Recibimos tu consulta</h1>
                </div>
                <div style="padding:28px">
                    <p>Hola <b>{escape(persona['nombre'])}</b>,</p>
                    <p>Gracias por comunicarte con Portal Pericial. Tu consulta fue recibida correctamente y te responderemos a la brevedad.</p>
                    <p style="margin-top:28px">Equipo de <b>Portal Pericial</b></p>
                </div>
            </div>
        """

    def _formatearfecha(self, fecha):
        fecha = fecha.astimezone(self.ZONA_HORARIA)

        dias = (
            "lunes",
            "martes",
            "miércoles",
            "jueves",
            "viernes",
            "sábado",
            "domingo"
        )
        meses = (
            "enero",
            "febrero",
            "marzo",
            "abril",
            "mayo",
            "junio",
            "julio",
            "agosto",
            "septiembre",
            "octubre",
            "noviembre",
            "diciembre"
        )

        return (
            f"{dias[fecha.weekday()]} {fecha.day} de "
            f"{meses[fecha.month - 1]} de {fecha.year} · "
            f"{fecha:%H:%M} hs"
        )
