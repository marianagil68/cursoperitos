from dataclasses import dataclass
from datetime import datetime


@dataclass
class PersonaDto:

    personaid: int | None = None

    nombre: str = ""
    apellido: str = ""

    email: str = ""
    telefono: str | None = None
    whatsapp: str | None = None

    emailvalidado: bool = False

    fechaultimoacceso: datetime | None = None

    origen: str = "WEB"

    activo: bool = True

    fechacreacion: datetime | None = None
    fechaactualizacion: datetime | None = None