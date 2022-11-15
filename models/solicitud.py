from conexionBD import Conexion as db
import json
from util import CustomJsonEncoder

class Solicitud():
    def __init__(self, p_id=None, p_descripcion=None, p_clase=None, p_tipo=None, p_categoria=None, p_peso=None, p_fecha_y_hora_partida=None, p_direccion_partida=None, p_llegada_carga=None,p_distancia=None, p_monto=None,p_id_usuario=None,p_id_tarifa=None):
        self.id = p_id
        self.descripcion = p_descripcion
        self.clase = p_clase
        self.tipo = p_tipo
        self.categoria = p_categoria
        self.peso = p_peso
        self.fecha_y_hora_partida = p_fecha_y_hora_partida
        self.direccion_partida = p_direccion_partida
        self.llegada_carga = p_llegada_carga
        self.distancia = p_distancia
        self.monto = p_monto
        self.id_usuario = p_id_usuario
        self.id_tarifa=p_id_tarifa

    def listarSolicitud(self):
        #Abrir conexión a la BD
        con = db().open

        #Crear un cursor para almacenar el resultado de la consulta SQL, realizada para validar las credenciales
        cursor = con.cursor()

        #Preparar la consulta para mostrar los clientes
        sql = "select * from solicitud order by fecha_y_hora_partida"

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

######listado de olicitudes por cliente
    def listarSolicitudCliente(self, usu_id):
        #Abrir conexión a la BD
        con = db().open

        #Crear un cursor para almacenar el resultado de la consulta SQL, realizada para validar las credenciales
        cursor = con.cursor()

        #Preparar la consulta para mostrar los clientes
        sql = "select id, descripcion, categoria, peso, fecha_y_hora_partida, direccion_partida, llegada_carga,estado,monto, id_usuario from solicitud where id_usuario = %s order by fecha_y_hora_partida"

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


    #Permite insertar nuevos clientes
    def insertar(self):
        #Abrir conexión a la BD
        con = db().open

        #Indicarle a python que los cambios en la BD serán confirmados de manera manual
        con.autocommit = False

        #Crear un cursor
        cursor = con.cursor()

        #Preparar la sentecia SQL para insertar nuevos clientes
        sql = "INSERT solicitud (descripcion, clase, tipo, categoria, peso, fecha_y_hora_partida, direccion_partida, llegada_carga, estado, distancia, monto, id_usuario,id_tarifa) VALUES (%s, %s,%s,%s,%s,%s,%s,%s,'PENDIENTE DE ATENCION',%s,%s,%s,%s)"

        try:
            #Ejecutar la sentencia sql
            cursor.execute(sql, [self.descripcion, self.clase, self.tipo, self.categoria, self.peso, self.fecha_y_hora_partida, self.direccion_partida, self.llegada_carga, self.distancia, self.monto, self.id_usuario,self.id_tarifa])

            #Confirmar los datos en la base de datos
            con.commit()

            #Retornar un mensaje confirmar la actualización
            return json.dumps({'status':True, 'data': 'Solicitud registrada correctamente'})

        except con.Error as error:
            #Revocar los cambios que se hubieran realizado en la base de datos
            con.rollBack()
          
           #Retornar un mensaje de Error
            return json.dumps({'status':False, 'data': format(error)}, cls=CustomJsonEncoder)

        finally:
            cursor.close()
            con.close()

######listado de solicitudes por chofer
    def listarSolicitudChofer(self, usu_id):
        #Abrir conexión a la BD
        con = db().open

        #Crear un cursor para almacenar el resultado de la consulta SQL, realizada para validar las credenciales
        cursor = con.cursor()

        #Preparar la consulta para mostrar los clientes
        sql = "SELECT s.id, s.descripcion, s.clase,s.tipo,s.categoria,s.peso, s.fecha_y_hora_partida,s.direccion_partida,s.llegada_carga,s.estado,s.distancia,s.monto,s.id_usuario AS id_usuario_cliente,c.documento,c.nombre, v.placa, ch.id_chofer, cho.id_usuario AS id_usuario_chofer FROM solicitud s INNER JOIN cliente c ON s.id_usuario=c.id_usuario INNER JOIN detalle_solicitud ds ON ds.id_solicitud=s.id INNER JOIN chofer_vehiculo ch ON ds.id_chofer_vehiculo=ch.id INNER JOIN chofer cho ON cho.id=ch.id_chofer INNER JOIN vehiculo v ON ch.id_vehiculo=v.id WHERE s.estado !='PENDIENTE DE ATENCION' AND s.estado !='FINALIZADO' AND cho.id_usuario=%s"

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

