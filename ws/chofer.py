from flask import Blueprint, request, jsonify
from models.chofer import Chofer
import json
import validarToken

ws_chofer = Blueprint('ws_chofer',__name__)

@ws_chofer.route('/chofer/listar', methods=['POST'])
@validarToken.validar_token
def listar():
  if request.method == 'POST':
    objChofer = Chofer()
    rptaJSON = objChofer.listarChofer()
    datos_chofer = json.loads(rptaJSON)
    return jsonify(datos_chofer), 200 #OK
    
@ws_chofer.route('/chofer/insertar', methods=['POST'])
@validarToken.validar_token
def insertar():
  if request.method == 'POST':
    documento = request.form['documento']
    nombres = request.form['nombres']
    telefono = request.form['telefono']
    direccion = request.form['direccion']
    usuario_id= request.form['id_usuario']

    objChofer = Chofer(0,documento,nombres,telefono,direccion,usuario_id)
    rptaJSON = objChofer.insertar()
    datos_chofer = json.loads(rptaJSON)
    return jsonify(datos_chofer), 200 #ok
  
@ws_chofer.route('/chofer/listarlibres', methods=['POST'])
@validarToken.validar_token
def listarlibre():
  if request.method == 'POST':
    objChofer = Chofer()
    rptaJSON = objChofer.listarChoferLibre()
    datos_chofer = json.loads(rptaJSON)
    return jsonify(datos_chofer), 200 #OK