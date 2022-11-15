from conexionBD import Conexion as db
import json
from util import CustomJsonEncoder

class Ubicacion():
    def __init__(self,
                 p_id=None,
                 p_latitud=None,
                 p_longitud=None,
                 p_id_chofer_vehiculo=None):
        self.id = p_id
        self.latitud = p_latitud
        self.longitud = p_longitud
        self.id_chofer_vehiculo = p_id_chofer_vehiculo

    def listarUbicacion(self):
        #Abrir conexión a la BD
        con = db().open

        #Crear un cursor para almacenar el resultado de la consulta SQL, realizada para validar las credenciales
        cursor = con.cursor()

        #Preparar la consulta para mostrar las ubicaciones
        sql = "select * from ubicacion"

        #ejecutar la consulta SQL
        cursor.execute(sql)

        #capturar el resultado de la consulta SQL
        datos = cursor.fetchall()

        #cerrar el cursor de la base de datos y luego cerrar la conexion
        cursor.close()
        con.close()

        #Retornar el resultado
        if (datos):  #se pregunta si la consulta SQL ha devuelto registros
            return json.dumps({'status': True, 'data': datos},cls=CustomJsonEncoder)
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
        sql = "insert into ubicacion (latitud,longitud,id_chofer_vehiculo) values (%s,%s,%s)"
        try:
            #Ejecutar la sentencia sql
            cursor.execute(sql, [self.latitud, self.longitud, self.id_chofer_vehiculo])

            #Confirmar los datos en la base de datos
            con.commit()

            #Retornar un mensaje confirmar la actualización
            return json.dumps({
                'status': True,
                'data': 'Ubicación registrada correctamente'
            })

        except con.Error as error:
            #Revocar los cambios que se hubieran realizado en la base de datos
            con.rollBack()
          
           #Retornar un mensaje de Error
            return json.dumps({'status':False, 'data': format(error)}, cls=CustomJsonEncoder)

        finally:
            cursor.close()
            con.close()


