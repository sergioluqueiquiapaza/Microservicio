from flask import Blueprint, request, jsonify
from app.utils.security import role_required 
from app.services.inventario_service import (
    # Categoria
    crear_categoria_service, obtener_categorias_service, 
    obtener_categoria_por_id_service, actualizar_categoria_service, 
    eliminar_categoria_service,
    # Proveedor
    crear_proveedor_service, obtener_proveedores_service, obtener_proveedor_id_service,
    actualizar_proveedor_service, eliminar_proveedor_service,
    # Producto
    crear_producto_service, obtener_productos_service, obtener_producto_id_service,
    actualizar_producto_service, eliminar_producto_service,
    # Relaciones
    asignar_proveedor_a_producto_service, desvincular_proveedor_producto_service,
    actualizar_relacion_service, obtener_productos_por_proveedor_service,
    obtener_todas_las_relaciones_service,
    # Inventario
    crear_inventario_service, obtener_inventarios_service, obtener_inventario_id_service,
    actualizar_inventario_service, eliminar_inventario_service
)

inventario_bp = Blueprint('inventario_bp', __name__)

# ================= RUTAS CATEGORIA =================

@inventario_bp.route('/categorias', methods=['POST'])
@role_required(['PROPIETARIO', 'ADMIN'])
def create_categoria():
    response, status = crear_categoria_service(request.get_json())
    return jsonify(response), status

@inventario_bp.route('/categorias', methods=['GET'])
@role_required(['PROPIETARIO', 'ADMIN', 'VENDEDOR']) 
def get_categorias():
    response, status = obtener_categorias_service()
    return jsonify(response), status

@inventario_bp.route('/categorias/<id_categoria>', methods=['GET'])
@role_required(['PROPIETARIO', 'ADMIN', 'VENDEDOR'])
def get_categoria(id_categoria):
    response, status = obtener_categoria_por_id_service(id_categoria)
    return jsonify(response), status

@inventario_bp.route('/categorias/<id_categoria>', methods=['PUT'])
@role_required(['PROPIETARIO', 'ADMIN'])
def update_categoria(id_categoria):
    response, status = actualizar_categoria_service(id_categoria, request.get_json())
    return jsonify(response), status

@inventario_bp.route('/categorias/<id_categoria>', methods=['DELETE'])
@role_required(['PROPIETARIO', 'ADMIN'])
def delete_categoria(id_categoria):
    response, status = eliminar_categoria_service(id_categoria)
    return jsonify(response), status


# ================= RUTAS PROVEEDOR =================

@inventario_bp.route('/proveedores', methods=['POST'])
@role_required(['PROPIETARIO', 'ADMIN'])
def create_proveedor():
    response, status = crear_proveedor_service(request.get_json())
    return jsonify(response), status

@inventario_bp.route('/proveedores', methods=['GET'])
@role_required(['PROPIETARIO', 'ADMIN'])
def get_proveedores():
    response, status = obtener_proveedores_service()
    return jsonify(response), status

@inventario_bp.route('/proveedores/<id_prov>', methods=['GET'])
@role_required(['PROPIETARIO', 'ADMIN'])
def get_proveedor(id_prov):
    response, status = obtener_proveedor_id_service(id_prov)
    return jsonify(response), status

@inventario_bp.route('/proveedores/<id_prov>', methods=['PUT'])
@role_required(['PROPIETARIO', 'ADMIN'])
def update_proveedor(id_prov):
    response, status = actualizar_proveedor_service(id_prov, request.get_json())
    return jsonify(response), status

@inventario_bp.route('/proveedores/<id_prov>', methods=['DELETE'])
@role_required(['PROPIETARIO', 'ADMIN'])
def delete_proveedor(id_prov):
    response, status = eliminar_proveedor_service(id_prov)
    return jsonify(response), status


# ================= RUTAS PRODUCTO =================

@inventario_bp.route('/productos', methods=['POST'])
@role_required(['PROPIETARIO', 'ADMIN'])
def create_producto():
    response, status = crear_producto_service(request.get_json())
    return jsonify(response), status

