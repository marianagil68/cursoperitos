import re

from app.correos.service import CorreoService
from app.eventos.service import EventoService
from app.inscripciones.service import InscripcionEventoService
from app.personas.repository import PersonaRepository


class PersonaService:

    def __init__(self):
        self.repository = PersonaRepository()
        self.correoservice = CorreoService()
        self.eventoservice = EventoService()
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
        nombre = self._normalizartexto(nombre, "nombre", 100)
        apellido = self._normalizartexto(apellido, "apellido", 100)
        email = self._normalizaremail(email)
        telefono = self._normalizaropcional(telefono, "teléfono", 30)
        whatsapp = self._normalizaropcional(whatsapp, "WhatsApp", 30)

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

        if personaid is None:
            return self.repository.obtenerporemail(email)

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
        if isinstance(eventoid, bool) or not isinstance(eventoid, int) or eventoid <= 0:
            raise ValueError("El evento seleccionado no es válido.")

        eventopublico = self.eventoservice.obtenerpublicoporid(eventoid)

        if eventopublico is None:
            raise LookupError("La charla seleccionada no está disponible.")

        evento = self.eventoservice.obtenerporid(eventoid)

        persona = self.crear(
            nombre,
            apellido,
            email,
            telefono,
            whatsapp,
            origen="CHARLA"
        )

        inscripcion = self.inscripcioneservice.inscribirconresultado(
            persona["personaid"],
            eventoid
        )

        self.correoservice.enviarcorreosinscripcion(
            persona,
            evento
        )

        return {
            "inscripcioneventoid": inscripcion["inscripcioneventoid"],
            "inscripcioncreada": inscripcion["inscripcioncreada"],
            "correoenviado": True,
            "mensaje": (
                "Inscripción realizada correctamente."
                if inscripcion["inscripcioncreada"]
                else "Ya estabas inscripto en esta charla."
            )
        }

    def reenviarcorreoinscripcion(self, email, eventoid):
        if isinstance(eventoid, bool) or not isinstance(eventoid, int) or eventoid <= 0:
            raise ValueError("El evento seleccionado no es válido.")

        email = self._normalizaremail(email)
        persona = self.repository.obtenerporemail(email)

        if persona is None:
            raise LookupError(
                "No encontramos una inscripción para ese correo y esa charla."
            )

        inscripcion = self.inscripcioneservice.obtener(
            persona["personaid"],
            eventoid
        )

        if inscripcion is None:
            raise LookupError(
                "No encontramos una inscripción para ese correo y esa charla."
            )

        eventopublico = self.eventoservice.obtenerpublicoporid(eventoid)

        if eventopublico is None:
            raise LookupError("La charla seleccionada no está disponible.")

        evento = self.eventoservice.obtenerporid(eventoid)

        self.correoservice.reenviarconfirmacioncharla(
            persona,
            evento
        )

        return {
            "correoenviado": True,
            "mensaje": "Te reenviamos el correo con los datos de acceso."
        }

    def _normalizartexto(self, valor, campo, longitudmaxima):
        if not isinstance(valor, str):
            raise ValueError(f"El campo {campo} es obligatorio.")

        valor = valor.strip()

        if not valor:
            raise ValueError(f"El campo {campo} es obligatorio.")

        if len(valor) > longitudmaxima:
            raise ValueError(
                f"El campo {campo} no puede superar los {longitudmaxima} caracteres."
            )

        return valor

    def _normalizaremail(self, email):
        email = self._normalizartexto(email, "email", 255).lower()

        if re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email) is None:
            raise ValueError("El correo electrónico no es válido.")

        return email

    def _normalizaropcional(self, valor, campo, longitudmaxima):
        if valor is None:
            return None

        if not isinstance(valor, str):
            raise ValueError(f"El campo {campo} no es válido.")

        valor = valor.strip()

        if not valor:
            return None

        if len(valor) > longitudmaxima:
            raise ValueError(
                f"El campo {campo} no puede superar los {longitudmaxima} caracteres."
            )

        return valor
