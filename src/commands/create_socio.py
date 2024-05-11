import uuid
from .base_command import BaseCommannd
from ..models.socio_model import SocioModel
from ..errors.errors import IncompleteParams, InvalidNameSocioError, SocioAlreadyExists
from ..dynamodb_socio import DynamoDbSocio
from datetime import datetime

class CreateSocio(BaseCommannd):
  
  def __init__(self, data):
    self.data = data
    self.db = DynamoDbSocio()
  
  def execute(self):
    try:

      posted_socio = SocioModel(self.data["id_usuario"], self.data["nombre"], self.data["apellido"],self.data["especialidad"] ,self.data["anios_experiencia"],self.data["genero"],
                                            self.data['telefono'], self.data['tipo_identificacion'], self.data['numero_identificacion'], self.data['numero_tarjeta_profesional'],
                                            self.data['pais_recidencia'], self.data['ciudad_recidencia'], self.data['organizador'], datetime.now())
      
      print(posted_socio)
      
      if not self.verificar_datos(self.data['nombre']):
         raise InvalidNameSocioError
      
      if self.socio_exist(self.data['id_usuario']):
        raise SocioAlreadyExists()
      
      self.db.insert_item(posted_socio)
      
      return posted_socio
        
    except TypeError as te:
      print("Error en el primer try:", str(te))
      raise IncompleteParams()
  
  def socio_exist(self, id_usuario):
    result = self.db.get_item(id_usuario)
    if result is None:
      return False
    else:
      return True
  
  def verificar_datos(self,nombre):
    if nombre and nombre.strip():
        return True
    else:
        return False