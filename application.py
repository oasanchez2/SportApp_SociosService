from flask import Flask, jsonify
from src.blueprints.socio import socios_blueprint
from src.errors.errors import ApiError
from flask_cors import CORS
from src.dynamodb_producto_servicio  import DynamoDbProductoServicio

application = Flask(__name__)
application.register_blueprint(socios_blueprint)
CORS(application)
DynamoDbProductoServicio().create_table()
## add comment
@application.errorhandler(ApiError)
def handle_exception(err):
    response = {
      "mssg": err.description 
    }
    return jsonify(response), err.code
##
if __name__ == "__main__":
    application.run(host="0.0.0.0", port = 5003, debug = True)
