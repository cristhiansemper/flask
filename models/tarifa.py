#from msilib.schema import Error
#from sqlalchemy import delete, insert
from conexionBD import Conexion as db
import json
from util import CustomJsonEncoder

class Tarifa():
    def __init__(self, p_id=None, p_valor=None):
        self.id = p_id
        self.valor = p_valor

    def obtenerValorTarifa(self):
        #Abrir conexión a la BD
        con = db().open

        #Crear un cursor para almacenar el resultado de la consulta SQL, realizada para validar las credenciales
        cursor = con.cursor()

        #Preparar la consulta SQL para validar las credenciales
        sql = "select id,valor from tarifa where id =(SELECT MAX(id) FROM tarifa)"

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
            
    def insertar(self):
            #Abrir conexión a la BD
            con = db().open

            #Indicarle a python que los cambios en la BD serán confirmados de manera manual
            con.autocommit = False

            #Crear un cursor
            cursor = con.cursor()

            #Preparar la sentecia SQL para insertar nuevos clientes
            sql = "insert into tarifa(valor) values (%s)"

            try:
                #Ejecutar la sentencia sql
                cursor.execute(sql, [self.valor])

                #Confirmar los datos en la base de datos
                con.commit()

                #Retornar un mensaje confirmar la actualización
                return json.dumps({'status':True, 'data': 'Tarifa registrada correctamente'})


            except con.Error as error:
                #Revocar los cambios que se hubieran realizado en la base de datos
                con.rollBack()

                #Retornar un mensaje de Error
                return json.dumps({'status':False, 'data': format(error)}, cls=CustomJsonEncoder)

            finally:
                cursor.close()
                con.close()