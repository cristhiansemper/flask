from conexionBD import Conexion as db
import json
from util import CustomJsonEncoder
class Usuario():
    def __init__(self, p_id=None, p_nombre=None, p_contrasena=None,  p_tipo_usuario=None):
        self.id = p_id
        self.nombre = p_nombre
        self.contrasena = p_contrasena
        self.tipo_usuario = p_tipo_usuario
   
      
    def listarUsuario(self):
        #Abrir conexión a la BD
        con = db().open

        #Crear un cursor para almacenar el resultado de la consulta SQL, realizada para validar las credenciales
        cursor = con.cursor()

        #Preparar la consulta para mostrar los clientes
        sql = "select u.id, u.usuario, u.contrasena, u.estado, u.token, u.tipo_usuario from usuario u  order by u.usuario"

        #ejecutar la consulta SQL
        cursor.execute(sql)

        #capturar el resultado de la consulta SQL
        datos = cursor.fetchall()

        #cerrar el cursor de la base de datos y luego cerrar la conexion
        cursor.close()
        con.close()
         #Retornar el resultado
        if (datos): #se pregunta si la consulta SQL ha devuelto registros
            return json.dumps({'status': True, 'data': datos}, cls=CustomJsonEncoder)
        else:
            return json.dumps({'status': False, 'data':'No hay registros'})

    
    #Permite insertar nuevos pagos
    def insertar(self):
        #Abrir conexión a la BD
        con = db().open

        #Indicarle a python que los cambios en la BD serán confirmados de manera manual
        con.autocommit = False

        #Crear un cursor
        cursor = con.cursor()

        #Preparar la sentecia SQL para insertar nuevos clientes
        sql = "insert into usuario(usuario, contrasena,estado,tipo_usuario) values (%s,%s,1,%s)"

        try:
            #Ejecutar la sentencia sql
            cursor.execute(sql, [self.nombre, self.contrasena, self.tipo_usuario])
            #Obtener el id del usuario
            usuario_id = con.insert_id()

            #Confirmar los datos en la base de datos
            con.commit()

            #Retornar un mensaje confirmar la actualización
            return json.dumps({'status':True, 'data': 'Usuario registrado correctamente', 'id':usuario_id})


        except con.Error as error:
            #Revocar los cambios que se hubieran realizado en la base de datos
            con.rollBack()
          
           #Retornar un mensaje de Error
            return json.dumps({'status':False, 'data': format(error)}, cls=CustomJsonEncoder)

        finally:
            cursor.close()
            con.close()

