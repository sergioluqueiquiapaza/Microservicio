from flask import Blueprint, request, jsonify
# Importamos el guardián de seguridad
from app.utils.security import role_required
from app.services.ventas_service import (
    crear_cliente_service, obtener_clientes_service, obtener_cliente_id_service,
    actualizar_cliente_service, eliminar_cliente_service,
    crear_venta_service, obtener_ventas_service, obtener_venta_id_service,
    eliminar_venta_service,crear_detalle_venta_service, obtener_detalles_por_venta_service, eliminar_detalle_venta_service,
    crear_pago_service, obtener_pagos_service, obtener_pago_id_service, eliminar_pago_service
)

ventas_bp = Blueprint('ventas_bp', __name__)

# ==========================================
# 1. CLIENTES (CRM)
# ==========================================

@ventas_bp.route('/clientes', methods=['POST'])
@role_required(['PROPIETARIO', 'ADMIN', 'VENDEDOR'])
# El vendedor necesita registrar clientes nuevos en el mostrador.
def create_cliente():
    response, status = crear_cliente_service(request.get_json())
    return jsonify(response), status

@ventas_bp.route('/clientes', methods=['GET'])
@role_required(['PROPIETARIO', 'ADMIN', 'VENDEDOR'])
# El vendedor necesita buscar clientes para asignarles la venta.
def get_clientes():
    response, status = obtener_clientes_service()
    return jsonify(response), status

@ventas_bp.route('/clientes/<id_cli>', methods=['GET'])
@role_required(['PROPIETARIO', 'ADMIN', 'VENDEDOR'])
def get_cliente(id_cli):
    response, status = obtener_cliente_id_service(id_cli)
    return jsonify(response), status

@ventas_bp.route('/clientes/<id_cli>', methods=['PUT'])
@role_required(['PROPIETARIO', 'ADMIN', 'VENDEDOR'])
# Permitimos al vendedor actualizar datos (ej. el cliente cambió su teléfono o dirección).
def update_cliente(id_cli):
    response, status = actualizar_cliente_service(id_cli, request.get_json())
    return jsonify(response), status

@ventas_bp.route('/clientes/<id_cli>', methods=['DELETE'])
@role_required(['PROPIETARIO', 'ADMIN'])
# SOLO JEFES. El vendedor no debe poder borrar la base de datos de clientes.
def delete_cliente(id_cli):
    response, status = eliminar_cliente_service(id_cli)
    return jsonify(response), status


# ==========================================
# 2. VENTAS (Cabecera)
# ==========================================

@ventas_bp.route('/ventas', methods=['POST'])
@role_required(['PROPIETARIO', 'ADMIN', 'VENDEDOR'])
# La función principal del vendedor.
def create_venta():
    response, status = crear_venta_service(request.get_json())
    return jsonify(response), status

@ventas_bp.route('/ventas', methods=['GET'])
@role_required(['PROPIETARIO', 'ADMIN', 'VENDEDOR'])
# El vendedor necesita ver el historial del día o reimprimir notas.
def get_ventas():
    response, status = obtener_ventas_service()
    return jsonify(response), status

@ventas_bp.route('/ventas/<id_venta>', methods=['GET'])
@role_required(['PROPIETARIO', 'ADMIN', 'VENDEDOR'])
def get_venta(id_venta):
    response, status = obtener_venta_id_service(id_venta)
    return jsonify(response), status

@ventas_bp.route('/ventas/<id_venta>', methods=['DELETE'])
@role_required(['PROPIETARIO', 'ADMIN'])
# SEGURIDAD CRÍTICA: El vendedor JAMÁS debe poder borrar una venta.
# Esto previene el robo de caja (cobrar, entregar producto y borrar el registro).
def delete_venta(id_venta):
    response, status = eliminar_venta_service(id_venta)
    return jsonify(response), status


# ==========================================
# 3. DETALLES DE VENTA (Líneas de productos)
# ==========================================

@ventas_bp.route('/detalles-venta', methods=['POST'])
@role_required(['PROPIETARIO', 'ADMIN', 'VENDEDOR'])
# Agregar items al carrito.
def create_detalle():
    response, status = crear_detalle_venta_service(request.get_json())
    return jsonify(response), status

@ventas_bp.route('/ventas/<id_venta>/detalles', methods=['GET'])
@role_required(['PROPIETARIO', 'ADMIN', 'VENDEDOR'])
def get_detalles_de_venta(id_venta):
    response, status = obtener_detalles_por_venta_service(id_venta)
    return jsonify(response), status

@ventas_bp.route('/detalles-venta/<id_detalle>', methods=['DELETE'])
@role_required(['PROPIETARIO', 'ADMIN'])
# Similar a borrar venta: Si hay que quitar un item de una venta ya CERRADA, 
# debe hacerlo un supervisor para autorizar la devolución.
# (Si es durante la creación en frontend, el manejo es local, esto es en BD).
def delete_detalle(id_detalle):
    response, status = eliminar_detalle_venta_service(id_detalle)
    return jsonify(response), status


# ==========================================
# 4. PAGOS (Caja)
# ==========================================

@ventas_bp.route('/pagos', methods=['POST'])
@role_required(['PROPIETARIO', 'ADMIN', 'VENDEDOR'])
# El vendedor cobra el dinero.
def create_pago():
    response, status = crear_pago_service(request.get_json())
    return jsonify(response), status

@ventas_bp.route('/pagos', methods=['GET'])
@role_required(['PROPIETARIO', 'ADMIN', 'VENDEDOR'])
# Verificar si una venta está pagada.
def get_pagos():
    response, status = obtener_pagos_service()
    return jsonify(response), status

@ventas_bp.route('/pagos/<id_pago>', methods=['GET'])
@role_required(['PROPIETARIO', 'ADMIN', 'VENDEDOR'])
def get_pago(id_pago):
    response, status = obtener_pago_id_service(id_pago)
    return jsonify(response), status

@ventas_bp.route('/pagos/<id_pago>', methods=['DELETE'])
@role_required(['PROPIETARIO', 'ADMIN'])
# SEGURIDAD CRÍTICA: Eliminar un pago es una forma común de desfalco.
# Solo dueños o admins pueden anular cobros.
def delete_pago(id_pago):
    response, status = eliminar_pago_service(id_pago)
    return jsonify(response), status