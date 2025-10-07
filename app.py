from flask import Flask
from flask_restful import Resource, Api
from routes import RutasAPI
import config


#Estamos creando una instancia/objeto de Flask
app = Flask(__name__)
api = Api(app)

#
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI

#El objeto "app" es el que me va a permitir manejar el servidor

#Y una instancia /objeto de API(flask_restful)
api =Api(app)

#Iniciamos rutas
rutas_api = RutasAPI()
rutas_api.inicializar_rutas(api)

#Me va apermitir controlar los recursos que voy a exponer 

app.run(debug=True, port=5000)  #Ejecuta el servidor en el puerto 5000

#debug=True Para que se reinicie automaticamente el servidor cuando haya cambios
#port=5000 Para definir el puerto en el que se ejecuta el servidor