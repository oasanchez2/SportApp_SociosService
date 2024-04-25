from .base_command import BaseCommannd
from ..errors.errors import Unauthorized, InvalidParams, ExerciseNotFoundError
from ..dynamodb_producto_servicio import DynamoDbProductoServicio

class GetTodosProductosServicios (BaseCommannd):
  def __init__(self):
    self.db = DynamoDbProductoServicio()
  
  def execute(self):    
    result  = self.db.get_all()
    if result is None:
      raise ExerciseNotFoundError()
    
    return result
