import uuid
from .base_command import BaseCommannd
from ..models.cita_deportologo_model import CitasDeportologoModel
from ..errors.errors import IncompleteParams, InvaliDeportistaError, CitaAlreadyExists
from ..dynamodb_cita_deportologo import DynamoDbCitasDeportologo

class CreateCitaDeportologo(BaseCommannd):
  
  def __init__(self, data):
    self.data = data
    self.db = DynamoDbCitasDeportologo()
  
  def execute(self):
    try:

      posted_cita_deportologo = CitasDeportologoModel(str(uuid.uuid4()), "01fb6f33-762f-4110-a36b-b7d88de0e59e", self.data["id_deportista"], self.data['fecha_cita'],
                                                 self.data['tipo_agenda'])
      
      print(posted_cita_deportologo)
      
      if not self.verificar_datos(self.data['id_deportista']):
         raise InvaliDeportistaError
      
      if self.cita_exist(self.data["id_deportista"], self.data['fecha_cita']):
        raise CitaAlreadyExists()
      
      self.db.insert_item(posted_cita_deportologo)
      
      return posted_cita_deportologo
        
    except TypeError as te:
      print("Error en el primer try:", str(te))
      raise IncompleteParams()
  
  def cita_exist(self, id_deportista, fecha_cita):
    result = self.db.cita_existe_deportista(id_deportista, fecha_cita)
    if result is None:
      return False
    else:
      return True
  
  def verificar_datos(self,id_deportista):
    if id_deportista and id_deportista.strip():
        return True
    else:
        return False