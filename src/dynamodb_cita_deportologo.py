import boto3
import os
import json
from boto3.dynamodb.conditions import Key, Attr
from .models.cita_deportologo_model import CitasDeportologoModel
from botocore.exceptions import ClientError

class DynamoDbInterface:
    def create_table(self):
        raise NotImplementedError
    
    def insert_item(self, cita_deportologo: CitasDeportologoModel):
        raise NotImplementedError
    
    def get_item(self, id_cita_deportologo):
        raise NotImplementedError
    
    def get_Item_nombre(self,nombre):
        raise NotImplementedError
    
    def get_all(self):
        raise NotImplementedError

    def tablaExits(self,name):
        raise NotImplementedError
    
    def deleteTable(self):
        raise NotImplementedError    
       
    
class DynamoDbCitasDeportologo(DynamoDbInterface):
    def __init__(self,dynamodb=None):
        # Crear una instancia de cliente DynamoDB
        if dynamodb is None:
            self.dynamodb = boto3.client('dynamodb',
                                    region_name='us-east-1',
                                    aws_access_key_id= os.environ['AWS_ACCESS_KEY_ID'],
                                    aws_secret_access_key= os.environ['AWS_SECRET_ACCESS_KEY'])
        else:
            self.dynamodb = dynamodb
        
        self.table_name = 'citas-deportologo'

    # Funciones para interactuar con DynamoDB

    def create_table(self):
        if not self.tablaExits(self.table_name):

            self.dynamodb.create_table(
                    TableName=self.table_name,
                    AttributeDefinitions=[
                        {
                            'AttributeName': 'id_cita_deportologo',
                            'AttributeType': 'S',
                        }
                    ],
                    KeySchema=[
                        {
                            'AttributeName': 'id_cita_deportologo',
                            'KeyType': 'HASH'  # Clave de partición
                        }
                    ],        
                    BillingMode='PAY_PER_REQUEST'
                )
            
            # Espera hasta que la tabla exista
            self.dynamodb.get_waiter('table_exists').wait(TableName=self.table_name)
            print(f'Tabla {self.table_name} creada correctamente.')
        else:
            print(f"La tabla '{self.table_name}' ya existe.")

    def insert_item(self,cita_deportologo: CitasDeportologoModel):
        item = {
            'id_cita_deportologo': {'S':  cita_deportologo.id_cita_deportologo },
            'id_deportologo': {'S': cita_deportologo.id_deportologo },
            'id_deportista': {'S': cita_deportologo.id_deportista},
            'fecha_cita': {'S': str(cita_deportologo.fecha_cita) }, # Revisar si es necesario convertir a string
            'tipo_agenda': {'S': cita_deportologo.tipo_agenda}  
            # Puedes agregar más atributos según la definición de tu tabla
        }
        result = self.dynamodb.put_item(
            TableName=self.table_name,
            Item=item,
            ReturnConsumedCapacity='TOTAL'
        )
        print('Ítem insertado correctamente.')

    def get_item(self,id_cita_deportologo):
        key = {
            'id_producto_servicio': {'S': id_cita_deportologo }  # Clave de búsqueda
        }
        response = self.dynamodb.get_item(
            TableName=self.table_name,
            Key=key
        )
        item = response.get('Item')
        if not item:
            return None

        # Extrae los valores de cada campo
        id_cita_deportologo = item['id_cita_deportologo']['S']
        id_deportologo = item['id_deportologo']['S']
        id_deportista = item['id_deportista']['S']
        fecha_cita = item['fecha_cita']['S']
        tipo_agenda = item['tipo_agenda']['S']
        
        # Crea una instancia de la clase Entrenamiento
        cita_deportologo = CitasDeportologoModel(id_cita_deportologo,id_deportologo,id_deportista,fecha_cita,tipo_agenda)

        # Devuelve el objeto como diccionario
        return cita_deportologo

    def cita_existe_deportista(self,id_deportista, fecha_cita):
        
        # Parámetros para la operación de escaneo
        parametros = {
            'TableName': self.table_name,
            'FilterExpression': '#id_deportista = :id_deportista AND #fecha_cita = :fecha_cita',
            'ExpressionAttributeNames': {
                '#id_deportista': 'id_deportista',
                '#fecha_cita': 'fecha_cita' 
            },
            'ExpressionAttributeValues': {
                ':id_deportista': {'S': id_deportista},
                ':fecha_cita': {'S': fecha_cita}
            }
        }
        
        # Realizar el escaneo
        response = self.dynamodb.scan(**parametros)
        print(response)
        # Obtener los items encontrados
        items = response.get('Items', [])
        if not items:
            return None
        
        # Procesar los items encontrados
        resultados = []
        for item in items:
            id_cita_deportologo = item['id_cita_deportologo']['S']
            id_deportologo = item['id_deportologo']['S']
            id_deportista = item['id_deportista']['S']
            fecha_cita = item['fecha_cita']['S']
            tipo_agenda = item['tipo_agenda']['S']

            cita_deportologo = CitasDeportologoModel(id_cita_deportologo,id_deportologo,id_deportista,fecha_cita,tipo_agenda)
            resultados.append(cita_deportologo)

        return resultados

    
    def tablaExits(self,name):
        try:
            response = self.dynamodb.describe_table(TableName=name)
            print(response)
            return True
        except ClientError as err:
            print(f"Here's why: {err.response['Error']['Code']}: {err.response['Error']['Message']}")
            if err.response['Error']['Code'] == 'ResourceNotFoundException':
                return False

    def deleteTable(self):
        # Eliminar la tabla
        self.dynamodb.delete_table(TableName=self.table_name)

        # Esperar hasta que la tabla no exista
        self.dynamodb.get_waiter('table_not_exists').wait(TableName=self.table_name)