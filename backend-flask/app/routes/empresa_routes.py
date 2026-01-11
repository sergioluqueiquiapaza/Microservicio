from flask import Blueprint, request, jsonify
# Importamos el decorador de seguridad
from app.utils.security import role_required
from app.services.empresa_service import (
    # Empresa
    crear_empresa_service, obtener_empresas_service, obtener_empresa_por_id_service,
    actualizar_empresa_service, eliminar_empresa_service,
    # Planes
    crear_plan_service, obtener_planes_service, obtener_plan_por_id_service,
    actualizar_plan_service, eliminar_plan_service,
    # Config
    crear_config_service, obtener_configs_service, obtener_config_por_id_service,
    actualizar_config_service, eliminar_config_service
)

empresa_bp = Blueprint('empresa_bp', __name__)

# ================= RUTAS DE EMPRESA =================

@empresa_bp.route('/empresas', methods=['POST'])
@role_required(['SUPERADMIN']) 
# Solo el Superadmin puede dar de alta una nueva empresa en el sistema (Tenant)
def create_empresa():
    data = request.get_json()
    response, status = crear_empresa_service(data)
    return jsonify(response), status

@empresa_bp.route('/empresas', methods=['GET'])
@role_required(['SUPERADMIN']) 
# Listar TODAS las empresas es un privilegio de Dios (Superadmin)
def get_empresas():
    response, status = obtener_empresas_service()
    return jsonify(response), status

@empresa_bp.route('/empresas/<id_empresa>', methods=['GET'])
@role_required(['PROPIETARIO', 'ADMIN'])
# El dueño y el admin pueden ver los datos de SU empresa
def get_empresa_by_id(id_empresa):
    response, status = obtener_empresa_por_id_service(id_empresa)
    return jsonify(response), status

@empresa_bp.route('/empresas/<id_empresa>', methods=['PUT'])
@role_required(['PROPIETARIO'])
# Solo el dueño debería poder cambiar la Razón Social o el Logo
def update_empresa(id_empresa):
    data = request.get_json()
    response, status = actualizar_empresa_service(id_empresa, data)
    return jsonify(response), status

@empresa_bp.route('/empresas/<id_empresa>', methods=['DELETE'])
@role_required(['SUPERADMIN'])
# Solo el Superadmin puede borrar una empresa entera del sistema
def delete_empresa(id_empresa):
    response, status = eliminar_empresa_service(id_empresa)
    return jsonify(response), status


# ================= RUTAS DE PLANES (Suscripciones) =================
# NOTA: Estas tablas controlan cuánto paga la empresa y cuándo vence su servicio.
# El Propietario NO debe poder editar esto, solo el Superadmin (Soporte/Ventas del SaaS).

@empresa_bp.route('/planes', methods=['POST'])
@role_required(['SUPERADMIN'])
def create_plan():
    data = request.get_json()
    response, status = crear_plan_service(data)
    return jsonify(response), status

@empresa_bp.route('/planes', methods=['GET'])
@role_required(['SUPERADMIN', 'PROPIETARIO'])
# El dueño puede VER qué plan tiene, pero no tocarlo
def get_planes():
    response, status = obtener_planes_service()
    return jsonify(response), status

@empresa_bp.route('/planes/<id_plan>', methods=['GET'])
@role_required(['SUPERADMIN', 'PROPIETARIO'])
def get_plan_by_id(id_plan):
    response, status = obtener_plan_por_id_service(id_plan)
    return jsonify(response), status

@empresa_bp.route('/planes/<id_plan>', methods=['PUT'])
@role_required(['SUPERADMIN'])
# Solo Superadmin puede extender la fecha de vencimiento o cambiar límites
def update_plan(id_plan):
    data = request.get_json()
    response, status = actualizar_plan_service(id_plan, data)
    return jsonify(response), status

@empresa_bp.route('/planes/<id_plan>', methods=['DELETE'])
@role_required(['SUPERADMIN'])
def delete_plan(id_plan):
    response, status = eliminar_plan_service(id_plan)
    return jsonify(response), status


# ================= RUTAS DE CONFIGURACIÓN =================
# Configuración operativa: Moneda, Impuestos, Alertas.

@empresa_bp.route('/configuracion', methods=['POST'])
@role_required(['PROPIETARIO']) 
# Configuración inicial la hace el dueño
def create_config():
    data = request.get_json()
    response, status = crear_config_service(data)
    return jsonify(response), status

@empresa_bp.route('/configuracion', methods=['GET'])
@role_required(['PROPIETARIO', 'ADMIN', 'VENDEDOR'])
# TODOS necesitan leer esto. El vendedor necesita saber el IVA para vender.
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
# El Admin operativo puede cambiar si se notifican ventas o stock, pero el vendedor no.
def update_config(id_config):
    data = request.get_json()
    response, status = actualizar_config_service(id_config, data)
    return jsonify(response), status

@empresa_bp.route('/configuracion/<id_config>', methods=['DELETE'])
@role_required(['PROPIETARIO'])
# Borrar la configuración es peligroso, solo dueño.
def delete_config(id_config):
    response, status = eliminar_config_service(id_config)
    return jsonify(response), status