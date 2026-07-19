from flask import Flask

from app.config.config import Config
from app.eventos.controller import eventosbp


def createapp():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(eventosbp)

    return app