from conexionBD import Conexion as db
import json
from util import CustomJsonEncoder

class Chofer_Vehiculo():
    def __init__(self, p_id=None, p_id_vehiculo=None, p_id_chofer=None):
        self.id = p_id
        self.id_vehiculo = p_id_vehiculo
        self.id_chofer = p_id_chofer
      
    def listarChofer_vehiculo(self):
        #Abrir conexión a la BD
        con = db().open

        #Crear un cursor para almacenar el resultado de la consulta SQL, realizada para validar las credenciales
        cursor = con.cursor()

        #Preparar la consulta para mostrar los detalles
        sql="select * from chofer_vehiculo order by id_chofer"

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

    
    #Permite insertar nuevos detalles
    def insertar(self):
        #Abrir conexión a la BD
        con = db().open

        #Indicarle a python que los cambios en la BD serán confirmados de manera manual
        con.autocommit = False

        #Crear un cursor
        cursor = con.cursor()

        #Preparar la sentecia SQL para insertar detalles
        sql = "insert into chofer_vehiculo (id_vehiculo, id_chofer, estado) values (%s,%s,'ACTIVO')"

        
        try:
            #Ejecutar la sentencia sql
            cursor.execute(sql, [self.id_vehiculo, self.id_chofer])
            usuario_id = con.insert_id()
            #Confirmar los datos en la base de datos
            con.commit()

            #Retornar un mensaje confirmar la actualización
            return json.dumps({'status':True, 'data': 'Detalle de chofer_vehiculo registrado correctamente','id':usuario_id})


        except con.Error as error:
            #Revocar los cambios que se hubieran realizado en la base de datos
            con.rollBack()
          
           #Retornar un mensaje de Error
            return json.dumps({'status':False, 'data': format(error)}, cls=CustomJsonEncoder)

        finally:
            cursor.close()
            con.close()


