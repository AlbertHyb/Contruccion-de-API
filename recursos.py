from flask_restful import Resource
from flask import render_template, make_response, request
from config import supabase




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

        # Validaciones
        if not contrasena or len(contrasena) < 6:
            return "Error: La contraseña debe tener al menos 6 caracteres"
        
        if not correo or not nombre or not telefono:
            return "Error: Todos los campos son obligatorios"

        # Limpiar el teléfono (quitar espacios y caracteres especiales)
        telefono_limpio = ''.join(filter(str.isdigit, telefono))

        print(f"Datos recibidos - Nombre: {nombre}, Correo: {correo}, Teléfono: {telefono} -> Limpio: {telefono_limpio}")

        #Registro en Supabase Auth
        try:
            response = supabase.auth.sign_up({
                "email": correo,
                "password": contrasena,
                "options": {
                    "data": {
                        "nombre": nombre,
                        "telefono": telefono_limpio
                    }
                }
            })

            print(f"Respuesta Auth: {response}")
            print(f"Usuario creado: {response.user}")

            if response.user:
                #Guardar informacion adicional en la tabla "usuarios"
                auth_id = response.user.id
                print(f"🔑 Auth ID: {auth_id}")

                # Datos que vamos a insertar
                datos_insertar = {
                    "auth_id": auth_id,
                    "nombre": nombre,
                    "correo": correo,
                    "telefono": telefono_limpio
                }
                print(f"Datos a insertar: {datos_insertar}")

                try:
                    result = supabase.table("usuarios").insert(datos_insertar).execute()
                    
                    print(f"Resultado completo: {result}")
                    print(f"Data insertada: {result.data}")
                    print(f"Count: {result.count}")
                    
                    if hasattr(result, 'error') and result.error:
                        print(f"Error en inserción: {result.error}")
                        return f"Error al guardar: {result.error}"
                    
                    if result.data and len(result.data) > 0:
                        return "Registro exitoso, usuario guardado en base de datos"
                    else:
                        return f"Usuario creado en Auth pero no se guardó en tabla usuarios. Resultado: {result}"
                        
                except Exception as tabla_error:
                    print(f"Excepción al insertar en tabla: {tabla_error}")
                    return f"Error al insertar en tabla usuarios: {str(tabla_error)}"
            else:
                return f"Error en el registro: {response}"
        except Exception as e:
            print(f"Excepción: {e}")
            return f"Excepcion durante el registro: {str(e)}"