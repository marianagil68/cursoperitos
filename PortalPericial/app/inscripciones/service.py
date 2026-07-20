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
        resultado = self.inscribirconresultado(
            personaid,
            eventoid,
            observaciones
        )

        return resultado["inscripcioneventoid"]

    def inscribirconresultado(
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
            return {
                "inscripcioneventoid": inscripcion["inscripcioneventoid"],
                "inscripcioncreada": False
            }

        inscripcioneventoid = self.repository.insertar(
            personaid,
            eventoid,
            "INSCRIPTO",
            observaciones
        )

        if inscripcioneventoid is not None:
            return {
                "inscripcioneventoid": inscripcioneventoid,
                "inscripcioncreada": True
            }

        inscripcion = self.repository.obtener(
            personaid,
            eventoid
        )

        return {
            "inscripcioneventoid": inscripcion["inscripcioneventoid"],
            "inscripcioncreada": False
        }

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
