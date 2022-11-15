from conexionBD import Conexion as db
import json
from util import CustomJsonEncoder

class Vehiculo():
    def __init__(self, p_id=None, p_placa=None, p_peso_maximo=None):
        self.id = p_id
        self.placa = p_placa
        self.peso_maximo = p_peso_maximo

    def listarVehiculo(self):
        #Abrir conexión a la BD
        con = db().open

        #Crear un cursor para almacenar el resultado de la consulta SQL, realizada para validar las credenciales
        cursor = con.cursor()

        #Preparar la consulta para mostrar los clientes
        sql = "select v.id, v.placa, v.peso_maximo, v.estado from vehiculo v order by v.placa"

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

    
    #Permite insertar nuevos clientes
    def insertar(self):
        #Abrir conexión a la BD
        con = db().open

        #Indicarle a python que los cambios en la BD serán confirmados de manera manual
        con.autocommit = False

        #Crear un cursor
        cursor = con.cursor()

        #Preparar la sentecia SQL para insertar nuevos clientes
        sql = "insert into vehiculo(id, placa, peso_maximo, estado) values (%s,%s,%s,1)"

        try:
            #Ejecutar la sentencia sql
            cursor.execute(sql, [self.id, self.placa, self.peso_maximo])

            #Confirmar los datos en la base de datos
            con.commit()

            #Retornar un mensaje confirmar la actualización
            return json.dumps({'status':True, 'data': 'Vehículo registrado correctamente'})


        except con.Error as error:
            #Revocar los cambios que se hubieran realizado en la base de datos
            con.rollBack()

            #Retornar un mensaje de Error
            return json.dumps({'status':False, 'data': format(error)}, cls=CustomJsonEncoder)

        finally:
            cursor.close()
            con.close()

    def listarVehiculoLibres(self):
        #Abrir conexión a la BD
        con = db().open

        #Crear un cursor para almacenar el resultado de la consulta SQL, realizada para validar las credenciales
        cursor = con.cursor()

        #Preparar la consulta para mostrar los clientes
        sql = "SELECT id,placa,peso_maximo FROM vehiculo WHERE id NOT IN (SELECT id_vehiculo FROM chofer_vehiculo) ORDER BY peso_maximo"

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
