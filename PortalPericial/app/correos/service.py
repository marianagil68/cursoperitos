import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.config.config import Config
from app.correos.repository import CorreoRepository


class CorreoService:

    def __init__(self):
        self.repository = CorreoRepository()

    def enviar(
        self,
        personaid,
        eventoid,
        destinatario,
        asunto,
        html
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

        mensaje["From"] = (
            f"{Config.SMTP_NOMBRE} <{Config.SMTP_REMITENTE}>"
        )

        mensaje["To"] = destinatario
        mensaje["Subject"] = asunto

        mensaje.attach(
            MIMEText(html, "html", "utf-8")
        )

        if Config.SMTP_USAR_SSL:
            servidor = smtplib.SMTP_SSL(
                Config.SMTP_HOST,
                Config.SMTP_PORT
            )
        else:
            servidor = smtplib.SMTP(
                Config.SMTP_HOST,
                Config.SMTP_PORT
            )

        try:

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
                correoid
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

            raise

        finally:

            servidor.quit()