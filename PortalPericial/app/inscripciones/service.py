from app.inscripciones.repository import InscripcionEventoRepository


class InscripcionEventoService:

    def __init__(self):
        self.repository = InscripcionEventoRepository()

    def obtener(self, personaid, eventoid):

        return self.repository.obtener(personaid, eventoid)

    def inscribir(
        self,
        personaid,
        eventoid,
        observaciones=None
    ):

        inscripcion = self.repository.obtener(
            personaid,
            eventoid
        )

        if inscripcion is not None:
            return inscripcion["inscripcioneventoid"]

        return self.repository.insertar(
            personaid,
            eventoid,
            "INSCRIPTO",
            observaciones
        )

    def cambiarestado(
        self,
        personaid,
        eventoid,
        estado
    ):

        self.repository.actualizarestado(
            personaid,
            eventoid,
            estado
        )