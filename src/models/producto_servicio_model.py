from dataclasses import dataclass
from datetime import datetime
from typing import List
from enum import Enum

    
class TipoOferta(Enum):
    SERVICIO = "Servicio"
    PRODUCTO = "Producto"

@dataclass
class ProductoServicioModel:
    id_producto_servicio: str
    id_socio : str
    nombre: str
    descripcion: str
    costo: int
    tipo_oferta: TipoOferta