@inventario_bp.route('/productos', methods=['GET'])
@role_required(['PROPIETARIO', 'ADMIN', 'VENDEDOR']) 
def get_productos():
    response, status = obtener_productos_service()
    return jsonify(response), status

@inventario_bp.route('/productos/<id_prod>', methods=['GET'])
@role_required(['PROPIETARIO', 'ADMIN', 'VENDEDOR'])
def get_producto(id_prod):
    response, status = obtener_producto_id_service(id_prod)
    return jsonify(response), status

@inventario_bp.route('/productos/<id_prod>', methods=['PUT'])
@role_required(['PROPIETARIO', 'ADMIN'])
def update_producto(id_prod):
    response, status = actualizar_producto_service(id_prod, request.get_json())
    return jsonify(response), status

@inventario_bp.route('/productos/<id_prod>', methods=['DELETE'])
@role_required(['PROPIETARIO', 'ADMIN'])
def delete_producto(id_prod):
    response, status = eliminar_producto_service(id_prod)
    return jsonify(response), status


# ================= RELACIÓN PRODUCTO - PROVEEDOR =================

@inventario_bp.route('/productos/<id_prod>/proveedores', methods=['POST'])
@role_required(['PROPIETARIO', 'ADMIN'])
def link_proveedor(id_prod):
    response, status = asignar_proveedor_a_producto_service(id_prod, request.get_json())
    return jsonify(response), status

@inventario_bp.route('/productos/<id_prod>/proveedores/<id_prov>', methods=['DELETE'])
@role_required(['PROPIETARIO', 'ADMIN'])
def unlink_proveedor(id_prod, id_prov):
    response, status = desvincular_proveedor_producto_service(id_prod, id_prov)
    return jsonify(response), status

@inventario_bp.route('/productos/<id_prod>/proveedores/<id_prov>', methods=['PUT'])
@role_required(['PROPIETARIO', 'ADMIN'])
def update_product_provider_link(id_prod, id_prov):
    response, status = actualizar_relacion_service(id_prod, id_prov, request.get_json())
    return jsonify(response), status

@inventario_bp.route('/proveedores/<id_prov>/productos', methods=['GET'])
@role_required(['PROPIETARIO', 'ADMIN'])
def get_products_by_provider(id_prov):
    response, status = obtener_productos_por_proveedor_service(id_prov)
    return jsonify(response), status

@inventario_bp.route('/relaciones-compras', methods=['GET'])
@role_required(['PROPIETARIO', 'ADMIN'])
def get_all_purchase_relations():
    response, status = obtener_todas_las_relaciones_service()
    return jsonify(response), status


# ================= RUTAS INVENTARIO =================

@inventario_bp.route('/inventarios', methods=['POST'])
@role_required(['PROPIETARIO', 'ADMIN']) 
def create_inventario():
    response, status = crear_inventario_service(request.get_json())
    return jsonify(response), status

@inventario_bp.route('/inventarios', methods=['GET'])
@role_required(['PROPIETARIO', 'ADMIN', 'VENDEDOR'])
def get_inventarios():
    response, status = obtener_inventarios_service()
    return jsonify(response), status

@inventario_bp.route('/inventarios/<id_inv>', methods=['GET'])
@role_required(['PROPIETARIO', 'ADMIN', 'VENDEDOR'])
def get_inventario(id_inv):
    response, status = obtener_inventario_id_service(id_inv)
    return jsonify(response), status

@inventario_bp.route('/inventarios/<id_inv>', methods=['PUT'])
@role_required(['PROPIETARIO', 'ADMIN'])
def update_inventario(id_inv):
    response, status = actualizar_inventario_service(id_inv, request.get_json())
    return jsonify(response), status

@inventario_bp.route('/inventarios/<id_inv>', methods=['DELETE'])
@role_required(['PROPIETARIO', 'ADMIN'])
def delete_inventario(id_inv):
    response, status = eliminar_inventario_service(id_inv)
    return jsonify(response), status