from dataclasses import dataclass
from datetime import datetime


@dataclass
class InscripcionEventoDto:

    inscripcioneventoid: int | None = None

    personaid: int = 0

    eventoid: int = 0

    estado: str = "INSCRIPTO"

    observaciones: str | None = None

    fechainscripcion: datetime | None = None

    fechaactualizacion: datetime | None = None