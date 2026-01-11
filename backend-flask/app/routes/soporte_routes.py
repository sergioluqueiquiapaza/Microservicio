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
# Solo jefes envían avisos manuales (ej. "Reunión a las 5")
# Nota: El sistema puede crear notificaciones automáticas internamente sin pasar por aquí.
def create_noti():
    response, status = crear_notificacion_service(request.get_json())
    return jsonify(response), status

@soporte_bp.route('/notificaciones', methods=['GET'])
@role_required(['PROPIETARIO', 'ADMIN', 'VENDEDOR'])
# TODOS deben ver sus notificaciones (Alertas de stock, avisos, etc.)
def get_notis():
    # IMPORTANTE: Tu servicio (obtener_notificaciones_service) debe filtrar
    # para devolver solo las notificaciones DEL USUARIO que llama, 
    # o las globales de la empresa.
    response, status = obtener_notificaciones_service()
    return jsonify(response), status

@soporte_bp.route('/notificaciones/<id_noti>', methods=['GET'])
@role_required(['PROPIETARIO', 'ADMIN', 'VENDEDOR'])
def get_noti(id_noti):
    response, status = obtener_notificacion_id_service(id_noti)
    return jsonify(response), status

@soporte_bp.route('/notificaciones/<id_noti>', methods=['PUT'])
@role_required(['PROPIETARIO', 'ADMIN', 'VENDEDOR'])
# Esto se usa comúnmente para marcar una notificación como "Leída" (is_read=True)
# Por tanto, el vendedor debe tener permiso.
def update_noti(id_noti):
    response, status = actualizar_notificacion_service(id_noti, request.get_json())
    return jsonify(response), status

@soporte_bp.route('/notificaciones/<id_noti>', methods=['DELETE'])
@role_required(['PROPIETARIO', 'ADMIN'])
# Borrar notificaciones del historial general.
def delete_noti(id_noti):
    response, status = eliminar_notificacion_service(id_noti)
    return jsonify(response), status


# ==========================================
# 2. AUDITORÍA (Logs de Seguridad)
# ==========================================
# Regla de Oro: Los logs de auditoría NO se deberían borrar ni editar.
# Solo se leen para investigar fraudes o errores.

@soporte_bp.route('/auditoria', methods=['POST'])
@role_required(['PROPIETARIO', 'ADMIN']) 
# Usualmente la auditoría es automática (backend), pero si el Frontend 
# necesita reportar un evento manual, solo usuarios de confianza.
def create_audit():
    response, status = crear_auditoria_service(request.get_json())
    return jsonify(response), status

@soporte_bp.route('/auditoria', methods=['GET'])
@role_required(['PROPIETARIO', 'ADMIN'])
# El Vendedor NO debe ver quién modificó qué. Eso es para gerencia.
def get_audits():
    response, status = obtener_auditorias_service()
    return jsonify(response), status

@soporte_bp.route('/auditoria/<id_audit>', methods=['GET'])
@role_required(['PROPIETARIO', 'ADMIN'])
def get_audit(id_audit):
    response, status = obtener_auditoria_id_service(id_audit)
    return jsonify(response), status

@soporte_bp.route('/auditoria/<id_audit>', methods=['DELETE'])
@role_required(['SUPERADMIN']) 
# EXTREMADAMENTE RESTRINGIDO.
# Ni siquiera el Propietario debería poder borrar auditoría fácilmente 
# para garantizar la integridad de los datos en caso de disputas legales.
# Si prefieres que el dueño pueda, agrega 'PROPIETARIO' a la lista.
def delete_audit(id_audit):
    response, status = eliminar_auditoria_service(id_audit)
    return jsonify(response), status