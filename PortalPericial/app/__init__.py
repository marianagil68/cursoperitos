from flask import Flask, request

from app.config.config import Config
from app.consultas.controller import consultasbp
from app.eventos.controller import eventosbp
from app.personas.controller import personasbp
from app.inscripciones.controller import inscripcionesbp
from app.correos.controller import correosbp

def createapp():
    app = Flask(__name__)
    app.config.from_object(Config)

    origenesdesarrollopermitidos = {
        "http://127.0.0.1:8080",
        "http://localhost:8080"
    }

    @app.after_request
    def habilitarcorsdesarrollo(respuesta):
        origen = request.headers.get("Origin")

        if app.debug and origen in origenesdesarrollopermitidos:
            respuesta.headers["Access-Control-Allow-Origin"] = origen
            respuesta.headers["Access-Control-Allow-Headers"] = "Content-Type"
            respuesta.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
            respuesta.headers["Vary"] = "Origin"

        return respuesta

    app.register_blueprint(eventosbp)
    app.register_blueprint(personasbp)
    app.register_blueprint(inscripcionesbp)
    app.register_blueprint(correosbp)
    app.register_blueprint(consultasbp)
    
    return app
