#*************************************************************************************
# Este servicio web permite mostrar un listado de ubicaciones e insertar nuevas
#*************************************************************************************

# Importar los paquetes y clases necesarios para implementar el servicio web
from flask import Blueprint, request, jsonify
from models.ubicacion import Ubicacion
import json
import validarToken

ws_ubicacion = Blueprint('ws_ubicacion', __name__)

@ws_ubicacion.route('/ubicacion/listar', methods=['POST'])
@validarToken.validar_token #Función de envoltura o función que se encarga de proteger a la función "listar()"
def listar():
    if request.method == 'POST':
        objUbicacion = Ubicacion()
        rptaJSON = objUbicacion.listarUbicacion()
        datos_ubicacion = json.loads(rptaJSON)
        return jsonify(datos_ubicacion), 200  #200->ok

@ws_ubicacion.route('/ubicacion/insertar', methods=['POST'])
#@validarToken.validar_token #Función de envoltura o función que se encarga de proteger a la función "insertar()"
def insertar():
    if request.method == 'POST':
        latitud = request.form['latitud']
        longitud = request.form['longitud']
        id_chofer_vehiculo = request.form['id_chofer_vehiculo']
      
        objUbicacion = Ubicacion(0, latitud, longitud, id_chofer_vehiculo)
        rptaJSON = objUbicacion.insertar()
        datos_ubicacion = json.loads(rptaJSON)
        return jsonify(datos_ubicacion), 200  #200->ok

