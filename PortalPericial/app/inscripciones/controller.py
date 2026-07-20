from flask import Blueprint
from flask import current_app
from flask import jsonify
from flask import request

from app.inscripciones.service import InscripcionEventoService
from app.personas.service import PersonaService
from app.shared.exceptions import ErrorEnvioCorreo
from app.shared.exceptions import ErrorReenvioReciente


inscripcionesbp = Blueprint("inscripciones", __name__)

service = InscripcionEventoService()
personaservice = PersonaService()


@inscripcionesbp.route("/api/inscripciones", methods=["POST"])
def registrarinscripcion():
    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({
            "error": "La solicitud debe contener un JSON válido."
        }), 400

    if str(datos.get("_honey") or "").strip():
        return jsonify({
            "mensaje": "Inscripción realizada correctamente.",
            "inscripcioncreada": False,
            "correoenviado": False
        }), 200

    try:
        resultado = personaservice.registrareinscribir(
            datos.get("nombre"),
            datos.get("apellido"),
            datos.get("email"),
            datos.get("telefono"),
            datos.get("whatsapp"),
            datos.get("eventoid")
        )
    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 400
    except LookupError as error:
        return jsonify({
            "error": str(error)
        }), 404
    except ErrorEnvioCorreo as error:
        current_app.logger.exception(
            "No se pudo completar el envío de la inscripción."
        )

        return jsonify({
            "error": str(error)
        }), 503

    estadohttp = 201 if resultado["inscripcioncreada"] else 200

    return jsonify(resultado), estadohttp


@inscripcionesbp.route(
    "/api/inscripciones/reenviar-correo",
    methods=["POST"]
)
def reenviarcorreoinscripcion():
    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({
            "error": "La solicitud debe contener un JSON válido."
        }), 400

    if str(datos.get("_honey") or "").strip():
        return jsonify({
            "correoenviado": True,
            "mensaje": "Te reenviamos el correo con los datos de acceso."
        }), 200

    try:
        resultado = personaservice.reenviarcorreoinscripcion(
            datos.get("email"),
            datos.get("eventoid")
        )
    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 400
    except LookupError as error:
        return jsonify({
            "error": str(error)
        }), 404
    except ErrorReenvioReciente as error:
        return jsonify({
            "error": str(error)
        }), 429
    except ErrorEnvioCorreo as error:
        current_app.logger.exception(
            "No se pudo completar el reenvío de la inscripción."
        )

        return jsonify({
            "error": str(error)
        }), 503

    return jsonify(resultado), 200


@inscripcionesbp.route("/inscripciones/<int:personaid>/<int:eventoid>", methods=["POST"])
def inscribir(personaid, eventoid):

    inscripcioneventoid = service.inscribir(
        personaid,
        eventoid
    )

    return jsonify(
        {
            "inscripcioneventoid": inscripcioneventoid,
            "mensaje": "Inscripción realizada correctamente."
        }
    )
