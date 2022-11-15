#*************************************************************************************
# Este servicio web permite mostrar el detalle de estado de la solicitud
#*************************************************************************************

# Importar los paquetes y clases necesarios para implementar el servicio web
from flask import Blueprint, request, jsonify
from models.detalle_solicitud_estado  import DetalleSolicitudEstado
from models.sesion import Sesion
import json
import validarToken

ws_detalle_solicitud_estado = Blueprint('ws_detalle_solicitud_estado', __name__)



@ws_detalle_solicitud_estado.route('/detalle_solicitud_estado/insertar', methods=['POST'])
@validarToken.validar_token #Función de envoltura o función que se encarga de proteger a la función "insertar()"
def insertar():
    if request.method == 'POST':
        estado = request.form['estado']
        observacion = request.form['observacion']
        id_detalle_solicitud = request.form['id_detalle_solicitud']
        objDetalleSolicitudEstado = DetalleSolicitudEstado(0, estado, observacion,id_detalle_solicitud)
        rptaJSON = objDetalleSolicitudEstado.insertar()
        datos_pago = json.loads(rptaJSON)
        return jsonify(datos_pago), 200  #200->ok

@ws_detalle_solicitud_estado.route('/detalle_solicitud_estado/listarReportesSolicitud', methods=['POST'])
@validarToken.validar_token #Función de envoltura o función que se encarga de proteger a la función "listar()"
def listarReportesSolicitud():
    if request.method == 'POST':
        sol_id = request.form['sol_id']
        objDetalleSolicitudEstado = DetalleSolicitudEstado()
        rptaJSON = objDetalleSolicitudEstado.listarReportesSolicitud(sol_id)
        datos_solicitud = json.loads(rptaJSON)
        return jsonify(datos_solicitud), 200  #200->ok