from flask import Blueprint, request, jsonify
from app.utils.security import role_required
from flask_jwt_extended import jwt_required
from app.services.saas_service import (
    # Admin SaaS
    crear_admin_saas_service, login_admin_saas_service, obtener_admins_saas_service, 
    logout_admin_saas_service, obtener_admin_saas_por_id_service, actualizar_admin_saas_service,
    desactivar_admin_saas_service, activar_admin_saas_service, obtener_admins_saas_inactivos_service,
    # Planes
    crear_plan_service, obtener_planes_service, obtener_plan_id_service,
    actualizar_plan_service, eliminar_plan_service,
    # Suscripciones
    crear_suscripcion_service, obtener_suscripcion_por_empresa_service,
    actualizar_suscripcion_service, obtener_todas_suscripciones_service,
    # Estadísticas
    obtener_estadisticas_dashboard_service, obtener_empresas_recientes_service,
    obtener_pagos_pendientes_service
)

saas_bp = Blueprint('saas_bp', __name__)

# ================= ADMIN SAAS (SUPERADMIN) =================

@saas_bp.route('/saas/admin', methods=['POST'])
def create_admin_saas():
    response, status = crear_admin_saas_service(request.get_json())
    return jsonify(response), status

@saas_bp.route('/saas/login', methods=['POST'])
def login_admin_saas():
    response, status = login_admin_saas_service(request.get_json())
    return jsonify(response), status

@saas_bp.route('/saas/logout', methods=['POST'])
@jwt_required()
def logout_saas():
    response, status = logout_admin_saas_service()
    return jsonify(response), status

@saas_bp.route('/saas/admins', methods=['GET'])
@role_required(['SUPER_ADMIN'])
def get_admins_saas():
    response, status = obtener_admins_saas_service()
    return jsonify(response), status

@saas_bp.route('/saas/admins/<id_admin>', methods=['GET'])
@role_required(['SUPER_ADMIN'])
def get_admin_saas_by_id(id_admin):
    response, status = obtener_admin_saas_por_id_service(id_admin)
    return jsonify(response), status

@saas_bp.route('/saas/admins/<id_admin>', methods=['PUT'])
@role_required(['SUPER_ADMIN'])
def update_admin_saas(id_admin):
    response, status = actualizar_admin_saas_service(id_admin, request.get_json())
    return jsonify(response), status

@saas_bp.route('/saas/admins/<id_admin>/desactivar', methods=['PUT'])
@role_required(['SUPER_ADMIN'])
def deactivate_admin_saas(id_admin):
    response, status = desactivar_admin_saas_service(id_admin)
    return jsonify(response), status

@saas_bp.route('/saas/admins/<id_admin>/activar', methods=['PUT'])
@role_required(['SUPER_ADMIN'])
def activate_admin_saas(id_admin):
    response, status = activar_admin_saas_service(id_admin)
    return jsonify(response), status

@saas_bp.route('/saas/admins/inactivos', methods=['GET'])
@role_required(['SUPER_ADMIN'])
def get_admins_saas_inactivos():
    response, status = obtener_admins_saas_inactivos_service()
    return jsonify(response), status

# ================= PLANES (Catálogo Global) =================

@saas_bp.route('/planes', methods=['POST'])
@role_required(['SUPER_ADMIN'])
def create_plan():
    data = request.get_json()
    response, status = crear_plan_service(data)
    return jsonify(response), status

@saas_bp.route('/planes', methods=['GET'])
def get_planes():
    response, status = obtener_planes_service()
    return jsonify(response), status

@saas_bp.route('/planes/<id_plan>', methods=['GET'])
def get_plan_by_id(id_plan):
    response, status = obtener_plan_id_service(id_plan)
    return jsonify(response), status

@saas_bp.route('/planes/<id_plan>', methods=['PUT'])
@role_required(['SUPER_ADMIN'])
def update_plan(id_plan):
    response, status = actualizar_plan_service(id_plan, request.get_json())
    return jsonify(response), status

@saas_bp.route('/planes/<id_plan>', methods=['DELETE'])
@role_required(['SUPER_ADMIN'])
def delete_plan(id_plan):
    response, status = eliminar_plan_service(id_plan)
    return jsonify(response), status

# ================= SUSCRIPCIONES (Empresa <-> Plan) =================

@saas_bp.route('/suscripciones', methods=['POST'])
def create_suscripcion():
    response, status = crear_suscripcion_service(request.get_json())
    return jsonify(response), status

@saas_bp.route('/suscripciones', methods=['GET'])
@role_required(['SUPER_ADMIN'])
def get_todas_suscripciones():
    response, status = obtener_todas_suscripciones_service()
    return jsonify(response), status

@saas_bp.route('/empresas/<id_empresa>/suscripcion', methods=['GET'])
@role_required(['SUPER_ADMIN', 'PROPIETARIO'])
def get_suscripcion_empresa(id_empresa):
    response, status = obtener_suscripcion_por_empresa_service(id_empresa)
    return jsonify(response), status

@saas_bp.route('/suscripciones/<id_suscripcion>', methods=['PUT'])
@role_required(['SUPER_ADMIN'])
def update_suscripcion(id_suscripcion):
    response, status = actualizar_suscripcion_service(id_suscripcion, request.get_json())
    return jsonify(response), status

# ================= ESTADÍSTICAS Y DASHBOARD =================

@saas_bp.route('/saas/dashboard/estadisticas', methods=['GET'])
@role_required(['SUPER_ADMIN'])
def get_estadisticas_dashboard():
    response, status = obtener_estadisticas_dashboard_service()
    return jsonify(response), status

@saas_bp.route('/saas/dashboard/empresas-recientes', methods=['GET'])
@role_required(['SUPER_ADMIN'])
def get_empresas_recientes():
    limit = request.args.get('limit', 10, type=int)
    response, status = obtener_empresas_recientes_service(limit)
    return jsonify(response), status

@saas_bp.route('/saas/dashboard/pagos-pendientes', methods=['GET'])
@role_required(['SUPER_ADMIN'])
def get_pagos_pendientes():
    response, status = obtener_pagos_pendientes_service()
    return jsonify(response), status

# Agregar esta ruta al archivo saas_routes.py existente
# Después de las rutas de estadísticas

@saas_bp.route('/saas/empresas', methods=['GET'])
@role_required(['SUPER_ADMIN'])
def get_empresas_con_propietarios():
    from app.services.saas_service import obtener_empresas_con_propietarios_service
    response, status = obtener_empresas_con_propietarios_service()
    return jsonify(response), status