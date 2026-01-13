from flask import Blueprint, request, jsonify
from app.utils.security import role_required
from flask_jwt_extended import jwt_required
from app.services.saas_service import (
    # Admin SaaS
    crear_admin_saas_service, login_admin_saas_service, obtener_admins_saas_service, logout_admin_saas_service,
    # Planes
    crear_plan_service, obtener_planes_service, obtener_plan_id_service, 
    actualizar_plan_service, eliminar_plan_service,
    # Suscripciones
    crear_suscripcion_service, obtener_suscripcion_por_empresa_service, actualizar_suscripcion_service
)

saas_bp = Blueprint('saas_bp', __name__)

# ================= ADMIN SAAS (SUPERADMIN) =================

@saas_bp.route('/saas/admin', methods=['POST'])
# Ojo: Esta ruta debería estar protegida o ser secreta para crear el primer SuperAdmin
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
    # Llamamos al servicio específico de SaaS
    response, status = logout_admin_saas_service()
    return jsonify(response), status

@saas_bp.route('/saas/admins', methods=['GET'])
@role_required(['SUPER_ADMIN'])
def get_admins_saas():
    response, status = obtener_admins_saas_service()
    return jsonify(response), status


# ================= PLANES (Catálogo Global) =================

@saas_bp.route('/planes', methods=['POST'])
@role_required(['SUPER_ADMIN'])
def create_plan():
    data = request.get_json()
    # Inyectamos el ID del admin que crea el plan (viene del token idealmente, o del JSON)
    # Por simplicidad lo tomamos del JSON
    response, status = crear_plan_service(data)
    return jsonify(response), status

@saas_bp.route('/planes', methods=['GET'])
# Público o restringido, pero los clientes deben poder ver qué planes existen
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
@role_required(['SUPER_ADMIN'])
# Generalmente el SuperAdmin activa la suscripción manualmente o mediante pasarela de pago
def create_suscripcion():
    response, status = crear_suscripcion_service(request.get_json())
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