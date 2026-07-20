import os

from dotenv import load_dotenv


load_dotenv()


class Config:

    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = int(os.getenv("DB_PORT", 5432))
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    SMTP_HOST = os.getenv("SMTP_HOST")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
    SMTP_USUARIO = os.getenv("SMTP_USUARIO")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    SMTP_REMITENTE = os.getenv("SMTP_REMITENTE")
    SMTP_NOMBRE = os.getenv("SMTP_NOMBRE", "Portal Pericial")
    SMTP_DESTINATARIO_ADMIN = os.getenv(
        "SMTP_DESTINATARIO_ADMIN",
        SMTP_REMITENTE
    )

    SMTP_USAR_TLS = (
        os.getenv("SMTP_USAR_TLS", "false").lower() == "true"
    )

    SMTP_USAR_SSL = (
        os.getenv("SMTP_USAR_SSL", "true").lower() == "true"
    )
