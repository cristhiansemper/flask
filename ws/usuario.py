#**************************************************************************************
# Este servicio web permite mostrar un listado de pagos e insertar pagos nuevos
#**************************************************************************************

# Importar los paquetes y clases necesarios para implementar el servicio web
from flask import Blueprint, request, jsonify
from models.usuario import Usuario
import json
import validarToken

ws_usuario = Blueprint('ws_usuario', __name__)

@ws_usuario.route('/usuario/listar', methods=['POST'])
@validarToken.validar_token #Función de envoltura o función que se encarga de proteger a la función "listar()"
def listar():
    if request.method == 'POST':
        objUsuario = Usuario()
        rptaJSON = objUsuario.listarUsuario()
        datos_usuario = json.loads(rptaJSON)
        return jsonify(datos_usuario), 200  #200->ok

@ws_usuario.route('/usuario/insertar', methods=['POST'])
#@validarToken.validar_token #Función de envoltura o función que se encarga de proteger a la función "insertar()"
def insertar():
    if request.method == 'POST':
        nombre = request.form['usuario']
        contrasena = request.form['contrasena']
        tipo_usuario = request.form['tipo_usuario']

        objUsuario = Usuario(0, nombre, contrasena,tipo_usuario)
        rptaJSON = objUsuario.insertar()
        datos_usuario = json.loads(rptaJSON)
        return jsonify(datos_usuario), 200  #200->ok

