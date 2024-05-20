import boto3
import os
import json
from boto3.dynamodb.conditions import Key, Attr
from .models.socio_model import SocioModel
from botocore.exceptions import ClientError

class DynamoDbInterface:
    def create_table(self):
        raise NotImplementedError
    
    def insert_item(self,socio: SocioModel):
        raise NotImplementedError
    
    def get_item(self,id_socio):
        raise NotImplementedError
  
    def tablaExits(self,name):
        raise NotImplementedError
    
    def deleteTable(self):
        raise NotImplementedError    
       

class DynamoDbSocio(DynamoDbInterface):
    def __init__(self,dynamodb=None):        
        # Crear una instancia de cliente DynamoDB
        if dynamodb is None:
            self.dynamodb = boto3.client('dynamodb',
                                    region_name='us-east-1',
                                    aws_access_key_id= os.environ['AWS_ACCESS_KEY_ID'],
                                    aws_secret_access_key= os.environ['AWS_SECRET_ACCESS_KEY'])
        else:
            self.dynamodb = dynamodb

        self.table_name = 'socio'

    # Funciones para interactuar con DynamoDB
    def create_table(self):
        if not self.tablaExits(self.table_name):

            self.dynamodb.create_table(
                    TableName=self.table_name,
                    AttributeDefinitions=[
                        {
                            'AttributeName': 'id_usuario',
                            'AttributeType': 'S',
                        }
                    ],
                    KeySchema=[
                        {
                            'AttributeName': 'id_usuario',
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

    def insert_item(self,socio: SocioModel):
        item = {
            "id_usuario": {'S': socio.id_usuario },
            'nombre': {'S': socio.nombre },
            'apellido': {'S': socio.apellido },
            'especialidad': {'S': socio.especialidad },
            'anio_experiencia': {'N': str(socio.anios_experiencia) }, # 'N' es el tipo de dato 'Number
            'genero': {'S': socio.genero },
            'telefono': {'S': socio.telefono },
            'tipo_identificacion': {'S': socio.tipo_identificacion },
            'numero_identificacion': {'S': socio.numero_identificacion },            
            'numero_tarjeta_profesional': {'S': socio.numero_tarjeta_profesional },
            'pais_recidencia': {'S': socio.pais_recidencia },
            'ciudad_recidencia': {'S': socio.ciudad_recidencia },
            'organizador': {'BOOL': socio.organizador},
            'fecha_creacion': {'S': str(socio.fecha_creacion)}  # Datetime conversion
             
            # Puedes agregar más atributos según la definición de tu tabla
        }
        result = self.dynamodb.put_item(
            TableName=self.table_name,
            Item=item,
            ReturnConsumedCapacity='TOTAL'
        )
        print('Ítem insertado correctamente.')

    def get_item(self,id_usuario):
        key = {
            'id_usuario': {'S': str(id_usuario) }  # Clave de búsqueda
        }
        response = self.dynamodb.get_item(
            TableName=self.table_name,
            Key=key
        )
        item = response.get('Item')
        if not item:
            return None
        
        # Extrae los valores de cada campo
        id_usuario = item['id_usuario']['S']
        nombre = item['nombre']['S']
        apellido = item['apellido']['S']        
        especialidad = item['especialidad']['S']
        anio_experiencia = item['anio_experiencia']['N']
        genero = item['genero']['S']
        telefono = item['telefono']['S']
        tipo_identificacion = item['tipo_identificacion']['S']
        numero_identificacion = item['numero_identificacion']['S']        
        numero_tarjeta_profesional = item['numero_tarjeta_profesional']['S']
        pais_recidencia = item['pais_recidencia']['S']
        ciudad_recidencia = item['ciudad_recidencia']['S']
        organizador = item['organizador']['BOOL']
        fecha_creacion = item['fecha_creacion']['S']

        # Crea una instancia de la clase Entrenamiento
        socio = SocioModel(id_usuario,nombre,apellido,especialidad,anio_experiencia,genero,telefono,tipo_identificacion,numero_identificacion,
                            numero_tarjeta_profesional,pais_recidencia,ciudad_recidencia, organizador, fecha_creacion)

        return socio
    
    def get_all(self):
        # Escaneo de todos los elementos de la tabla
        response = self.dynamodb.scan(
            TableName=self.table_name
        )

        # Recuperar los items escaneados
        items = response['Items']
                
        # Si hay más resultados, seguir escaneando
        while 'LastEvaluatedKey' in response:
            response = self.dynamodb.scan(
                TableName=self.table_name,
                ExclusiveStartKey=response['LastEvaluatedKey']
            )
            items.extend(response['Items'])
        
        # Procesar los items encontrados
        resultados = []
        for item in items:
            id_usuario = item['id_usuario']['S']
            nombre = item['nombre']['S']
            apellido = item['apellido']['S']        
            especialidad = item['especialidad']['S']
            anio_experiencia = item['anio_experiencia']['N']
            genero = item['genero']['S']
            telefono = item['telefono']['S']
            tipo_identificacion = item['tipo_identificacion']['S']
            numero_identificacion = item['numero_identificacion']['S']        
            numero_tarjeta_profesional = item['numero_tarjeta_profesional']['S']
            pais_recidencia = item['pais_recidencia']['S']
            ciudad_recidencia = item['ciudad_recidencia']['S']
            organizador = item['organizador']['BOOL']
            fecha_creacion = item['fecha_creacion']['S']
        
            socio = SocioModel(id_usuario,nombre,apellido,especialidad,anio_experiencia,genero,telefono,tipo_identificacion,numero_identificacion,
                            numero_tarjeta_profesional,pais_recidencia,ciudad_recidencia, organizador, fecha_creacion)
            resultados.append(socio)
        
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