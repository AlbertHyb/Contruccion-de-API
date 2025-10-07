from flask_restful import Resource
from flask import render_template, make_response, request, jsonify
from config import supabase
from jwt_config import jwt_manager, token_required, refresh_token_required
import bcrypt

class HelloWorld(Resource):
    def get(self):
        return 'Hola Mundo!'

class InicioDeSesion(Resource):
    def get(self):
        return make_response(render_template('login.html'))
    
    def post(self):
        correo = request.form.get('email')
        contrasena = request.form.get('password')
        
        if not correo or not contrasena:
            return jsonify({'error': 'Email y contraseña son requeridos'}), 400
        
        try:
            # Autenticar con Supabase
            response = supabase.auth.sign_in_with_password({
                "email": correo, 
                "password": contrasena
            })
            
            if response.user:
                user_id = response.user.id
                
                # Generar tokens usando jwt_manager
                access_token = jwt_manager.generar_access_token(user_id, correo)
                refresh_token = jwt_manager.generar_refresh_token(user_id, correo)
                
                return jsonify({
                    'mensaje': 'Inicio de sesión exitoso',
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'usuario': {
                        'id': user_id,
                        'email': correo
                    }
                }), 200
            else:
                return jsonify({'error': 'Credenciales inválidas'}), 401
                
        except Exception as e:
            return jsonify({'error': f'Error en autenticación: {str(e)}'}), 500

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
            return jsonify({'error': 'La contraseña debe tener al menos 6 caracteres'}), 400
        
        if not correo or not nombre or not telefono:
            return jsonify({'error': 'Todos los campos son obligatorios'}), 400

        

        try:

            telefono_limpio = ''.join(filter(str.isdigit, telefono))


            # Registro en Supabase
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
                auth_id = response.user.id
                
                # Guardar en tabla usuarios
                datos_insertar = {
                    "auth_id": auth_id,
                    "nombre": nombre,
                    "correo": correo,
                    "telefono": telefono_limpio
                }
                
                result = supabase.table("usuarios").insert(datos_insertar).execute()
                
                if result.data:
                    # Generar tokens para usuario recién registrado
                    access_token = jwt_manager.generar_access_token(auth_id, correo)
                    refresh_token = jwt_manager.generar_refresh_token(auth_id, correo)
                    
                    return jsonify({
                        'mensaje': 'Registro exitoso',
                        'access_token': access_token,
                        'refresh_token': refresh_token,
                        'usuario': {
                            'id': auth_id,
                            'email': correo,
                            'nombre': nombre
                        }
                    }), 201
                else:
                    return jsonify({'error': 'Error al guardar usuario en base de datos'}), 500
            else:
                return jsonify({'error': 'Error en el registro'}), 400
                
        except Exception as e:
            return jsonify({'error': f'Error durante el registro: {str(e)}'}), 500

class PerfilUsuario(Resource):
    @token_required
    def get(self):
        try:
            user_id = request.current_user['user_id']
            
            # Obtener datos del usuario
            result = supabase.table("usuarios").select("*").eq("auth_id", user_id).execute()
            
            if result.data and len(result.data) > 0:
                usuario = result.data[0]
                # No enviar datos sensibles
                usuario_seguro = {
                    'id': usuario.get('id'),
                    'nombre': usuario.get('nombre'),
                    'correo': usuario.get('correo'),
                    'telefono': usuario.get('telefono')
                }
                return jsonify({'usuario': usuario_seguro}), 200
            else:
                return jsonify({'error': 'Usuario no encontrado'}), 404
                
        except Exception as e:
            return jsonify({'error': f'Error al obtener perfil: {str(e)}'}), 500
        

class RefreshToken(Resource):
    @refresh_token_required
    def post(self):
        """Genera nuevo access token usando refresh token"""
        try:
            user_data = request.current_user
            user_id = user_data['user_id']
            email = user_data['email']
            
            # Generar nuevo access token
            nuevo_access_token = jwt_manager.generar_access_token(user_id, email)
            
            return jsonify({
                'access_token': nuevo_access_token,
                'mensaje': 'Token renovado exitosamente'
            }), 200
            
        except Exception as e:
            return jsonify({'error': f'Error al renovar token: {str(e)}'}), 500

class Logout(Resource):
    @token_required
    def post(self):
        """Cerrar sesión - invalida el token actual"""
        try:
            # Obtener token del header
            auth_header = request.headers.get('Authorization')
            token = auth_header.split(" ")[1] if auth_header else None
            
            if token:
                jwt_manager.agregar_a_lista_negra(token)
                return jsonify({'mensaje': 'Sesión cerrada exitosamente'}), 200
            else:
                return jsonify({'error': 'Token no encontrado'}), 400
                
        except Exception as e:
            return jsonify({'error': f'Error al cerrar sesión: {str(e)}'}), 500

