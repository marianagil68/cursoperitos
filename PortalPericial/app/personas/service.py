from app.inscripciones.service import InscripcionEventoService
from app.personas.repository import PersonaRepository


class PersonaService:

    def __init__(self):
        self.repository = PersonaRepository()
        self.inscripcioneservice = InscripcionEventoService()

    def obtenerporid(self, personaid):
        return self.repository.obtenerporid(personaid)

    def obtenerporemail(self, email):
        return self.repository.obtenerporemail(email)

    def crear(
        self,
        nombre,
        apellido,
        email,
        telefono=None,
        whatsapp=None,
        origen="WEB"
    ):
        persona = self.repository.obtenerporemail(email)

        if persona is not None:
            return persona

        personaid = self.repository.insertar(
            nombre,
            apellido,
            email,
            telefono,
            whatsapp,
            origen
        )

        return self.repository.obtenerporid(personaid)

    def registrarultimoacceso(self, personaid):
        self.repository.actualizarultimoacceso(personaid)

    def registrareinscribir(
        self,
        nombre,
        apellido,
        email,
        telefono,
        whatsapp,
        eventoid
    ):
        persona = self.crear(
            nombre,
            apellido,
            email,
            telefono,
            whatsapp
        )

        inscripcioneventoid = self.inscripcioneservice.inscribir(
            persona["personaid"],
            eventoid
        )

        return {
            "persona": persona,
            "inscripcioneventoid": inscripcioneventoid
        }