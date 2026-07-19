from flask import Blueprint
from flask import jsonify
from flask import request

from app.personas.service import PersonaService


personasbp = Blueprint("personas", __name__)

service = PersonaService() 


@personasbp.route("/personas/registrar", methods=["POST"])
def registrar():

    datos = request.get_json()

    resultado = service.registrareinscribir(
        datos["nombre"],
        datos["apellido"],
        datos["email"],
        datos.get("telefono"),
        datos.get("whatsapp"),
        datos["eventoid"]
    )

    return jsonify(resultado), 201