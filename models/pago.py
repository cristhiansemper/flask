from conexionBD import Conexion as db
import json
from util import CustomJsonEncoder

class Pago():
    def __init__(self, p_id=None, p_entidad_financiera=None, p_numero_operacion=None, p_fecha_hora_operacion=None, p_monto=None,p_observacion=None,p_voucher=None,p_solicitud_id=None):
        self.id = p_id
        self.entidad_financiera = p_entidad_financiera
        self.numero_operacion = p_numero_operacion
        self.fecha_hora_operacion = p_fecha_hora_operacion
        self.monto = p_monto
        self.observacion = p_observacion
        self.voucher=p_voucher
        self.solicitud_id = p_solicitud_id 

    def listarPago(self):
        #Abrir conexión a la BD
        con = db().open

        #Crear un cursor para almacenar el resultado de la consulta SQL, realizada para validar las credenciales
        cursor = con.cursor()

        #Preparar la consulta para mostrar los pagos
        sql = "select id, entidad_financiera, numero_operacion, fecha_y_hora_operacion, estado, monto, observacion, solicitud_id, CONCAT('/static/imgs-producto/', id, '.jpg') AS img from pago pg order by fecha_y_hora_operacion"
        
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

######listado de pagos por cliente
    def listarPagoCliente(self, usu_id):
        #Abrir conexión a la BD
        con = db().open

        #Crear un cursor para almacenar el resultado de la consulta SQL, realizada para validar las credenciales
        cursor = con.cursor()

        #Preparar la consulta para mostrar los clientes
        #sql = "select p.id, p.entidad_financiera, p.numero_operacion, p.fecha_y_hora_operacion, p.estado, p.monto, p.solicitud_id, CONCAT('/static/imgs-producto/', '2.jpg') AS img from pago p  inner join solicitud s on p.solicitud_id = s.id  where s.id_usuario = %s order by fecha_y_hora_partida"
        sql = "select p.id, p.entidad_financiera, p.numero_operacion, p.fecha_y_hora_operacion, p.estado, p.monto, p.solicitud_id, voucher from pago p  inner join solicitud s on p.solicitud_id = s.id  where s.id_usuario = %s order by fecha_y_hora_partida"
        #ejecutar la consulta SQL
        cursor.execute(sql,[usu_id])

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

        #Preparar la sentecia SQL para insertar pago
        sql = "insert into pago (entidad_financiera, numero_operacion, fecha_y_hora_operacion, estado, monto, observacion, voucher, solicitud_id) values (%s,%s,%s,'P',%s,%s,%s,%s)"

        try:
            #Ejecutar la sentencia sql
            cursor.execute(sql, [self.entidad_financiera, self.numero_operacion, self.fecha_hora_operacion, self.monto, self.observacion,self.voucher, self.solicitud_id])

            #Confirmar los datos en la base de datos
            con.commit()

            #Retornar un mensaje confirmar la actualización
            return json.dumps({'status':True, 'data': 'Pago registrado correctamente'})


        except con.Error as error:
            #Revocar los cambios que se hubieran realizado en la base de datos
            con.rollBack()
          
           #Retornar un mensaje de Error
            return json.dumps({'status':False, 'data': format(error)}, cls=CustomJsonEncoder)

        finally:
            cursor.close()
            con.close()

#anular solictud
    def Pagovalidar(self,est,id_c):
        #Abrir conexión a la BD
        con = db().open

        #Indicarle a python que los cambios en la BD serán confirmados de manera manual
        con.autocommit = False

        #Crear un cursor
        cursor = con.cursor()
        
        try:
            #Preparar la sentecia SQL para actualizar nuevos clientes
            
            sql = "UPDATE pago SET estado=%s WHERE solicitud_id=%s"
            cursor.execute(sql, [est,id_c])

            con.commit()

            return json.dumps({'status':True, 'data':'PAGO Validado correctamente'})

        except con.Error as error:
            con.rollBack()

            return json.dumps({'status':False, 'data':format(error)}, cls=CustomJsonEncoder)

        finally:
            cursor.close()
            con.close()

##### ver voucher
    def listarvoucher(self,id_sol):

        #Abrir conexión a la BD
        con = db().open

        #Indicarle a python que los cambios en la BD serán confirmados de manera manual
        con.autocommit = False


        #Crear un cursor para almacenar el resultado de la consulta SQL, realizada para validar las credenciales
        cursor = con.cursor()

        #Preparar sql
        sql="SELECT voucher FROM pago WHERE solicitud_id=%s"

        #ejecutar la consulta SQL
        cursor.execute(sql,[id_sol])

        #capturar el resultado de la consulta SQL
        datos = cursor.fetchone()

        #cerrar el cursor de la base de datos y luego cerrar la conexion
        cursor.close()
        con.close()

        #Retornar el resultado
        if (datos): #se pregunta si la consulta SQL ha devuelto registros
            return json.dumps({'status': True, 'data': datos['voucher']}, cls=CustomJsonEncoder)
        else:
            return json.dumps({'status': False, 'data':'No hay registros'})