from .base_command import BaseCommannd
from ..dynamodb_socio import DynamoDbSocio

class ResetSocio(BaseCommannd):  
  def __init__(self):
    self.db = DynamoDbSocio()

  def execute(self):
    self.db.deleteTable()
    self.db.create_table()