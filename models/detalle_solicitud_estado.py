from conexionBD import Conexion as db
import json
from util import CustomJsonEncoder

class DetalleSolicitudEstado():
    def __init__(self, p_id = None, p_estado=None, p_observacion=None, p_id_detalle_solicitud=None):
        self.id=p_id
        self.estado=p_estado
        self.observacion=p_observacion
        self.id_detalle_solicitud=p_id_detalle_solicitud

#Permite insertar nuevos estados de solicitud
    def insertar(self):
        #Abrir conexión a la BD
        con = db().open

        #Indicarle a python que los cambios en la BD serán confirmados de manera manual
        con.autocommit = False

        #Crear un cursor
        cursor = con.cursor()

        #Preparar la sentecia SQL para insertar nuevos clientes
        sql = "INSERT detalle_solicitud_estado (estado, observacion, id_detalle_solicitud) VALUES (%s,%s,%s)"

        try:
            #Ejecutar la sentencia sql
            cursor.execute(sql, [self.estado, self.observacion, self.id_detalle_solicitud])

            #Confirmar los datos en la base de datos
            con.commit()

            #Retornar un mensaje confirmar la actualización
            return json.dumps({'status':True, 'data': 'Detalle de estado de la solicitud registrada correctamente'})

        except con.Error as error:
            #Revocar los cambios que se hubieran realizado en la base de datos
            con.rollBack()
          
           #Retornar un mensaje de Error
            return json.dumps({'status':False, 'data': format(error)}, cls=CustomJsonEncoder)

        finally:
            cursor.close()
            con.close()

######listado de pagos por cliente
    def listarReportesSolicitud(self, sol_id):
        #Abrir conexión a la BD
        con = db().open

        #Crear un cursor para almacenar el resultado de la consulta SQL, realizada para validar las credenciales
        cursor = con.cursor()

        #Preparar la consulta para mostrar los clientes
        #sql = "select p.id, p.entidad_financiera, p.numero_operacion, p.fecha_y_hora_operacion, p.estado, p.monto, p.solicitud_id, CONCAT('/static/imgs-producto/', '2.jpg') AS img from pago p  inner join solicitud s on p.solicitud_id = s.id  where s.id_usuario = %s order by fecha_y_hora_partida"
        sql = "SELECT dse.id, dse.estado, dse.fecha_y_hora, dse.observacion FROM detalle_solicitud_estado dse INNER JOIN detalle_solicitud ds ON  ds.id=dse.id_detalle_solicitud INNER JOIN solicitud s ON ds.id_solicitud=s.id WHERE s.id=%s ORDER BY dse.fecha_y_hora DESC"
        #ejecutar la consulta SQL
        cursor.execute(sql,[sol_id])

        #capturar el resultado de la consulta SQL
        datos = cursor.fetchall()

        #cerrar el cursor de la base de datos y luego cerrar la conexion
        cursor.close()
        con.close()

        #Retornar el resultado
        if (datos): #se pregunta si la consulta SQL ha devuelto registros
            return json.dumps({'status': True, 'data': datos}, cls=CustomJsonEncoder)
        else:
            return json.dumps({'status': False, 'data':'No hay reportes de estado de esa solicitud'})