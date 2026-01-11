from flask import Blueprint, request, jsonify
# Importamos el decorador de seguridad
from app.utils.security import role_required
from app.services.compras_service import (
    crear_compra_service, obtener_compras_service, obtener_compra_id_service,
    actualizar_compra_service, eliminar_compra_service,
    crear_detalle_compra_service, obtener_detalles_por_compra_service, eliminar_detalle_compra_service
)

compras_bp = Blueprint('compras_bp', __name__)

# --- RUTAS DE CABECERA DE COMPRA ---

@compras_bp.route('/compras', methods=['POST'])
@role_required(['PROPIETARIO', 'ADMIN']) 
# Nota: SUPERADMIN siempre pasa por defecto en nuestro decorador
def create_compra():
    response, status = crear_compra_service(request.get_json())
    return jsonify(response), status

@compras_bp.route('/compras', methods=['GET'])
@role_required(['PROPIETARIO', 'ADMIN'])
def get_compras():
    response, status = obtener_compras_service()
    return jsonify(response), status

@compras_bp.route('/compras/<id_compra>', methods=['GET'])
@role_required(['PROPIETARIO', 'ADMIN'])
def get_compra(id_compra):
    response, status = obtener_compra_id_service(id_compra)
    return jsonify(response), status

@compras_bp.route('/compras/<id_compra>', methods=['PUT'])
@role_required(['PROPIETARIO', 'ADMIN'])
def update_compra(id_compra):
    response, status = actualizar_compra_service(id_compra, request.get_json())
    return jsonify(response), status

@compras_bp.route('/compras/<id_compra>', methods=['DELETE'])
@role_required(['PROPIETARIO', 'ADMIN']) 
# Si quieres que SOLO el dueño pueda borrar compras, quita 'ADMIN' de esta lista
def delete_compra(id_compra):
    response, status = eliminar_compra_service(id_compra)
    return jsonify(response), status

# --- DETALLES DE COMPRA ---

@compras_bp.route('/detalles-compra', methods=['POST'])
@role_required(['PROPIETARIO', 'ADMIN'])
def create_detalle_compra():
    response, status = crear_detalle_compra_service(request.get_json())
    return jsonify(response), status

# Ver detalles de una compra específica
@compras_bp.route('/compras/<id_compra>/detalles', methods=['GET'])
@role_required(['PROPIETARIO', 'ADMIN'])
def get_detalles_de_compra(id_compra):
    response, status = obtener_detalles_por_compra_service(id_compra)
    return jsonify(response), status

@compras_bp.route('/detalles-compra/<id_detalle>', methods=['DELETE'])
@role_required(['PROPIETARIO', 'ADMIN'])
def delete_detalle_compra(id_detalle):
    response, status = eliminar_detalle_compra_service(id_detalle)
    return jsonify(response), status