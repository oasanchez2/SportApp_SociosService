from flask import Flask, jsonify, request, Blueprint
from ..commands.create_producto_servicio import CreateProductoServicio
from ..commands.get_producto_servicio import GetProductoServicio
from ..commands.get_todos_producto_servicio import GetTodosProductosServicios
from ..commands.reset_producto_servicio import ResetProductoServicio

socios_blueprint = Blueprint('socios', __name__)

@socios_blueprint.route('/socios/producto-servicio', methods = ['POST'])
def create_producto_servicio():
    producto_servicio = CreateProductoServicio(request.get_json()).execute()
    return jsonify(producto_servicio), 201

@socios_blueprint.route('/socios/producto-servicio/<id>', methods = ['GET'])
def show_producto_servicio(id):
    """ Authenticate(auth_token()).execute() """
    producto_servicio = GetProductoServicio(id).execute() 
    return jsonify(producto_servicio)

@socios_blueprint.route('/socios/producto-servicio/all', methods = ['GET'])
def alls_producto_servicio():
    """ Authenticate(auth_token()).execute() """
    ejercicio = GetTodosProductosServicios().execute() 
    return jsonify(ejercicio)

@socios_blueprint.route('/socios/ping', methods = ['GET'])
def ping():
    return 'pong'

@socios_blueprint.route('/socios/producto-servicio/reset', methods = ['POST'])
def reset_producto_servicio():
    ResetProductoServicio().execute()
    return jsonify({'status': 'OK'})

def auth_token():
    if 'Authorization' in request.headers:
        authorization = request.headers['Authorization']
    else:
        authorization = None
    return authorization