from app.correos.service import CorreoService
from app.personas.service import PersonaService


class ConsultaService:

    def __init__(self):
        self.personaservice = PersonaService()
        self.correoservice = CorreoService()

    def registrar(
        self,
        nombrecompleto,
        email,
        whatsapp,
        consulta
    ):
        nombre, apellido = self._separarnombre(nombrecompleto)
        consulta = self._normalizarconsulta(consulta)

        persona = self.personaservice.crear(
            nombre=nombre,
            apellido=apellido,
            email=email,
            whatsapp=whatsapp,
            origen="CONSULTA"
        )

        self.correoservice.enviarcorreosconsulta(
            persona,
            consulta
        )

        return {
            "mensaje": "Consulta enviada correctamente.",
            "correoenviado": True
        }

    def _separarnombre(self, nombrecompleto):
        if not isinstance(nombrecompleto, str):
            raise ValueError(
                "El nombre y apellido son obligatorios."
            )

        partes = nombrecompleto.strip().split()

        if len(partes) < 2:
            raise ValueError(
                "Ingresá tu nombre y apellido."
            )

        nombre = " ".join(partes[:-1])
        apellido = partes[-1]

        return nombre, apellido

    def _normalizarconsulta(self, consulta):
        if not isinstance(consulta, str):
            raise ValueError("La consulta es obligatoria.")

        consulta = consulta.strip()

        if not consulta:
            raise ValueError("La consulta es obligatoria.")

        if len(consulta) > 1800:
            raise ValueError(
                "La consulta no puede superar los 1800 caracteres."
            )

        return consulta
