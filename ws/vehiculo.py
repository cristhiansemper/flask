#**************************************************************************************
# Este servicio web permite mostrar un listado de vehículos e insertar vehículos nuevos
#**************************************************************************************

# Importar los paquetes y clases necesarios para implementar el servicio web
from flask import Blueprint, request, jsonify
from models.vehiculo import Vehiculo
import json
import validarToken

ws_vehiculo = Blueprint('ws_vehiculo', __name__)

@ws_vehiculo.route('/vehiculo/listar', methods=['POST'])
@validarToken.validar_token #Función de envoltura o función que se encarga de proteger a la función "listar()"
def listar():
    if request.method == 'POST':
        objVehiculo = Vehiculo()
        rptaJSON = objVehiculo.listarVehiculo()
        datos_vehiculo = json.loads(rptaJSON)
        return jsonify(datos_vehiculo), 200  #200->ok

@ws_vehiculo.route('/vehiculo/insertar', methods=['POST'])
@validarToken.validar_token #Función de envoltura o función que se encarga de proteger a la función "insertar()"
def insertar():
    if request.method == 'POST':
        placa = request.form['placa']
        peso_maximo = request.form['peso_maximo']

        objVehiculo = Vehiculo(0, placa, peso_maximo)
        rptaJSON = objVehiculo.insertar()
        datos_vehiculo = json.loads(rptaJSON)
        return jsonify(datos_vehiculo), 200  #200->ok

@ws_vehiculo.route('/vehiculo/listarlibres', methods=['POST'])
@validarToken.validar_token #Función de envoltura o función que se encarga de proteger a la función "listar()"
def listarlibres():
    if request.method == 'POST':
        objVehiculo = Vehiculo()
        rptaJSON = objVehiculo.listarVehiculoLibres()
        datos_vehiculo = json.loads(rptaJSON)
        return jsonify(datos_vehiculo), 200  #200->ok