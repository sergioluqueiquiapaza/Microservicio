from flask import Blueprint, request, jsonify
# Importamos el decorador de seguridad
from app.utils.security import role_required
from app.services.empresa_service import (
    # Empresa
    crear_empresa_service, obtener_empresas_service, obtener_empresa_por_id_service,
    actualizar_empresa_service, eliminar_empresa_service,
    # Config
    crear_config_service, obtener_configs_service, obtener_config_por_id_service,
    actualizar_config_service, eliminar_config_service
)

empresa_bp = Blueprint('empresa_bp', __name__)

# ================= RUTAS DE EMPRESA =================

@empresa_bp.route('/empresas', methods=['POST'])
##@role_required(['SUPER_ADMIN']) 
# Solo el Superadmin puede dar de alta una nueva empresa (Tenant) manualmente por aquí
def create_empresa():
    data = request.get_json()
    response, status = crear_empresa_service(data)
    return jsonify(response), status

@empresa_bp.route('/empresas', methods=['GET'])
@role_required(['SUPER_ADMIN']) 
def get_empresas():
    response, status = obtener_empresas_service()
    return jsonify(response), status

@empresa_bp.route('/empresas/<id_empresa>', methods=['GET'])
@role_required(['PROPIETARIO', 'ADMIN', 'SUPER_ADMIN'])
# El dueño, el admin y el superadmin pueden ver los datos
def get_empresa_by_id(id_empresa):
    response, status = obtener_empresa_por_id_service(id_empresa)
    return jsonify(response), status

@empresa_bp.route('/empresas/<id_empresa>', methods=['PUT'])
@role_required(['PROPIETARIO', 'SUPER_ADMIN'])
# Solo el dueño o superadmin cambia la Razón Social o el Logo
def update_empresa(id_empresa):
    data = request.get_json()
    response, status = actualizar_empresa_service(id_empresa, data)
    return jsonify(response), status

@empresa_bp.route('/empresas/<id_empresa>', methods=['DELETE'])
@role_required(['SUPER_ADMIN'])
# Solo el Superadmin puede borrar una empresa entera del sistema
def delete_empresa(id_empresa):
    response, status = eliminar_empresa_service(id_empresa)
    return jsonify(response), status


# ================= RUTAS DE CONFIGURACIÓN =================

@empresa_bp.route('/configuracion', methods=['POST'])
@role_required(['PROPIETARIO']) 
def create_config():
    data = request.get_json()
    response, status = crear_config_service(data)
    return jsonify(response), status

@empresa_bp.route('/configuracion', methods=['GET'])
@role_required(['PROPIETARIO', 'ADMIN', 'VENDEDOR'])
def get_configs():
    response, status = obtener_configs_service()
    return jsonify(response), status

@empresa_bp.route('/configuracion/<id_config>', methods=['GET'])
@role_required(['PROPIETARIO', 'ADMIN', 'VENDEDOR'])
def get_config_by_id(id_config):
    response, status = obtener_config_por_id_service(id_config)
    return jsonify(response), status

@empresa_bp.route('/configuracion/<id_config>', methods=['PUT'])
@role_required(['PROPIETARIO', 'ADMIN'])
def update_config(id_config):
    data = request.get_json()
    response, status = actualizar_config_service(id_config, data)
    return jsonify(response), status

@empresa_bp.route('/configuracion/<id_config>', methods=['DELETE'])
@role_required(['PROPIETARIO'])
def delete_config(id_config):
    response, status = eliminar_config_service(id_config)
    return jsonify(response), status