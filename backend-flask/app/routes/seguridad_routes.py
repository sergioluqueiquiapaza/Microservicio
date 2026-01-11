from flask import Blueprint, request, jsonify
# Importamos el decorador y funciones de JWT
from app.utils.security import role_required
from flask_jwt_extended import create_access_token # Por si necesitas generar token manual

from app.services.seguridad_service import (
    crear_rol_service, obtener_roles_service, obtener_rol_por_id_service,
    actualizar_rol_service, eliminar_rol_service,
    crear_usuario_service, obtener_usuarios_service, obtener_usuario_por_id_service,
    actualizar_usuario_service, eliminar_usuario_service,
    registrar_empresa_y_dueno_service,
    login_usuario_service
)

seguridad_bp = Blueprint('seguridad_bp', __name__)

# ==========================================
# 1. AUTENTICACIÓN (Rutas Públicas)
# ==========================================

@seguridad_bp.route('/auth/registro-empresa', methods=['POST'])
def register_company():

    data = request.get_json()
    response, status = registrar_empresa_y_dueno_service(data)
    return jsonify(response), status

@seguridad_bp.route('/auth/login', methods=['POST'])
def login():

    data = request.get_json()
    response, status = login_usuario_service(data)
    return jsonify(response), status


# ==========================================
# 2. GESTIÓN DE ROLES (Estructural)
# ==========================================

@seguridad_bp.route('/roles', methods=['POST'])
@role_required(['SUPERADMIN']) 
# Solo el Superadmin define qué roles existen en el sistema SaaS
def create_rol():
    response, status = crear_rol_service(request.get_json())
    return jsonify(response), status

@seguridad_bp.route('/roles', methods=['GET'])
@role_required(['SUPERADMIN', 'PROPIETARIO', 'ADMIN'])
# El dueño necesita listar los roles para saber cuál asignarle a su empleado nuevo
def get_roles():
    response, status = obtener_roles_service()
    return jsonify(response), status

@seguridad_bp.route('/roles/<id_rol>', methods=['GET'])
@role_required(['SUPERADMIN', 'PROPIETARIO', 'ADMIN'])
def get_rol(id_rol):
    response, status = obtener_rol_por_id_service(id_rol)
    return jsonify(response), status

@seguridad_bp.route('/roles/<id_rol>', methods=['PUT'])
@role_required(['SUPERADMIN'])
def update_rol(id_rol):
    response, status = actualizar_rol_service(id_rol, request.get_json())
    return jsonify(response), status

@seguridad_bp.route('/roles/<id_rol>', methods=['DELETE'])
@role_required(['SUPERADMIN'])
def delete_rol(id_rol):
    response, status = eliminar_rol_service(id_rol)
    return jsonify(response), status


# ==========================================
# 3. GESTIÓN DE USUARIOS (RRHH)
# ==========================================

@seguridad_bp.route('/usuarios', methods=['POST'])
@role_required(['PROPIETARIO', 'ADMIN'])
# Contratación: El dueño o el gerente crean cuentas para vendedores
def create_usuario():
    response, status = crear_usuario_service(request.get_json())
    return jsonify(response), status

@seguridad_bp.route('/usuarios', methods=['GET'])
@role_required(['PROPIETARIO', 'ADMIN'])
# Ver la lista de empleados. El vendedor NO debe ver esto.
def get_usuarios():
    response, status = obtener_usuarios_service()
    return jsonify(response), status

@seguridad_bp.route('/usuarios/<id_usuario>', methods=['GET'])
@role_required(['PROPIETARIO', 'ADMIN'])
def get_usuario(id_usuario):
    response, status = obtener_usuario_por_id_service(id_usuario)
    return jsonify(response), status

@seguridad_bp.route('/usuarios/<id_usuario>', methods=['PUT'])
@role_required(['PROPIETARIO', 'ADMIN'])
# Cambiar datos de un empleado (ej. cambiar contraseña o teléfono)
def update_usuario(id_usuario):
    response, status = actualizar_usuario_service(id_usuario, request.get_json())
    return jsonify(response), status

@seguridad_bp.route('/usuarios/<id_usuario>', methods=['DELETE'])
@role_required(['PROPIETARIO', 'ADMIN'])
# Despido: Borrar acceso al sistema.
def delete_usuario(id_usuario):
    response, status = eliminar_usuario_service(id_usuario)
    return jsonify(response), status