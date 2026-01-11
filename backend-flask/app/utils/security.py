from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def role_required(roles_permitidos):
    """
    Decorador para restringir acceso según el rol del usuario.
    Ejemplo de uso: @role_required(['SUPERADMIN', 'PROPIETARIO'])
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request() # Verifica que el token sea válido
            claims = get_jwt()
            rol_usuario = claims.get('rol') # Extraemos el rol del token
            
            # El SUPERADMIN siempre pasa (puerta trasera divina)
            if rol_usuario == 'SUPERADMIN':
                return fn(*args, **kwargs)
                
            if rol_usuario in roles_permitidos:
                return fn(*args, **kwargs)
            else:
                return jsonify({"error": "Acceso denegado: No tienes permisos suficientes"}), 403
        return decorator
    return wrapper