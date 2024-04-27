from dataclasses import dataclass
from datetime import datetime
from typing import List
from enum import Enum

class Especialidad(Enum):
    Nutricion = "Nutricion"
    Deportologo = "Deportologo"
    Entrenador = "Entrenador"

class Genero(Enum):
    FEMENINO = "Femenino"
    MASCULINO = "Masculino"

class TipoIdentificacion(Enum):
    CedulaCiudadania = "Cédula de ciudadanía"
    TarjetaIdentidad = "Tarjeta de identidad"
    CedulaExtrangeria = "Cédula de extranjería"
    Pasaporte = "Pasaporte"
    NIT = "NIT"

@dataclass
class SocioModel:
    id_usuario: str
    nombre: str
    apellido: str    
    especialidad: Especialidad
    genero: Genero
    telefono: str
    tipo_identificacion: TipoIdentificacion
    numero_identificacion: str    
    numero_tarjeta_profesional: str
    pais_recidencia: str
    ciudad_recidencia: str
    organizador: bool
    fecha_creacion: datetime
