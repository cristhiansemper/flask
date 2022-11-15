from flask import Flask

#Importar a los módulos que contienen a los servicios web
from ws.sesion import ws_sesion
from ws.vehiculo import ws_vehiculo 
from ws.chofer import ws_chofer
from ws.chofer_vehiculo import ws_chofer_vehiculo
from ws.cliente import ws_cliente
from ws.detalle_solicitud import ws_detalle_solicitud
from ws.pago import ws_pago
from ws.solicitud import ws_solicitud
from ws.ubicacion import ws_ubicacion
from ws.usuario import ws_usuario
from ws.tarifa import ws_tarifa
from ws.detalle_solicitud_estado import ws_detalle_solicitud_estado


#Crear la variable de aplicación con Flask
app = Flask(__name__)


#Registrar los módulos que contienen a los servicios web
app.register_blueprint(ws_sesion)
app.register_blueprint(ws_vehiculo)
app.register_blueprint(ws_chofer)
app.register_blueprint(ws_cliente)
app.register_blueprint(ws_chofer_vehiculo)
app.register_blueprint(ws_detalle_solicitud)
app.register_blueprint(ws_pago)
app.register_blueprint(ws_solicitud)
app.register_blueprint(ws_ubicacion)
app.register_blueprint(ws_usuario)
app.register_blueprint(ws_tarifa)
app.register_blueprint(ws_detalle_solicitud_estado)


@app.route('/')
def home():
    return 'Servicios web en ejecución'

#Iniciar el servicio web con Flask
if __name__ == '__main__':
    app.run(port=os.getenv("PORT", default=5000), debug=True)
