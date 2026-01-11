from app.extensions import db
from app.models.compras import Compra, DetalleCompra
import uuid

def crear_compra_service(data):
    try:
        required = ['id_empresa', 'id_proveedor', 'id_usuario']
        for campo in required:
            if campo not in data: return {"error": f"Falta {campo}"}, 400

        nuevo_id = data.get('id_compra', str(uuid.uuid4()))
        compra = Compra(
            id_compra=nuevo_id,
            id_empresa=data['id_empresa'],
            id_proveedor=data['id_proveedor'],
            id_usuario=data['id_usuario'],
            numero_compra=data.get('numero_compra'),
            subtotal=data.get('subtotal', 0),
            impuesto=data.get('impuesto', 0),
            total=data.get('total', 0),
            estado=data.get('estado', 'SOLICITADA'),
            observaciones=data.get('observaciones')
            # fecha_entrega_estimada se puede parsear si viene como string
        )
        db.session.add(compra)
        db.session.commit()
        return {"message": "Compra registrada", "compra": compra.to_dict()}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def obtener_compras_service():
    compras = Compra.query.all()
    return [c.to_dict() for c in compras], 200

def obtener_compra_id_service(id_compra):
    compra = Compra.query.get(id_compra)
    return (compra.to_dict(), 200) if compra else ({"error": "No encontrado"}, 404)

def actualizar_compra_service(id_compra, data):
    compra = Compra.query.get(id_compra)
    if not compra: return {"error": "Compra no encontrada"}, 404
    try:
        # Versión MEJORADA con todos los campos editables
        if 'estado' in data: compra.estado = data['estado']
        if 'numero_compra' in data: compra.numero_compra = data['numero_compra'] # Agregado
        if 'subtotal' in data: compra.subtotal = data['subtotal'] # Agregado
        if 'impuesto' in data: compra.impuesto = data['impuesto'] # Agregado
        if 'total' in data: compra.total = data['total']
        if 'observaciones' in data: compra.observaciones = data['observaciones']
        
        # Opcional: Permitir cambiar de proveedor si hubo error
        if 'id_proveedor' in data: compra.id_proveedor = data['id_proveedor'] 

        db.session.commit()
        return {"message": "Compra actualizada", "compra": compra.to_dict()}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def eliminar_compra_service(id_compra):
    compra = Compra.query.get(id_compra)
    if not compra: return {"error": "No encontrado"}, 404
    try:
        db.session.delete(compra)
        db.session.commit()
        return {"message": "Compra eliminada"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500
    
# ==================== CRUD DETALLE COMPRA ====================
def crear_detalle_compra_service(data):
    try:
        if 'id_compra' not in data or 'id_producto' not in data:
            return {"error": "Faltan datos obligatorios"}, 400

        nuevo_id = data.get('id_detalle_compra', str(uuid.uuid4()))
        detalle = DetalleCompra(
            id_detalle_compra=nuevo_id,
            id_compra=data['id_compra'],
            id_producto=data['id_producto'],
            cantidad=data.get('cantidad', 1),
            precio_unitario=data.get('precio_unitario', 0),
            subtotal=data.get('subtotal', 0)
        )
        db.session.add(detalle)
        db.session.commit()
        return {"message": "Detalle de compra agregado", "detalle": detalle.to_dict()}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def obtener_detalles_por_compra_service(id_compra):
    detalles = DetalleCompra.query.filter_by(id_compra=id_compra).all()
    return [d.to_dict() for d in detalles], 200

def eliminar_detalle_compra_service(id_detalle):
    detalle = DetalleCompra.query.get(id_detalle)
    if not detalle: return {"error": "No encontrado"}, 404
    try:
        db.session.delete(detalle)
        db.session.commit()
        return {"message": "Detalle eliminado"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500