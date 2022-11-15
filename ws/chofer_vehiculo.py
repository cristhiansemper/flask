from flask import Blueprint, request, jsonify
from models.chofer_vehiculo import Chofer_Vehiculo
import json
import validarToken

ws_chofer_vehiculo = Blueprint('ws_chofer_vehiculo',__name__)

@ws_chofer_vehiculo.route('/chofer_vehiculo/listar', methods=['POST'])
@validarToken.validar_token

def listar():
  if request.method == 'POST':
    objChofer_Vehiculo = Chofer_Vehiculo()
    rptaJSON = objChofer_Vehiculo.listarChofer_vehiculo()
    datos_chofer_vehiculo = json.loads(rptaJSON)
    return jsonify(datos_chofer_vehiculo), 200 #OK

@ws_chofer_vehiculo.route('/chofer_vehiculo/insertar', methods=['POST'])
@validarToken.validar_token
def insertar():
  if request.method == 'POST':
    
    id_vehiculo = request.form['id_vehiculo']
    id_chofer = request.form['id_chofer']
    
    objChofer_Vehiculo = Chofer_Vehiculo(0,id_vehiculo,id_chofer)
    rptaJSON = objChofer_Vehiculo.insertar()
    datos_chofer_vehiculo = json.loads(rptaJSON)
    return jsonify(datos_chofer_vehiculo), 200 #ok
    