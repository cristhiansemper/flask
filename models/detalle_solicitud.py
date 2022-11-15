from conexionBD import Conexion as db
import json
from util import CustomJsonEncoder

class Detalle_Solicitud():
  def __init__(self, p_id=None,p_id_chofer_vehiculo=None,p_id_solicitud=None):
    self.id=p_id
    self.id_chofer_vehiculo=p_id_chofer_vehiculo
    self.id_solicitud=p_id_solicitud

  def listarDetalleSolicitud(self):
    con=db().open
    cursor=con.cursor()
    sql="select * from detalle_solicitud"
    cursor.execute(sql)
    datos=cursor.fetchall()
    cursor.close()
    con.close()

    if(datos):
      return json.dumps({'status': True, 'data':datos},cls=CustomJsonEncoder)
    else:
      return json.dumps({'status':False,'data':'No hay registros'})

  def insertar(self):
    con=db().open
    con.autocommit=False
    cursor = con.cursor()
    sql="insert into detalle_solicitud(id_chofer_vehiculo,id_solicitud) values (%s,%s)"
    sql1 = "update solicitud set estado='VEHICULO ASIGNADO' where id=%s"
    try:
      cursor.execute(sql,[self.id_chofer_vehiculo,self.id_solicitud])
      cursor.execute(sql1,[self.id_solicitud])
      con.commit()
      return json.dumps({'status':True,'data':'Detalle_Solicitud registrada correctamente'})
      
    except con.Error as error:
      con.rollBack()
      return json.dumps({'status':False,'data': format(error)},cls=CustomJsonEncoder)

    finally:
      cursor.close()
      con.close()
