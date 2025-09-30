from unittest import result
from flask_restful import Resource
from flask import render_template, make_response, request
from supabase import create_client, Client



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
        nombre = request.form.get('nombre')
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
                #Guardar informacion adicional en la tabla "usuarios"
                auth_id = response.user.id
                data, error = supabase.table("usuarios").insert({
                    "auth_id": auth_id,
                    "nombre": nombre,
                    "correo": correo,
                    "telefono": telefono
                }).execute()
                if result.error:
                    return "Error al guardar datos adicionales: {result.error}"
                return "Registro exitoso, por favor verifica tu correo"
            else:
                return "Error en el registro"
        except Exception as e:
            return f"Excepcion durante el registro: {str(e)}"    
               
        
        
