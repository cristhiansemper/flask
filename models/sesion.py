from ast import If
#from msilib.schema import Error
from sqlalchemy import delete, insert
import sqlalchemy
from conexionBD import Conexion as db
import json
from util import CustomJsonEncoder

class Sesion():
    def __init__(self, p_usuario=None, p_contrasena=None):
        self.usuario = p_usuario
        self.contrasena = p_contrasena

    def iniciarSesion(self):
        #Abrir conexión a la BD
        con = db().open

        #Crear un cursor para almacenar el resultado de la consulta SQL, realizada para validar las credenciales
        cursor = con.cursor()

        #Preparar la consulta SQL para validar las credenciales
        sql = "select id, usuario, estado, tipo_usuario from usuario  where usuario=%s and contrasena=%s"

        #ejecutar la consulta SQL
        cursor.execute(sql, [self.usuario, self.contrasena])

        #capturar el resultado de la consulta SQL
        datos = cursor.fetchone()

        #cerrar el cursor de la base de datos y luego cerrar la conexion
        cursor.close()
        con.close()

        #Retonar una respuesta sobre el inicio de sesión
        if datos: #se pregunta si la consulta SQL ha devuelto registros
            if datos['estado'] == '1': #1=Usuario activo
                return json.dumps({'status': True, 'data':datos, 'mensaje_bienvenida':'Credenciales correctas, bienvenido a la aplicación'})
            else:
                return json.dumps({'status':False, 'data':'El usuario se encuentra inactivo, consulte con su administrador del sistema'})
        else: #no hay datos
            return json.dumps({'status':False, 'data':'Credenciales incorrectas o el usuario no existe'})
            
    
    def actualizarToken(self, token, idUsuario):
        #Abrir conexión a la BD
        con = db().open

        #Indicarle a python que los cambios en la BD serán confirmados de manera manual
        con.autocommit = False

        #Crear un cursor
        cursor = con.cursor()

        #Preparar la sentecia SQL para actualizar el token y el esatdo del token en la tabla usuario
        sql = "update usuario set token=%s, estado_token='1' where id=%s"

        try:
            #Ejecutar la sentencia sql
            cursor.execute(sql, [token, idUsuario])

            #Confirmar los datos en la base de datos
            con.commit()

            #Retornar un mensaje confirmar la actualización
            return json.dumps({'status':True, 'data': 'Token actualizado correctamente'})


        except con.Error as error:
            #Revocar los cambios que se hubieran realizado en la base de datos
            con.rollBack()

            #Retornar un mensaje de Error
            return json.dumps({'status':False, 'data': format(error)}, cls=CustomJsonEncoder)

        finally:
            cursor.close()
            con.close()


    def validarEstadoToken(self, idUsuario):
         #Abrir conexión a la BD
        con = db().open

        #Crear un cursor para almacenar el resultado de la consulta SQL, realizada para validar las credenciales
        cursor = con.cursor()

        #Preparar la consulta SQL para validar las credenciales
        sql = "select estado_token from usuario where id=%s"

        #ejecutar la consulta SQL
        cursor.execute(sql, [idUsuario])

        #capturar el resultado de la consulta SQL
        datos = cursor.fetchone()

        #cerrar el cursor de la base de datos y luego cerrar la conexion
        cursor.close()
        con.close()

        #Retornar el resultado
        if datos: #se pregunta si la consulta SQL ha devuelto registros
            return json.dumps({'status': True, 'data': datos}, cls=CustomJsonEncoder)
        else:
            return json.dumps({'status': False, 'data':'No se ha podido acceder al estado del token'})

    def validarEstadoCliente(self,idUsuario):
        con=db().open
        cursor=con.cursor()
        sql="select estado from cliente where id_usuario=%s"
        
         #ejecutar la consulta SQL
        cursor.execute(sql, [idUsuario])

        #capturar el resultado de la consulta SQL
        datos = cursor.fetchone()

        #cerrar el cursor de la base de datos y luego cerrar la conexion
        cursor.close()
        con.close()

        #Retonar una respuesta sobre el inicio de sesión
        if datos: #se pregunta si la consulta SQL ha devuelto registros
            return json.dumps({'status': True, 'data':datos})
        else: #no hay datos
            return json.dumps({'status':False, 'data':'No existe el parámetro de configuración solicitado'})


    def obtnerDiaSemana(self):
        #Abrir conexión a la BD
        con = db().open

        #Crear un cursor para almacenar el resultado de la consulta SQL, realizada para validar las credenciales
        cursor = con.cursor()

        #Preparar la consulta SQL para validar las credenciales
        sql = "SELECT case DAYOFWEEK(CURRENT_TIMESTAMP()) when 2 then 'LUNES' when 3 then 'MARTES' when 4 then 'MIERCOLES' when 5 then 'JUEVES' when 6 then 'VIERNES' when 7 then 'SABADO' when 1 then 'DOMINGO' END DIA"

        #ejecutar la consulta SQL
        cursor.execute(sql)

        #capturar el resultado de la consulta SQL
        datos = cursor.fetchone()

        #cerrar el cursor de la base de datos y luego cerrar la conexion
        cursor.close()
        con.close()

        #Retonar una respuesta sobre el inicio de sesión
        if datos: #se pregunta si la consulta SQL ha devuelto registros
            return json.dumps({'status': True, 'data':datos})
        else: #no hay datos
            return json.dumps({'status':False, 'data':'No existe el parámetro de configuración solicitado'})

        











        





        



