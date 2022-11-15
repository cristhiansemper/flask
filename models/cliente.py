from conexionBD import Conexion as db
import json
from util import CustomJsonEncoder


class Cliente():
    def __init__(self,
                 p_id=None,
                 p_tipo_documento=None,
                 p_documento=None,
                 p_nombre=None,
                 p_direccion=None,
                 p_email=None,
                 p_telefono=None,
                 p_usuario_id=None):
        self.id = p_id
        self.tipo_documento = p_tipo_documento
        self.documento = p_documento
        self.nombre = p_nombre
        self.direccion = p_direccion
        self.email = p_email
        self.telefono = p_telefono
        self.usuario_id=p_usuario_id

    def listarCliente(self):
        #Abrir conexión a la BD
        con = db().open

        #Crear un cursor para almacenar el resultado de la consulta SQL, realizada para validar las credenciales
        cursor = con.cursor()

        #Preparar la consulta para mostrar los clientes
        sql = "select * from cliente order by nombre"

        #ejecutar la consulta SQL
        cursor.execute(sql)

        #capturar el resultado de la consulta SQL
        datos = cursor.fetchall()

        #cerrar el cursor de la base de datos y luego cerrar la conexion
        cursor.close()
        con.close()

        #Retornar el resultado
        if (datos):  #se pregunta si la consulta SQL ha devuelto registros
            return json.dumps({
                'status': True,
                'data': datos
            },
                              cls=CustomJsonEncoder)
        else:
            return json.dumps({'status': False, 'data': 'No hay registros'})

    #Permite insertar nuevos clientes
    def insertar(self):
        #Abrir conexión a la BD
        con = db().open

        #Indicarle a python que los cambios en la BD serán confirmados de manera manual
        con.autocommit = False

        #Crear un cursor
        cursor = con.cursor()

        #Preparar la sentecia SQL para insertar nuevos clientes
        sql = "insert into cliente (tipo_documento, documento, nombre, direccion, email, telefono, estado, id_usuario) values (%s,%s,%s,%s,%s,%s,'P',%s)"

        try:
            #Ejecutar la sentencia sql
            cursor.execute(sql, [
                self.tipo_documento, self.documento, self.nombre,
                self.direccion, self.email, self.telefono,self.usuario_id])

            #Confirmar los datos en la base de datos
            con.commit()

            #Retornar un mensaje confirmar la actualización
            return json.dumps({
                'status': True,
                'data': 'Cliente registrado correctamente'
            })

        except con.Error as error:
            #Revocar los cambios que se hubieran realizado en la base de datos
            con.rollBack()

            #Retornar un mensaje de Error
            return json.dumps({
                'status': False,
                'data': format(error)
            },
                              cls=CustomJsonEncoder)

        finally:
            cursor.close()
            con.close()


#Permite insertar nuevos clientes
    def updateEstado(self, est, id_c):
        #Abrir conexión a la BD
        con = db().open

        #Indicarle a python que los cambios en la BD serán confirmados de manera manual
        con.autocommit = False

        #Crear un cursor
        cursor = con.cursor()

        
        try:
            #Preparar la sentecia SQL para actualizar nuevos clientes
            
            sql = "UPDATE cliente SET estado=%s WHERE id=%s"
            cursor.execute(sql, [est,id_c])

            con.commit()

            return json.dumps({'status':True, 'data':'Cliente modificado correctamente'})

        except con.Error as error:
            con.rollBack()

            return json.dumps({'status':False, 'data':format(error)}, cls=CustomJsonEncoder)

        finally:
            cursor.close()
            con.close()

    def listarClienteFiltro(self,est,tdoc,nom):
        #Abrir conexión a la BD
        con = db().open

        #Crear un cursor para almacenar el resultado de la consulta SQL, realizada para validar las credenciales
        cursor = con.cursor()

        #Preparar la consulta para mostrar los clientes
        sql = "SELECT * FROM cliente WHERE estado=%s OR tipo_documento=%s OR nombre=%s"

        #ejecutar la consulta SQL
        cursor.execute(sql,[est,tdoc,nom])

        #capturar el resultado de la consulta SQL
        datos = cursor.fetchall()

        #cerrar el cursor de la base de datos y luego cerrar la conexion
        cursor.close()
        con.close()

        #Retornar el resultado
        if (datos):  #se pregunta si la consulta SQL ha devuelto registros
            return json.dumps({
                'status': True,
                'data': datos
            },
                              cls=CustomJsonEncoder)
        else:
            return json.dumps({'status': False, 'data': 'No hay registros'})