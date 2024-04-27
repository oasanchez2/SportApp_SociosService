from .base_command import BaseCommannd
from ..errors.errors import Unauthorized, InvalidParams, ExerciseNotFoundError
from ..dynamodb_socio import DynamoDbSocio

class GetAllsSocios (BaseCommannd):
  def __init__(self):
    self.db = DynamoDbSocio()
  
  def execute(self):    
    result  = self.db.get_all()
   
    return result