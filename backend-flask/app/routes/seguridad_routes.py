from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.utils.security import role_required
from app.services.seguridad_service import (
    crear_rol_service, obtener_roles_service, obtener_rol_por_id_service,
    actualizar_rol_service, eliminar_rol_service,
    crear_usuario_service, obtener_usuarios_service, obtener_usuario_por_id_service,
    actualizar_usuario_service, eliminar_usuario_service,
    registrar_empresa_y_dueno_service,
    login_usuario_service, logout_service
)

seguridad_bp = Blueprint('seguridad_bp', __name__)

# ==========================================
# 1. AUTENTICACIÓN (Rutas Públicas)
# ==========================================

@seguridad_bp.route('/auth/registro-empresa', methods=['POST'])
def register_company():
    # Este endpoint crea Empresa + Config + Usuario Dueño (Onboarding)
    data = request.get_json()
    response, status = registrar_empresa_y_dueno_service(data)
    return jsonify(response), status

@seguridad_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    response, status = login_usuario_service(data)
    return jsonify(response), status

@seguridad_bp.route('/auth/logout', methods=['POST'])
@jwt_required() # IMPORTANTE: Solo puede salir quien está dentro
def logout():
    response, status = logout_service()
    return jsonify(response), status


# ==========================================
# 2. GESTIÓN DE ROLES (Estructural)
# ==========================================

@seguridad_bp.route('/roles', methods=['POST'])
@role_required(['SUPER_ADMIN']) 
# Solo el SuperAdmin del SaaS define los roles globales del sistema
def create_rol():
    response, status = crear_rol_service(request.get_json())
    return jsonify(response), status

@seguridad_bp.route('/roles', methods=['GET'])
@role_required(['SUPER_ADMIN', 'PROPIETARIO', 'ADMIN'])
# El dueño necesita listar los roles para asignarlos a sus empleados
def get_roles():
    response, status = obtener_roles_service()
    return jsonify(response), status

@seguridad_bp.route('/roles/<id_rol>', methods=['GET'])
@role_required(['SUPER_ADMIN', 'PROPIETARIO', 'ADMIN'])
def get_rol(id_rol):
    response, status = obtener_rol_por_id_service(id_rol)
    return jsonify(response), status

@seguridad_bp.route('/roles/<id_rol>', methods=['PUT'])
@role_required(['SUPER_ADMIN'])
def update_rol(id_rol):
    response, status = actualizar_rol_service(id_rol, request.get_json())
    return jsonify(response), status

@seguridad_bp.route('/roles/<id_rol>', methods=['DELETE'])
@role_required(['SUPER_ADMIN'])
def delete_rol(id_rol):
    response, status = eliminar_rol_service(id_rol)
    return jsonify(response), status


# ==========================================
# 3. GESTIÓN DE USUARIOS (RRHH)
# ==========================================

@seguridad_bp.route('/usuarios', methods=['POST'])
@role_required(['PROPIETARIO', 'ADMIN'])
# Contratación: El dueño o el gerente crean cuentas para empleados
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
# Actualizar datos del empleado
def update_usuario(id_usuario):
    response, status = actualizar_usuario_service(id_usuario, request.get_json())
    return jsonify(response), status

@seguridad_bp.route('/usuarios/<id_usuario>', methods=['DELETE'])
@role_required(['PROPIETARIO', 'ADMIN'])
# Despido: Borrar acceso al sistema.
def delete_usuario(id_usuario):
    response, status = eliminar_usuario_service(id_usuario)
    return jsonify(response), status

