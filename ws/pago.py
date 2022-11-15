#**************************************************************************************
# Este servicio web permite mostrar un listado de pagos e insertar pagos nuevos
#**************************************************************************************

# Importar los paquetes y clases necesarios para implementar el servicio web
from cgitb import reset
from flask import Blueprint, request, jsonify
from models.pago import Pago
import json
import validarToken

ws_pago = Blueprint('ws_pago', __name__)

@ws_pago.route('/pago/listar', methods=['POST'])
@validarToken.validar_token #Función de envoltura o función que se encarga de proteger a la función "listar()"
def listar():
    if request.method == 'POST':
        objPago = Pago()
        rptaJSON = objPago.listarPago()
        datos_pago = json.loads(rptaJSON)
        return jsonify(datos_pago), 200  #200->ok

@ws_pago.route('/pago/insertar', methods=['POST'])
@validarToken.validar_token #Función de envoltura o función que se encarga de proteger a la función "insertar()"
def insertar():
    if request.method == 'POST':
        entidad_financiera = request.form['entidad_financiera']
        numero_operacion = request.form['numero_operacion']
        fecha_y_hora_operacion = request.form['fecha_y_hora_operacion']
        monto = request.form['monto']
        observacion = request.form['observacion']
        voucher = request.form['voucher']
        solicitud_id = request.form['solicitud_id']

        objPago = Pago(0, entidad_financiera, numero_operacion,fecha_y_hora_operacion, monto, observacion, voucher,solicitud_id)
        rptaJSON = objPago.insertar()
        datos_pago = json.loads(rptaJSON)
        return jsonify(datos_pago), 200  #200->ok

@ws_pago.route('/pago/listarcliente', methods=['POST'])
@validarToken.validar_token #Función de envoltura o función que se encarga de proteger a la función "listar()"
def listarPagoCliente():
    if request.method == 'POST':
        usu_id = request.form['usu_id']
        objPago = Pago()
        rptaJSON = objPago.listarPagoCliente(usu_id)
        datos_solicitud = json.loads(rptaJSON)
        return jsonify(datos_solicitud), 200  #200->ok

@ws_pago.route('/pago/validar', methods=['POST'])
@validarToken.validar_token #Función de envoltura o función que se encarga de proteger a la función "insertar()"
def Validarpago():
    if request.method == 'POST':
        id = request.form['id']
        est = request.form['est']
        
        objPago = Pago()
        rptaJSON = objPago.Pagovalidar(est,id)
        datos_solicitud = json.loads(rptaJSON)
        return jsonify(datos_solicitud), 200  #200->ok

@ws_pago.route('/pago/voucher', methods=['POST'])
@validarToken.validar_token #Función de envoltura o función que se encarga de proteger a la función "insertar()"
def listarVoucher():
    if request.method == 'POST':
        id = request.form['id_sol']
        
        objPago = Pago()
        rptaJSON = objPago.listarvoucher(id)
        datos_solicitud = json.loads(rptaJSON)
        return jsonify(datos_solicitud), 200  #200->ok
