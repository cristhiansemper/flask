from flask import Blueprint, request, jsonify
from models.tarifa import Tarifa
import json
import validarToken
ws_tarifa = Blueprint('ws_tarifa', __name__)

@ws_tarifa.route('/tarifa/insertar', methods=['POST'])
#@validarToken.validar_token #Función de envoltura o función que se encarga de proteger a la función "insertar()"
def insertar():
    if request.method == 'POST':
        valor = request.form['valor']

        objTarifa = Tarifa(0,valor)
        rptaJSON = objTarifa.insertar()
        datos_tarifa = json.loads(rptaJSON)
        return jsonify(datos_tarifa), 200  #200->ok