import uuid
from .base_command import BaseCommannd
from ..models.producto_servicio_model import ProductoServicioModel
from ..errors.errors import IncompleteParams, InvalidNombreError, ProductAlreadyExists
from ..dynamodb_producto_servicio import DynamoDbProductoServicio

class CreateProductoServicio(BaseCommannd):
  
  def __init__(self, data):
    self.data = data
    self.db = DynamoDbProductoServicio()
  
  def execute(self):
    try:

      posted_producto_servicio = ProductoServicioModel(str(uuid.uuid4()), self.data["id_socio"], self.data['nombre'],
                                                 self.data['descripcion'],self.data['costo'],self.data['tipo_oferta'])
      
      print(posted_producto_servicio)
      
      if not self.verificar_datos(self.data['nombre']):
         raise InvalidNombreError
      
      if self.exercise_exist(self.data['nombre']):
        raise ProductAlreadyExists()
      
      self.db.insert_item(posted_producto_servicio)
      
      return posted_producto_servicio
        
    except TypeError as te:
      print("Error en el primer try:", str(te))
      raise IncompleteParams()
  
  def exercise_exist(self, nombre):
    result = self.db.get_Item_nombre(nombre)
    if result is None:
      return False
    else:
      return True
  
  def verificar_datos(self,nombre):
    if nombre and nombre.strip():
        return True
    else:
        return False