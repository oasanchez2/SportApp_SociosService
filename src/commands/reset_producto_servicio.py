from .base_command import BaseCommannd
from ..dynamodb_producto_servicio import DynamoDbProductoServicio

class ResetProductoServicio(BaseCommannd):  
  def __init__(self):
    self.db = DynamoDbProductoServicio()

  def execute(self):
    self.db.deleteTable()
    self.db.create_table()