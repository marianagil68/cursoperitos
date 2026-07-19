from flask import Blueprint, jsonify

from app.eventos.service import EventoService

eventosbp = Blueprint("eventos", __name__)

service = EventoService()


@eventosbp.route("/eventos", methods=["GET"])
def obtenereventos():
    eventos = service.obtenerpublicosproximos()
    return jsonify(eventos)