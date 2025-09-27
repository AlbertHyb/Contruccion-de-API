from flask_restful import Resource
from flask import render_template, make_response, request
from config import SUPABASE_URL, SUPABASE_KEY
from supabase import create_client, Client


supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class HelloWorld(Resource):
    def get(self):
        return 'Hola Mundo!'

class InicioDeSesion(Resource):
    def get(self):
        return make_response(render_template('login.html'))
    
    def post(self):
        #Tenemos que capturar los datos del formulario
        correo = request.form.get('email')
        contrasena = request.form.get('password')
        response = supabase.auth.sign_in_with_password({"email": correo, "password": contrasena})
        #Aqui iria la logica de autenticacion
        if response.user:
            return "Inicio de sesion exitoso"
        else:
            return "Inicio de sesion fallido"

class RegistroUsuario(Resource):
    def get(self):
        return make_response(render_template('registro.html'))
    
    def post(self):
        nombre = request.form.get('nobre')
        correo = request.form.get('correo')
        contrasena = request.form.get('password')
        telefono = request.form.get('telefono')

        #Registro en Supabase Auth

        try:
            response = supabase.auth.sign_up({
                "email": correo,
                "password": contrasena,
                "options": {
                    "data": {
                        "nombre": nombre,
                        "telefono": telefono
                    }
                }
            })
            if response.user:
                return "Registro exitoso, por favor verifica tu correo"
            else:
                return "Error en el registro"
        except Exception as e:
            return f"Error en el registro: {str(e)}"
        
        
