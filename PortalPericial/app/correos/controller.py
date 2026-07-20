from flask import abort
from flask import Blueprint
from flask import current_app
from flask import jsonify

from app.config.config import Config
from app.correos.service import CorreoService


correosbp = Blueprint("correos", __name__)

service = CorreoService()

@correosbp.route("/correos/prueba", methods=["GET"])
def correoprueba():

    if not current_app.debug:
        abort(404)

    correoid = service.enviar(
        personaid=1,
        eventoid=1,
        destinatario=Config.SMTP_DESTINATARIO_ADMIN,
        asunto="Prueba Portal Pericial",
        html="""
        <html>
            <body>
                <h2>Portal Pericial</h2>
                    <p>Si estás leyendo este correo, la configuración SMTP funciona correctamente.<p>

                    <p>Este correo fue enviado desde Portal Pericial.<p>
                    <p>Inscripción a la charla de Peritos 2026.<p>
            </body>
        </html>
        """
    )

    return jsonify({
        "ok": True,
        "correoid": correoid
    })
