from flask import Blueprint, current_app, jsonify, request

from app.consultas.service import ConsultaService
from app.shared.exceptions import ErrorEnvioCorreo


consultasbp = Blueprint("consultas", __name__)

service = ConsultaService()


@consultasbp.route("/api/consultas", methods=["POST"])
def registrarconsulta():
    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({
            "error": "La solicitud debe contener un JSON válido."
        }), 400

    if datos.get("_honey"):
        return jsonify({
            "mensaje": "Consulta enviada correctamente.",
            "correoenviado": True
        })

    try:
        resultado = service.registrar(
            datos.get("nombrecompleto"),
            datos.get("email"),
            datos.get("whatsapp"),
            datos.get("consulta")
        )
    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 400
    except ErrorEnvioCorreo as error:
        current_app.logger.exception(
            "No se pudo completar el envío de la consulta."
        )

        return jsonify({
            "error": str(error)
        }), 503

    return jsonify(resultado), 201
