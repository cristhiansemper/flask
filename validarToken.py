#*************************************************************************************
# Permite validar el token recibido mediante la petición que se hace al servicio web
#*************************************************************************************

from ast import arg
from flask import jsonify, request
import jwt
from functools import wraps
from config import SecretKey
import json
from models.sesion import Sesion

#Validar el estado del token del usuario en la BASE DE DATOS, con la finalidad de conocer si el token se encuentra ACTIVO o INACTIVO
def validar_estado_token_usuario(usuario_id):
    objSesion = Sesion()
    rptaJSON = objSesion.validarEstadoToken(usuario_id)
    datos_token = json.loads(rptaJSON)
    if datos_token['status'] == True: #Significa que la consulta ha devuelto datos
        estado_token_usuario = datos_token['data']['estado_token']
        if estado_token_usuario == None: #Devuelve None cuando el campo de la tabla se encuentra vacio
            return False #No tendrá acceso al servicio web
        else:
            if estado_token_usuario == '0': #significa que el token se encuentra inactivo
                return False #No tendrá acceso al servicio web
            else:
                return True #SI tendrá acceso al servicio web
    else:
        return False #No tendrá acceso al servicio web


#Validar el token a nivel de FIRMA, TIEMPO DE VIDA o algún otro error de codificación del TOKEN
def validar_token(fx):
    @wraps(fx)
    def decorated(*args, **kwargs):
        token = request.form['token']

        if not token:
            return jsonify({'status': False, 'data': 'Falta token'}), 403
        
        try:
           #Decodificar el token
           #data = jwt.decode(token, SecretKey.JWT_SECRET_KEY)
           data = jwt.decode(token, SecretKey.JWT_SECRET_KEY, algorithms="HS256") #para versiones mayor o igual a 2.0 de PyJWT

           #Extraer el id del usuario, el cual se encuentra guardado en el token
           usuario_id = data['usuarioId']

           #Consultar el estado del token a nivel de BD
           estado_token_bd = validar_estado_token_usuario(usuario_id)

           if estado_token_bd == False:
               return jsonify({'status': False, 'data': 'El token se encuentra inactivo'}), 403


        except (jwt.DecodeError, jwt.ExpiredSignatureError) as error:
            return jsonify({'status': False, 'data': 'El token es invalido', 'internal_token_error': format(error)}), 403

        except (Exception) as error:
            return jsonify({'status': False, 'data': 'El token es invalido', 'internal_token_error': format(error)}), 403

        return fx(*args, **kwargs)
    
    return decorated