import jwt
import redis
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app
import os
from dotenv import load_dotenv
import uuid

load_dotenv()  # Cargar variables de entorno desde el archivo .env

class JWTConfig:
    def __init__(self):
        self.SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'mi_clave_secreta')
        self.ACCESS_TOKEN_EXPIRES = timedelta(minutes=int(os.getenv('ACCESS_TOKEN_EXPIRES', 15)))
        self.REFRESH_TOKEN_EXPIRES = timedelta(minutes=int(os.getenv('REFRESH_TOKEN_EXPIRES', 1440)))
        
        # Configuración Redis
        self.redis_client = redis.Redis(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            db=0,
            decode_responses=True
        )

    def generar_access_token(self, user_id, email):
        """Generar un token de acceso"""
        payload = {
            'user_id': user_id,
            'email': email,
            'exp': datetime.utcnow() + self.ACCESS_TOKEN_EXPIRES,
            'iat': datetime.utcnow(),
            'type': 'access'
        }
        return jwt.encode(payload, self.SECRET_KEY, algorithm='HS256')

    def generar_refresh_token(self, user_id, email):
        """Generar un token de refresco"""
        jti = str(uuid.uuid4())
        payload = {
            'user_id': user_id,
            'email': email,
            'exp': datetime.utcnow() + self.REFRESH_TOKEN_EXPIRES,
            'iat': datetime.utcnow(),
            'jti': jti,
            'type': 'refresh'
        }

        # Guardar en redis para control
        token_key = f"refresh_token:{user_id}:{jti}"
        self.redis_client.setex(
            token_key, 
            int(self.REFRESH_TOKEN_EXPIRES.total_seconds()),
            email
        )

        return jwt.encode(payload, self.SECRET_KEY, algorithm='HS256')

    def validar_token(self, token):
        """Valida cualquier tipo de token"""
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=['HS256'])

            # Verificar si esta en lista negra
            if self.esta_en_lista_negra(token):
                return None
            
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def agregar_a_lista_negra(self, token, tiempo_expiracion=None):
        """Agregar token a lista negra"""
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=['HS256'], options={"verify_exp": False})
            jti = payload.get('jti', token[:10])  # Usar JTI o primeros 10 chars

            if tiempo_expiracion is None:
                tiempo_expiracion = payload['exp'] - datetime.utcnow().timestamp()
                tiempo_expiracion = max(1, int(tiempo_expiracion))

            self.redis_client.setex(f"blacklist:{jti}", tiempo_expiracion, "blacklisted")
            return True
        except Exception as e:
            print(f"Error al agregar a lista negra: {e}")
            return False
    
    def esta_en_lista_negra(self, token):
        """Verifica si un token esta en la lista negra"""
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=['HS256'], options={"verify_exp": False})
            jti = payload.get('jti', token[:10])  # Usar JTI o primeros 10 chars
            return self.redis_client.exists(f"blacklist:{jti}")
        except:
            return False 
           
    def invalidar_todos_tokens_usuario(self, user_id):
        """Invalidar todos los tokens de un usuario"""
        pattern = f"refresh_token:{user_id}:*"
        keys = self.redis_client.keys(pattern)
        if keys:
            self.redis_client.delete(*keys)
        return len(keys)

# Instancia global
jwt_manager = JWTConfig()

# Decorador para rutas protegidas
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None

        # Buscar token en header Authorization
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Asumiendo formato "Bearer <token>"
            except IndexError:
                return jsonify({'message': 'Token invalido'}), 401
            
        if not token:
            return jsonify({'message': 'Token faltante'}), 401
        
        payload = jwt_manager.validar_token(token)
        if not payload:
            return jsonify({'mensaje': 'Token inválido o expirado'}), 401
        
        # Verificar que sea un access token
        if payload.get('type') != 'access':
            return jsonify({'mensaje': 'Tipo de token inválido'}), 401
        
        request.current_user = payload
        return f(*args, **kwargs)
    
    return decorated_function

def refresh_token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'mensaje': 'Formato de token inválido'}), 401
        
        if not token:
            return jsonify({'mensaje': 'Refresh token faltante'}), 401
        
        payload = jwt_manager.validar_token(token)
        if not payload:
            return jsonify({'mensaje': 'Refresh token inválido o expirado'}), 401
        
        # Verificar que sea un refresh token
        if payload.get('type') != 'refresh':
            return jsonify({'mensaje': 'Tipo de token inválido'}), 401
        
        # Verificar que existe en Redis
        user_id = payload['user_id']
        jti = payload['jti']
        token_key = f"refresh_token:{user_id}:{jti}"
        
        if not jwt_manager.redis_client.exists(token_key):
            return jsonify({'mensaje': 'Refresh token revocado'}), 401
        
        request.current_user = payload
        request.current_refresh_token = token
        return f(*args, **kwargs)
    
    return decorated_function










