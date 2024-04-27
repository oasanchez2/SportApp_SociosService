from .base_command import BaseCommannd
from ..errors.errors import Unauthorized, InvalidParams, SocioNotFoundError
from ..dynamodb_socio import DynamoDbSocio

class GetSocio (BaseCommannd):
  def __init__(self, id_socio):
    if id_socio and id_socio.strip():
      self.id_socio = id_socio
    else:
      raise InvalidParams()
    
    self.db = DynamoDbSocio()
  
  def execute(self):
    
    result  = self.db.get_item(self.id_socio)
    if result is None:
      raise SocioNotFoundError()
    
    return result