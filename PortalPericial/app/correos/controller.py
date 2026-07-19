from flask import Blueprint, jsonify

from app.correos.service import CorreoService


correosbp = Blueprint("correos", __name__)

service = CorreoService()

@correosbp.route("/correos/prueba", methods=["GET"])
def correoprueba():

    correoid = service.enviar(
        personaid=1,
        eventoid=1,
        destinatario="yerard30@gmail.com",
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