#*************************************************************************************
# Este servicio web permite validar las credenciales del usuario e iniciar sesión
# Adicionalmente se generará un token de seguridad, utilizando JWT
#*************************************************************************************

# Importar los paquetes y clases necesarios para implementar el servicio web
from flask import Blueprint, request, jsonify
from models.solicitud import Solicitud
from models.tarifa import Tarifa
from models.sesion import Sesion
#from models.configuracion import Configuracion
from config import SecretKey 
import jwt
import datetime
import json

from models.usuario import Usuario

#Se genera el módulo con el cual se gestionará el servicio web de inicio de sesión
ws_sesion = Blueprint('ws_sesion', __name__)

@ws_sesion.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        #Leer los datos que vienen mediante el método POST
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
      

        #Instanciar un objeto de la clase Sesion, con la finalidad de enviar el email y la clave
        objSesion = Sesion(usuario, contrasena)

        #Obtener respuesta del método iniciarSesion()
        rptaJSON = objSesion.iniciarSesion()

        #Convertir la respuesta JSON (cadena) a objeto JSON
        datosSesion = json.loads(rptaJSON)

        if datosSesion['status'] == True: #Credenciales son correctas y se le dará accedo a la aplicación (inicio de sesión satisfactorio)
            #Almacenar el ID del usuario dentro del token
            usuarioId = datosSesion['data']['id']

            #Generar el token con jwt
            token = jwt.encode({'usuarioId': usuarioId, 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60*60*12)}, SecretKey.JWT_SECRET_KEY)


            #Actualizar el token generado por el inicio de sesión
            objSesion.actualizarToken(token, usuarioId)

            #Incluir al token dentro de la respuesta del servicio web
            datosSesion['data']['token'] = token # El ".decode('UTF-8')" sirve para versiones de jwt menores a 2.0

            #Obtener el valor del parámetro de tarifa
            objTarifa = Tarifa()

            rptaJSONConfiguracion = objTarifa.obtenerValorTarifa() #id 1=VAlor20
            datosConfiguracion = json.loads(rptaJSONConfiguracion)
            valorTarifa = datosConfiguracion['data']['valor']
            idTarifa=datosConfiguracion['data']['id']


            ###dia de la semana
            rptaJSONDia=objSesion.obtnerDiaSemana()
            datosDia=json.loads(rptaJSONDia)
            dia= datosDia['data']['DIA']

            #Agregar datos a la variable datosSesion
            datosSesion['data']['precio_tarifa'] = valorTarifa
            datosSesion['data']['id_tarifa'] = idTarifa


            tipo_usuario= datosSesion['data']['tipo_usuario']
            datosSesion['data']['nomDia'] =dia
            if tipo_usuario=='cliente':
                rptaJSONEstadoCliente= objSesion.validarEstadoCliente(usuarioId)
                datosEstadoCliente=json.loads(rptaJSONEstadoCliente)
                valorEstado= datosEstadoCliente['data']['estado']
                datosSesion['data']['estado_cliente']=valorEstado

            #Mostrar la respuesta del servicio web en formato JSON
            return jsonify(datosSesion), 200 #Status de la petición http es satisfactoria (OK)
        else:
            return jsonify(datosSesion), 401 #El usuario no se encuentra autorizado para ingresar a la app