######listado de olicitudes por chofer
    def listarSolicitudGeneralChofer(self, usu_id):
        #Abrir conexión a la BD
        con = db().open

        #Crear un cursor para almacenar el resultado de la consulta SQL, realizada para validar las credenciales
        cursor = con.cursor()

        #Preparar la consulta para mostrar los clientes
        sql = "SELECT s.id, s.descripcion, s.clase,s.tipo,s.categoria,s.peso, s.fecha_y_hora_partida,s.direccion_partida,s.llegada_carga,s.estado,s.distancia,s.monto, v.placa, ch.id_chofer, cho.id_usuario AS id_usuario_chofer FROM solicitud s INNER JOIN detalle_solicitud ds ON ds.id_solicitud=s.id INNER JOIN chofer_vehiculo ch ON ds.id_chofer_vehiculo=ch.id INNER JOIN chofer cho ON cho.id=ch.id_chofer INNER JOIN vehiculo v ON ch.id_vehiculo=v.id WHERE cho.id_usuario=%s order by fecha_y_hora_partida"

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

#anular solictud
    def Estadoanular(self,id_c):
        #Abrir conexión a la BD
        con = db().open

        #Indicarle a python que los cambios en la BD serán confirmados de manera manual
        con.autocommit = False

        #Crear un cursor
        cursor = con.cursor()

        
        try:
            #Preparar la sentecia SQL para actualizar nuevos clientes
            
            sql = "UPDATE solicitud SET estado='ANULADO' WHERE id=%s"
            cursor.execute(sql, [id_c])

            con.commit()

            return json.dumps({'status':True, 'data':'Solicitud anulada correctamente'})

        except con.Error as error:
            con.rollBack()

            return json.dumps({'status':False, 'data':format(error)}, cls=CustomJsonEncoder)

        finally:
            cursor.close()
            con.close()
#### VALIDAR SOLICITUD PENDIENTE DE PAGO
    def obtnerNumValidarPagoPendiente(self, usu_id):
        #Abrir conexión a la BD
        con = db().open

        #Crear un cursor para almacenar el resultado de la consulta SQL, realizada para validar las credenciales
        cursor = con.cursor()

        #Preparar la consulta SQL para validar las credenciales
        sql = "SELECT COUNT(id) as numero FROM solicitud WHERE estado='PENDIENTE DE PAGO' AND monto>=1000 and id_usuario=%s"
        #sql1= "SELECT COUNT(*) AS numero FROM SOLICITUD WHERE  estado='FINALIZADO'"

        #ejecutar la consulta SQL
        cursor.execute(sql,[usu_id])

        #sql1= "#sql1= "SELECT COUNT(*) AS numero FROM SOLICITUD WHERE  estado='FINALIZADO'""
        #cursor.execute(sql1,[usu_id])

        #capturar el resultado de la consulta SQL
        datos = cursor.fetchone()

        #cerrar el cursor de la base de datos y luego cerrar la conexion
        cursor.close()
        con.close()

        #Retonar una respuesta sobre el inicio de sesión
        if datos: #se pregunta si la consulta SQL ha devuelto registros
            return json.dumps({'status': True, 'data':datos['numero']})
        else: #no hay datos
            return json.dumps({'status':False, 'data':'No existe hay registros'})

#### VALIDAR SOLICITUD PENDIENTE DE PAGO
    def obtnerNumSolicitudesFinalizadas(self, usu_id):
        #Abrir conexión a la BD
        con = db().open

        #Crear un cursor para almacenar el resultado de la consulta SQL, realizada para validar las credenciales
        cursor = con.cursor()

        #Preparar la consulta SQL para validar las credenciales
        sql = "SELECT COUNT(*) AS finalizados FROM SOLICITUD WHERE  estado='FINALIZADO'  and id_usuario=%s"
        #sql1= "SELECT COUNT(*) AS numero FROM SOLICITUD WHERE  estado='FINALIZADO'"

        #ejecutar la consulta SQL
        cursor.execute(sql,[usu_id])

        #capturar el resultado de la consulta SQL
        datos = cursor.fetchone()

        #cerrar el cursor de la base de datos y luego cerrar la conexion
        cursor.close()
        con.close()

        #Retonar una respuesta sobre el inicio de sesión
        if datos: #se pregunta si la consulta SQL ha devuelto registros
            return json.dumps({'status': True, 'data':datos['finalizados']})
        else: #no hay datos
            return json.dumps({'status':False, 'data':'No existe hay registros'})