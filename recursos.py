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

        

            if response.user:
                #Guardar informacion adicional en la tabla "usuarios"
                auth_id = response.user.id

                # Datos que vamos a insertar
                datos_insertar = {
                    "auth_id": auth_id,
                    "nombre": nombre,
                    "correo": correo,
                    "telefono": telefono_limpio
                }
                
                try:
                    result = supabase.table("usuarios").insert(datos_insertar).execute()
                    
                
                    
                    if hasattr(result, 'error') and result.error:
                        return f"Error al guardar: {result.error}"
                    
                    if result.data and len(result.data) > 0:
                        return "Registro exitoso, usuario guardado en base de datos"
                    else:
                        return f"Usuario creado en Auth pero no se guardó en tabla usuarios. Resultado: {result}"
                        
                except Exception as tabla_error:
                    return f"Error al insertar en tabla usuarios: {str(tabla_error)}"
            else:
                return f"Error en el registro: {response}"
        except Exception as e:
            return f"Excepcion durante el registro: {str(e)}"
        
class PerfilUsuario(Resource):
    def get(self):
        try:
        
            # Obtener datos actuales del usuario
            result = supabase.table("usuarios").select("*").limit(1).execute()
            
            usuario_data = {}
            if result.data and len(result.data) > 0:
                usuario_data = result.data[0]
            
            return make_response(render_template('perfil.html', usuario=usuario_data))
        except Exception as e:
            return make_response(render_template('perfil.html', error=f"Error al cargar perfil: {str(e)}"))
          
    
    def post(self):
        # Capturar datos del formulario (nombres consistentes con el HTML)
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validaciones basicas
        if not email or not username:
            return "Error: El nombre de usuario y correo son obligatorios"

        # Validar contraseña si se proporciona
        if password:
            if len(password) < 6:
                return "Error: La contraseña debe tener al menos 6 caracteres"
            if password != confirm_password:
                return "Error: Las contraseñas no coinciden"

        try:

            # Buscar usuario por correo para obtener su ID
            buscar_usuario = supabase.table("usuarios").select("*").eq("correo", email).execute()
            
            if not buscar_usuario.data or len(buscar_usuario.data) == 0:
                return "Error: No se encontró un usuario con ese correo"

            usuario_id = buscar_usuario.data[0]['id']
            
            datos_actualizar = {
                "nombre": username,
                "correo": email
            }

            # Actualizar usando el ID del usuario
            result = supabase.table("usuarios").update(datos_actualizar).eq("id", usuario_id).execute()

            if hasattr(result, 'error') and result.error:
                return f"Error al actualizar perfil: {result.error}"

            return "Perfil actualizado exitosamente"
                
        except Exception as e:
            return f"Error durante la actualización del perfil: {str(e)}"
            

            # Si se proporcionó nueva contraseña, actualizarla en Supabase Auth
            if password:
                try:
                    # Actualizar contraseña en Supabase Auth
                    auth_response = supabase.auth.update_user({
                        "password": password
                    })
                    
                    if hasattr(auth_response, 'error') and auth_response.error:
                        return f"Perfil actualizado, pero error al cambiar contraseña: {auth_response.error}"
                        
                except Exception as auth_error:
                    return f"Perfil actualizado, pero error al cambiar contraseña: {str(auth_error)}"

            if result.data and len(result.data) > 0:
                return "Perfil actualizado exitosamente"
            else:
                return f"No se encontró el usuario para actualizar"
                
        except Exception as e:
            return f"Error durante la actualización del perfil: {str(e)}"
        