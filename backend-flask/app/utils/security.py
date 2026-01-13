from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def role_required(roles_permitidos):
    """
    Decorador para restringir acceso según el rol del usuario.
    Ejemplo de uso: @role_required(['SUPER_ADMIN', 'PROPIETARIO'])
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                verify_jwt_in_request() # Verifica que el token sea válido y no haya expirado
                claims = get_jwt()
                rol_usuario = claims.get('rol') # Extraemos el rol del token (inyectado en el login)
                
                # 1. El SUPER_ADMIN siempre pasa (Puerta trasera para el dueño del SaaS)
                # CAMBIO IMPORTANTE: 'SUPER_ADMIN' con guion bajo para coincidir con saas_service.py
                if rol_usuario == 'SUPER_ADMIN':
                    return fn(*args, **kwargs)
                
                # 2. Verificar si el rol del usuario está en la lista permitida para esta ruta
                if rol_usuario in roles_permitidos:
                    return fn(*args, **kwargs)
                else:
                    return jsonify({
                        "error": "Acceso denegado", 
                        "mensaje": f"El rol '{rol_usuario}' no tiene permisos para realizar esta acción."
                    }), 403
            
            except Exception as e:
                # Captura errores si el token no existe o es inválido
                return jsonify({"error": "Autorización fallida", "detalle": str(e)}), 401
                
        return decorator
    return wrapper