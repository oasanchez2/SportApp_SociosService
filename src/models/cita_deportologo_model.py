from dataclasses import dataclass
from datetime import datetime
from typing import List
from enum import Enum

    
class TipoAgenda(Enum):
    Presencial = "Presencial"
    Virtual = "Virtual"

@dataclass
class CitasDeportologoModel:
    id_cita_deportologo: str
    id_deportologo : str
    id_deportista : str
    fecha_cita: datetime
    tipo_agenda: TipoAgenda