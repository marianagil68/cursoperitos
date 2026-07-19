from app.eventos.repository import EventoRepository


class EventoService:

    def __init__(self):
        self.repository = EventoRepository()

    def obtenertodos(self):
        return self.repository.obtenertodos()

    def obtenerpublicosproximos(self):
        return self.repository.obtenerpublicosproximos()
    
    def obtenerporid(self, eventoid):
        return self.repository.obtenerporid(eventoid)