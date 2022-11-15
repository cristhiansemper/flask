from flask import Blueprint, request, jsonify
from models.detalle_solicitud import Detalle_Solicitud
import json
import validarToken

ws_detalle_solicitud = Blueprint('ws_detalle_solicitud',__name__)

@ws_detalle_solicitud.route('/detalle_solicitud/listar',methods=['POST'])
@validarToken.validar_token
def listar():
  if request.method=='POST':
    objDetalleSolicitud = Detalle_Solicitud()
    rptaJSON=objDetalleSolicitud.listarDetalleSolicitud()
    datos_detalle_solicitud = json.loads(rptaJSON)
    return jsonify(datos_detalle_solicitud), 200

@ws_detalle_solicitud.route('/detalle_solicitud/insertar',methods=['POST'])
@validarToken.validar_token
def insertar():
  if request.method=='POST':
    id_chofer_vehiculo=request.form['id_chofer_vehiculo']
    id_solicitud=request.form['id_solicitud']
    
    objDetalleSolicitud = Detalle_Solicitud(0,id_chofer_vehiculo,id_solicitud)
    rptaJSON=objDetalleSolicitud.insertar()
    datos_detalle_solicitud = json.loads(rptaJSON)
    return jsonify(datos_detalle_solicitud), 200