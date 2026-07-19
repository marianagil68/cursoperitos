from flask import Blueprint
from flask import jsonify

from app.inscripciones.service import InscripcionEventoService


inscripcionesbp = Blueprint("inscripciones", __name__)

service = InscripcionEventoService()


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