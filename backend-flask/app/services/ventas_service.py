from app.extensions import db
from app.models.ventas import Cliente, Venta, DetalleVenta, Pago
import uuid

# ==================== CRUD CLIENTE ====================
def crear_cliente_service(data):
    try:
        if 'id_empresa' not in data:
            return {"error": "id_empresa es obligatorio"}, 400
            
        nuevo_id = data.get('id_cliente', str(uuid.uuid4()))
        cliente = Cliente(
            id_cliente=nuevo_id,
            id_empresa=data['id_empresa'],
            nombre_completo=data.get('nombre_completo'),
            nit_ci=data.get('nit_ci'),
            telefono=data.get('telefono'),
            email=data.get('email'),
            direccion=data.get('direccion'),
            es_generico=data.get('es_generico', False)
        )
        db.session.add(cliente)
        db.session.commit()
        return {"message": "Cliente creado", "cliente": cliente.to_dict()}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def obtener_clientes_service():
    clientes = Cliente.query.all()
    return [c.to_dict() for c in clientes], 200

def obtener_cliente_id_service(id_cli):
    cliente = Cliente.query.get(id_cli)
    return (cliente.to_dict(), 200) if cliente else ({"error": "Cliente no encontrado"}, 404)

def actualizar_cliente_service(id_cli, data):
    cliente = Cliente.query.get(id_cli)
    if not cliente: return {"error": "No encontrado"}, 404
    try:
        if 'nombre_completo' in data: cliente.nombre_completo = data['nombre_completo']
        if 'nit_ci' in data: cliente.nit_ci = data['nit_ci']
        if 'telefono' in data: cliente.telefono = data['telefono']
        if 'email' in data: cliente.email = data['email']
        if 'direccion' in data: cliente.direccion = data['direccion']
        
        db.session.commit()
        return {"message": "Cliente actualizado", "cliente": cliente.to_dict()}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def eliminar_cliente_service(id_cli):
    cliente = Cliente.query.get(id_cli)
    if not cliente: return {"error": "No encontrado"}, 404
    try:
        db.session.delete(cliente)
        db.session.commit()
        return {"message": "Cliente eliminado"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500


# ==================== CRUD VENTA ====================
def crear_venta_service(data):
    try:
        required = ['id_empresa', 'id_cliente', 'id_usuario', 'total']
        for campo in required:
            if campo not in data:
                return {"error": f"Falta el campo obligatorio: {campo}"}, 400

        nuevo_id = data.get('id_venta', str(uuid.uuid4()))
        venta = Venta(
            id_venta=nuevo_id,
            id_empresa=data['id_empresa'],
            id_cliente=data['id_cliente'],
            id_usuario=data['id_usuario'],
            numero_factura=data.get('numero_factura'),
            subtotal=data.get('subtotal', 0),
            impuesto=data.get('impuesto', 0),
            descuento=data.get('descuento', 0),
            total=data.get('total', 0),
            tipo_venta=data.get('tipo_venta', 'CONTADO'),
            observaciones=data.get('observaciones'),
            estado=True
        )
        db.session.add(venta)
        db.session.commit()
        return {"message": "Venta registrada", "venta": venta.to_dict()}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def obtener_ventas_service():
    ventas = Venta.query.all()
    return [v.to_dict() for v in ventas], 200

def obtener_venta_id_service(id_venta):
    venta = Venta.query.get(id_venta)
    return (venta.to_dict(), 200) if venta else ({"error": "Venta no encontrada"}, 404)

def eliminar_venta_service(id_venta):
    venta = Venta.query.get(id_venta)
    if not venta: return {"error": "No encontrado"}, 404
    try:
        db.session.delete(venta)
        db.session.commit()
        return {"message": "Venta eliminada"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

# ==================== CRUD DETALLE VENTA ====================
def crear_detalle_venta_service(data):
    try:
        if 'id_venta' not in data or 'id_producto' not in data:
            return {"error": "Faltan datos (id_venta, id_producto)"}, 400

        nuevo_id = data.get('id_detalle_venta', str(uuid.uuid4()))
        detalle = DetalleVenta(
            id_detalle_venta=nuevo_id,
            id_venta=data['id_venta'],
            id_producto=data['id_producto'],
            cantidad=data.get('cantidad', 1),
            precio_unitario=data.get('precio_unitario', 0),
            subtotal=data.get('subtotal', 0),
            descuento_linea=data.get('descuento_linea', 0)
        )
        db.session.add(detalle)
        db.session.commit()
        return {"message": "Detalle agregado", "detalle": detalle.to_dict()}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def obtener_detalles_por_venta_service(id_venta):
    # Función útil para listar items de una venta específica
    detalles = DetalleVenta.query.filter_by(id_venta=id_venta).all()
    return [d.to_dict() for d in detalles], 200

def eliminar_detalle_venta_service(id_detalle):
    detalle = DetalleVenta.query.get(id_detalle)
    if not detalle: return {"error": "No encontrado"}, 404
    try:
        db.session.delete(detalle)
        db.session.commit()
        return {"message": "Detalle eliminado"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500


# ==================== CRUD PAGO ====================
def crear_pago_service(data):
    try:
        if 'id_venta' not in data: return {"error": "id_venta es obligatorio"}, 400

        nuevo_id = data.get('id_pago', str(uuid.uuid4()))
        pago = Pago(
            id_pago=nuevo_id,
            id_venta=data['id_venta'],
            metodo_pago=data.get('metodo_pago'),
            monto_pagado=data.get('monto_pagado', 0),
            comprobante_url=data.get('comprobante_url'),
            numero_transaccion=data.get('numero_transaccion'),
            estado=data.get('estado', 'PENDIENTE')
        )
        db.session.add(pago)
        db.session.commit()
        return {"message": "Pago registrado", "pago": pago.to_dict()}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def obtener_pagos_service():
    pagos = Pago.query.all()
    return [p.to_dict() for p in pagos], 200

def obtener_pago_id_service(id_pago):
    pago = Pago.query.get(id_pago)
    return (pago.to_dict(), 200) if pago else ({"error": "No encontrado"}, 404)

def eliminar_pago_service(id_pago):
    pago = Pago.query.get(id_pago)
    if not pago: return {"error": "No encontrado"}, 404
    try:
        db.session.delete(pago)
        db.session.commit()
        return {"message": "Pago eliminado"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500