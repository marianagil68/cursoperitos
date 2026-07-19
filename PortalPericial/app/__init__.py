from flask import Flask

from app.config.config import Config
from app.eventos.controller import eventosbp
from app.personas.controller import personasbp
from app.inscripciones.controller import inscripcionesbp
from app.correos.controller import correosbp

def createapp():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(eventosbp)
    app.register_blueprint(personasbp)
    app.register_blueprint(inscripcionesbp)
    app.register_blueprint(correosbp)
    
    return app