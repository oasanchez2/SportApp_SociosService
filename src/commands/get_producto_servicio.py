from .base_command import BaseCommannd
from ..errors.errors import Unauthorized, InvalidParams, ExerciseNotFoundError
from ..dynamodb_producto_servicio import DynamoDbProductoServicio

class GetProductoServicio (BaseCommannd):
  def __init__(self, id_producto_servicio):
    if id_producto_servicio and id_producto_servicio.strip():
      self.id_producto_servicio = id_producto_servicio
    else:
      raise InvalidParams()
    
    self.db = DynamoDbProductoServicio()
  
  def execute(self):
    
    result  = self.db.get_item(self.id_producto_servicio)
    if result is None:
      raise ExerciseNotFoundError()
    
    return result