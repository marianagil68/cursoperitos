from flask import Blueprint, jsonify

from app.eventos.service import EventoService

eventosbp = Blueprint("eventos", __name__)

service = EventoService()


@eventosbp.route("/api/eventos", methods=["GET"])
def obtenereventos():
    eventos = service.obtenerpublicosproximos()

    return jsonify(eventos)


@eventosbp.route("/api/eventos/<int:eventoid>", methods=["GET"])
def obtenerevento(eventoid):
    evento = service.obtenerpublicoporid(eventoid)

    if evento is None:
        return jsonify({
            "error": "Evento no encontrado."
        }), 404

    return jsonify(evento)
