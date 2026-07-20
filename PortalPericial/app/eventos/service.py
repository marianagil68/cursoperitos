from app.eventos.repository import EventoRepository


class EventoService:

    def __init__(self):
        self.repository = EventoRepository()

    def obtenertodos(self):
        return self.repository.obtenertodos()

    def obtenerpublicosproximos(self):
        eventos = self.repository.obtenerpublicosproximos()

        return [
            self._convertirapublico(evento)
            for evento in eventos
        ]

    def obtenerpublicoporid(self, eventoid):
        evento = self.repository.obtenerpublicoporid(eventoid)

        if evento is None:
            return None

        return self._convertirapublico(evento)

    def obtenerporid(self, eventoid):
        return self.repository.obtenerporid(eventoid)

    def _convertirapublico(self, evento):
        return {
            "eventoid": evento["eventoid"],
            "titulo": evento["titulo"],
            "slug": evento["slug"],
            "descripcion": evento["descripcion"],
            "fechainicio": evento["fechainicio"].isoformat(),
            "fechafin": evento["fechafin"].isoformat(),
            "capacidad": evento["capacidad"]
        }
