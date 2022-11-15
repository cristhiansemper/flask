#*************************************************************************************
# Este servicio web permite mostrar las solicitudes
#*************************************************************************************

# Importar los paquetes y clases necesarios para implementar el servicio web
import re
from flask import Blueprint, request, jsonify
from models.solicitud  import Solicitud
from models.sesion import Sesion
import json
import validarToken

ws_solicitud = Blueprint('ws_solicitud', __name__)
@ws_solicitud.route('/solicitud/listar', methods=['POST'])
@validarToken.validar_token #Función de envoltura o función que se encarga de proteger a la función "listar()"
def listar():
    if request.method == 'POST':
        objSolicitud = Solicitud()
        rptaJSON = objSolicitud.listarSolicitud()
        datos_solicitud = json.loads(rptaJSON)
        return jsonify(datos_solicitud), 200  #200->ok

@ws_solicitud.route('/solicitud/insertar', methods=['POST'])
@validarToken.validar_token #Función de envoltura o función que se encarga de proteger a la función "insertar()"
def insertar():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        clase = request.form['clase']
        tipo = request.form['tipo']
        categoria = request.form['categoria']
        peso = request.form['peso']
        fecha_y_hora_partida = request.form['fecha_y_hora_partida']
        direccion_partida = request.form['direccion_partida']
        llegada_carga= request.form['llegada_carga']
        distancia= request.form['distancia']
        monto= request.form['monto']
        id_usuario= request.form['id_usuario']
        id_tarifa= request.form['id_tarifa']

        objSolicitud = Solicitud(0, descripcion, clase,tipo,categoria, peso,fecha_y_hora_partida,direccion_partida,llegada_carga,distancia,monto,id_usuario, id_tarifa)
        rptaJSON = objSolicitud.insertar()
        datos_pago = json.loads(rptaJSON)
        return jsonify(datos_pago), 200  #200->ok

@ws_solicitud.route('/solicitud/listarcliente', methods=['POST'])
@validarToken.validar_token #Función de envoltura o función que se encarga de proteger a la función "listar()"
def listarSolicitudCliente():
    if request.method == 'POST':
        usu_id = request.form['usu_id']
        objSolicitud = Solicitud()
        rptaJSON = objSolicitud.listarSolicitudCliente(usu_id)
        datos_solicitud = json.loads(rptaJSON)
        return jsonify(datos_solicitud), 200  #200->ok

@ws_solicitud.route('/solicitud/listarchofer', methods=['POST'])
@validarToken.validar_token #Función de envoltura o función que se encarga de proteger a la función "listar()"
def listarSolicitudChofer():
    if request.method == 'POST':
        usu_id = request.form['usu_id']
        objSolicitud = Solicitud()
        rptaJSON = objSolicitud.listarSolicitudChofer(usu_id)
        datos_solicitud = json.loads(rptaJSON)
        return jsonify(datos_solicitud), 200  #200->ok

@ws_solicitud.route('/solicitud/listargeneralchofer', methods=['POST'])
@validarToken.validar_token #Función de envoltura o función que se encarga de proteger a la función "listar()"
def listarSolicitudGeneralChofer():
    if request.method == 'POST':
        usu_id = request.form['usu_id']
        objSolicitud = Solicitud()
        rptaJSON = objSolicitud.listarSolicitudGeneralChofer(usu_id)
        datos_solicitud = json.loads(rptaJSON)
        return jsonify(datos_solicitud), 200  #200->ok

@ws_solicitud.route('/solicitud/anular', methods=['POST'])
@validarToken.validar_token #Función de envoltura o función que se encarga de proteger a la función "insertar()"
def Estadoanular():
    if request.method == 'POST':
        id = request.form['id']

        objSolicitud = Solicitud()
        rptaJSON = objSolicitud.Estadoanular(id)
        datos_solicitud = json.loads(rptaJSON)
        return jsonify(datos_solicitud), 200  #200->ok

@ws_solicitud.route('/solicitud/numpagopendiente', methods=['POST'])
#@validarToken.validar_token #Función de envoltura o función que se encarga de proteger a la función "listar()"
def validarEstadoPago():
    if request.method == 'POST':
        id=request.form['id_usuario']
        objSolicitud = Solicitud()
        rptaJSON = objSolicitud.obtnerNumValidarPagoPendiente(id)
        datos_solicitud = json.loads(rptaJSON)
        return jsonify(datos_solicitud), 200  #200->ok


@ws_solicitud.route('/solicitud/numSolicitudesFinalizadas', methods=['POST'])
#@validarToken.validar_token #Función de envoltura o función que se encarga de proteger a la función "listar()"
def validarSolicitudFinalizadas():
    if request.method == 'POST':
        id=request.form['id_usuario']
        objSolicitud = Solicitud()
        rptaJSON = objSolicitud.obtnerNumSolicitudesFinalizadas(id)
        datos_solicitud = json.loads(rptaJSON)
        return jsonify(datos_solicitud), 200  #200->ok