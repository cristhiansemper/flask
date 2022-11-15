#*************************************************************************************
# Este servicio web permite mostrar un listado de clientes e insertar clientes nuevos
#*************************************************************************************

# Importar los paquetes y clases necesarios para implementar el servicio web
from flask import Blueprint, request, jsonify
from models.cliente import Cliente
import json
import validarToken

ws_cliente = Blueprint('ws_cliente', __name__)

@ws_cliente.route('/cliente/listar', methods=['POST'])
@validarToken.validar_token #Función de envoltura o función que se encarga de proteger a la función "listar()"
def listar():
    if request.method == 'POST':
        objCliente = Cliente()
        rptaJSON = objCliente.listarCliente()
        datos_cliente = json.loads(rptaJSON)
        return jsonify(datos_cliente), 200  #200->ok



@ws_cliente.route('/cliente/insertar', methods=['POST'])
#@validarToken.validar_token #Función de envoltura o función que se encarga de proteger a la función "insertar()"
def insertar():
    if request.method == 'POST':
        tipo_documento = request.form['tipo_documento']
        documento = request.form['documento']
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        email = request.form['email']
        telefono = request.form['telefono']
        usuario_id=request.form['id_usuario']
      
        objCliente = Cliente(0, tipo_documento, documento, nombre, direccion, email, telefono,usuario_id)
        rptaJSON = objCliente.insertar()
        datos_cliente = json.loads(rptaJSON)
        return jsonify(datos_cliente), 200  #200->ok

@ws_cliente.route('/cliente/update', methods=['POST'])
@validarToken.validar_token #Función de envoltura o función que se encarga de proteger a la función "insertar()"
def updateestado():
    if request.method == 'POST':
        estado = request.form['estado']
        id = request.form['id']

        objCliente = Cliente()
        rptaJSON = objCliente.updateEstado(estado,id)
        datos_cliente = json.loads(rptaJSON)
        return jsonify(datos_cliente), 200  #200->ok

@ws_cliente.route('/cliente/listarfiltro', methods=['POST'])
@validarToken.validar_token #Función de envoltura o función que se encarga de proteger a la función "insertar()"
def listafiltro():
    if request.method == 'POST':
        estado = request.form['estado']
        tipo_doc = request.form['tipo_documento']
        nombre = request.form['nombre']

        objCliente = Cliente()
        rptaJSON = objCliente.listarClienteFiltro(estado,tipo_doc,nombre)
        datos_cliente = json.loads(rptaJSON)
        return jsonify(datos_cliente), 200  #200->ok