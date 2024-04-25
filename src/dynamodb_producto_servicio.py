import boto3
import os
import json
from boto3.dynamodb.conditions import Key, Attr
from .models.producto_servicio_model import ProductoServicioModel
from botocore.exceptions import ClientError

class DynamoDbInterface:
    def create_table(self):
        raise NotImplementedError
    
    def insert_item(self, producto_servicio: ProductoServicioModel):
        raise NotImplementedError
    
    def get_item(self, id_producto_servicio):
        raise NotImplementedError
    
    def get_Item_nombre(self,nombre):
        raise NotImplementedError
    
    def get_all(self):
        raise NotImplementedError

    def tablaExits(self,name):
        raise NotImplementedError
    
    def deleteTable(self):
        raise NotImplementedError    
       
    
class DynamoDbProductoServicio(DynamoDbInterface):
    def __init__(self,dynamodb=None):
        # Crear una instancia de cliente DynamoDB
        if dynamodb is None:
            self.dynamodb = boto3.client('dynamodb',
                                    region_name='us-east-1',
                                    aws_access_key_id= os.environ['AWS_ACCESS_KEY_ID'],
                                    aws_secret_access_key= os.environ['AWS_SECRET_ACCESS_KEY'])
        else:
            self.dynamodb = dynamodb
        
        self.table_name = 'producto-servicio'

    # Funciones para interactuar con DynamoDB

    def create_table(self):
        if not self.tablaExits(self.table_name):

            self.dynamodb.create_table(
                    TableName=self.table_name,
                    AttributeDefinitions=[
                        {
                            'AttributeName': 'id_producto_servicio',
                            'AttributeType': 'S',
                        }
                    ],
                    KeySchema=[
                        {
                            'AttributeName': 'id_producto_servicio',
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

    def insert_item(self,producto_servicio: ProductoServicioModel):
        item = {
            'id_producto_servicio': {'S':  producto_servicio.id_producto_servicio },
            'id_socio': {'S': producto_servicio.id_socio},
            'nombre': {'S': producto_servicio.nombre },
            'descripcion': {'S': producto_servicio.descripcion},
            'costo': {'N': str(producto_servicio.costo)},
            'tipo_oferta': {'S': producto_servicio.tipo_oferta}            
            # Puedes agregar más atributos según la definición de tu tabla
        }
        result = self.dynamodb.put_item(
            TableName=self.table_name,
            Item=item,
            ReturnConsumedCapacity='TOTAL'
        )
        print('Ítem insertado correctamente.')

    def get_item(self,id_producto_servicio):
        key = {
            'id_producto_servicio': {'S': str(id_producto_servicio) }  # Clave de búsqueda
        }
        response = self.dynamodb.get_item(
            TableName=self.table_name,
            Key=key
        )
        item = response.get('Item')
        if not item:
            return None

        # Extrae los valores de cada campo
        id_producto_servicio = item['id_producto_servicio']['S']
        id_socio = item['id_socio']['S']
        nombre = item['nombre']['S']
        descripcion = item['descripcion']['S']
        costo = int(item['costo']['N'])
        tipo_oferta = item['tipo_oferta']['S']
               

        # Crea una instancia de la clase Entrenamiento
        producto_servicio = ProductoServicioModel(id_producto_servicio,id_socio,nombre,descripcion,costo,tipo_oferta)

        # Devuelve el objeto como diccionario
        return producto_servicio

    def get_Item_nombre(self,nombre):
        
        # Parámetros para la operación de escaneo
        parametros = {
            'TableName': self.table_name,
            'FilterExpression': '#nombre = :nombre',
            'ExpressionAttributeNames': {
                '#nombre': 'nombre'
            },
            'ExpressionAttributeValues': {
                ':nombre': {'S': nombre}
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
            id_producto_servicio = item['id_producto_servicio']['S']
            id_socio = item['id_socio']['S']
            nombre = item['nombre']['S']
            descripcion = item['descripcion']['S']
            costo = int(item['costo']['N'])
            tipo_oferta = item['tipo_oferta']['S']

            producto_servicio = ProductoServicioModel(id_producto_servicio,id_socio,nombre,descripcion,costo,tipo_oferta)
            resultados.append(producto_servicio)

        return resultados

    def get_all(self):
        # Escaneo de todos los elementos de la tabla
        response = self.dynamodb.scan(
            TableName=self.table_name
        )

        # Recuperar los items escaneados
        items = response['Items']
        if not items:
            return None
        
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
            id_producto_servicio = item['id_producto_servicio']['S']
            id_socio = item['id_socio']['S']
            nombre = item['nombre']['S']
            descripcion = item['descripcion']['S']
            costo = int(item['costo']['N'])
            tipo_oferta = item['tipo_oferta']['S']
        
            producto_servicio = ProductoServicioModel(id_producto_servicio,id_socio,nombre,descripcion,costo,tipo_oferta)
            resultados.append(producto_servicio)
        
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