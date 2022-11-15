from conexionBD import Conexion as db
import json
from util import CustomJsonEncoder

class Chofer():
  def __init__(self, p_id=None, p_documento=None, p_nombres=None,p_telefono=None,p_direccion=None,p_usuario_id=None):
    self.id=p_id
    self.documento=p_documento
    self.nombres=p_nombres
    self.telefono=p_telefono
    self.direccion=p_direccion
    self.usuario_id=p_usuario_id
    
  def listarChofer(self):
    #Abrir conexion a la BD
    con = db().open

    #Crear un cursor para almacenar el resultado de la consulta
    cursor = con.cursor()

    #preparar la consulta
    sql="select * from chofer order by nombres"

    cursor.execute(sql)

    datos = cursor.fetchall()

    cursor.close()
    con.close()

    if(datos): 
      return json.dumps({'status':True,'data':datos}, cls=CustomJsonEncoder)
    else:
      return json.dumps({'status':False,'data':'No hay registros'})

  def insertar(self):
    con = db().open
    con.autocommit= False
    cursor = con.cursor()

    sql = "insert into chofer(documento,nombres,telefono, direccion, estado, id_usuario) values (%s,%s,%s,%s,'1',%s)"

    try:
      cursor.execute(sql, [self.documento, self.nombres, self.telefono, self.direccion, self.usuario_id])
      con.commit()
      return json.dumps({'status':True, 'data':'Chofer registrado correctamente'})

    except con.Error as error:
      con.rollBack()
      return json.dumps({'status':False, 'data':format(error)}, cls=CustomJsonEncoder)

    finally:
      cursor.close()
      con.close()

  def listarChoferLibre(self):
    #Abrir conexion a la BD
    con = db().open

    #Crear un cursor para almacenar el resultado de la consulta
    cursor = con.cursor()

    #preparar la consulta
    sql="SELECT id,nombres,documento, id_usuario FROM chofer WHERE id NOT IN (SELECT id_chofer FROM chofer_vehiculo) ORDER BY nombres"

    cursor.execute(sql)

    datos = cursor.fetchall()

    cursor.close()
    con.close()

    if(datos): 
      return json.dumps({'status':True,'data':datos}, cls=CustomJsonEncoder)
    else:
      return json.dumps({'status':False,'data':'No hay registros'})