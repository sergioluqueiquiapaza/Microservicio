from flask import Blueprint, request, jsonify
from app.utils.security import role_required
from app.services.soporte_service import (
    crear_notificacion_service, obtener_notificaciones_service, obtener_notificacion_id_service,
    actualizar_notificacion_service, eliminar_notificacion_service,
    crear_auditoria_service, obtener_auditorias_service, obtener_auditoria_id_service,
    eliminar_auditoria_service
)

soporte_bp = Blueprint('soporte_bp', __name__)

# ==========================================
# 1. NOTIFICACIONES (Comunicación Interna)
# ==========================================

@soporte_bp.route('/notificaciones', methods=['POST'])
@role_required(['PROPIETARIO', 'ADMIN'])
def create_noti():
    response, status = crear_notificacion_service(request.get_json())
    return jsonify(response), status

@soporte_bp.route('/notificaciones', methods=['GET'])
@role_required(['PROPIETARIO', 'ADMIN', 'VENDEDOR'])
def get_notis():
    # Nota: El servicio debe encargarse de filtrar por empresa/usuario
    response, status = obtener_notificaciones_service()
    return jsonify(response), status

@soporte_bp.route('/notificaciones/<id_noti>', methods=['GET'])
@role_required(['PROPIETARIO', 'ADMIN', 'VENDEDOR'])
def get_noti(id_noti):
    response, status = obtener_notificacion_id_service(id_noti)
    return jsonify(response), status

@soporte_bp.route('/notificaciones/<id_noti>', methods=['PUT'])
@role_required(['PROPIETARIO', 'ADMIN', 'VENDEDOR'])
# Permitido a todos para marcar como "Leída"
def update_noti(id_noti):
    response, status = actualizar_notificacion_service(id_noti, request.get_json())
    return jsonify(response), status

@soporte_bp.route('/notificaciones/<id_noti>', methods=['DELETE'])
@role_required(['PROPIETARIO', 'ADMIN'])
def delete_noti(id_noti):
    response, status = eliminar_notificacion_service(id_noti)
    return jsonify(response), status


# ==========================================
# 2. AUDITORÍA (Logs de Seguridad)
# ==========================================

@soporte_bp.route('/auditoria', methods=['POST'])
@role_required(['PROPIETARIO', 'ADMIN']) 
def create_audit():
    response, status = crear_auditoria_service(request.get_json())
    return jsonify(response), status

@soporte_bp.route('/auditoria', methods=['GET'])
@role_required(['PROPIETARIO', 'ADMIN'])
# Vendedor no ve logs
def get_audits():
    response, status = obtener_auditorias_service()
    return jsonify(response), status

@soporte_bp.route('/auditoria/<id_audit>', methods=['GET'])
@role_required(['PROPIETARIO', 'ADMIN'])
def get_audit(id_audit):
    response, status = obtener_auditoria_id_service(id_audit)
    return jsonify(response), status

@soporte_bp.route('/auditoria/<id_audit>', methods=['DELETE'])
@role_required(['SUPER_ADMIN']) 
# Extremadamente restringido para integridad de datos
def delete_audit(id_audit):
    response, status = eliminar_auditoria_service(id_audit)
    return jsonify(response), status