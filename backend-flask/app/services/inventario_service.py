from app.extensions import db
from app.models.inventario import Categoria, Proveedor, Producto, ProductoProveedor, Inventario
import uuid

# ==================== CRUD CATEGORIA ====================

def crear_categoria_service(data):
    try:
        if 'id_empresa' not in data:
            return {"error": "id_empresa es obligatorio"}, 400

        nuevo_id = data.get('id_categoria', str(uuid.uuid4()))
        nueva_cat = Categoria(
            id_categoria=nuevo_id,
            id_empresa=data['id_empresa'],
            nombre=data.get('nombre'),
            descripcion=data.get('descripcion'),
            activo=data.get('activo', True),
            orden_visualizacion=data.get('orden_visualizacion', 0)
        )
        db.session.add(nueva_cat)
        db.session.commit()
        return {"message": "Categoría creada", "categoria": nueva_cat.to_dict()}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def obtener_categorias_service():
    # En producción deberías filtrar por id_empresa
    cats = Categoria.query.all()
    return [c.to_dict() for c in cats], 200

def obtener_categoria_por_id_service(id_categoria):
    cat = Categoria.query.get(id_categoria)
    if not cat:
        return {"error": "Categoría no encontrada"}, 404
    return cat.to_dict(), 200

def actualizar_categoria_service(id_categoria, data):
    cat = Categoria.query.get(id_categoria)
    if not cat:
        return {"error": "Categoría no encontrada"}, 404
    try:
        if 'nombre' in data: cat.nombre = data['nombre']
        if 'descripcion' in data: cat.descripcion = data['descripcion']
        if 'activo' in data: cat.activo = data['activo']
        if 'orden_visualizacion' in data: cat.orden_visualizacion = data['orden_visualizacion']
        
        db.session.commit()
        return {"message": "Categoría actualizada", "categoria": cat.to_dict()}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def eliminar_categoria_service(id_categoria):
    cat = Categoria.query.get(id_categoria)
    if not cat:
        return {"error": "Categoría no encontrada"}, 404
    try:
        db.session.delete(cat)
        db.session.commit()
        return {"message": "Categoría eliminada correctamente"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

# ==================== CRUD PROVEEDOR ====================
def crear_proveedor_service(data):
    try:
        # CAMBIO: nombre -> razon_social
        if 'id_empresa' not in data or 'razon_social' not in data:
            return {"error": "Faltan datos obligatorios (id_empresa, razon_social)"}, 400

        nuevo_id = data.get('id_proveedor', str(uuid.uuid4()))
        prov = Proveedor(
            id_proveedor=nuevo_id,
            id_empresa=data['id_empresa'],
            razon_social=data.get('razon_social'), # CAMBIO
            telefono=data.get('telefono'),
            email=data.get('email'),
            direccion=data.get('direccion'),
            nit_ruc=data.get('nit_ruc'),
            forma_pago=data.get('forma_pago'),
            activo=data.get('activo', True)
        )
        db.session.add(prov)
        db.session.commit()
        return {"message": "Proveedor creado", "proveedor": prov.to_dict()}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def obtener_proveedores_service():
    provs = Proveedor.query.all()
    return [p.to_dict() for p in provs], 200

def obtener_proveedor_id_service(id_prov):
    prov = Proveedor.query.get(id_prov)
    return (prov.to_dict(), 200) if prov else ({"error": "No encontrado"}, 404)

def actualizar_proveedor_service(id_prov, data):
    prov = Proveedor.query.get(id_prov)
    if not prov: return {"error": "No encontrado"}, 404
    try:
        # CAMBIO: nombre -> razon_social
        if 'razon_social' in data: prov.razon_social = data['razon_social']
        if 'telefono' in data: prov.telefono = data['telefono']
        if 'email' in data: prov.email = data['email']
        if 'direccion' in data: prov.direccion = data['direccion']
        if 'nit_ruc' in data: prov.nit_ruc = data['nit_ruc']
        if 'forma_pago' in data: prov.forma_pago = data['forma_pago']
        if 'activo' in data: prov.activo = data['activo']
        
        db.session.commit()
        return {"message": "Actualizado", "proveedor": prov.to_dict()}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def eliminar_proveedor_service(id_prov):
    prov = Proveedor.query.get(id_prov)
    if not prov: return {"error": "No encontrado"}, 404
    try:
        db.session.delete(prov)
        db.session.commit()
        return {"message": "Eliminado correctamente"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500


# ==================== CRUD PRODUCTO ====================
def crear_producto_service(data):
    try:
        if 'id_empresa' not in data:
            return {"error": "id_empresa obligatorio"}, 400
            
        nuevo_id = data.get('id_producto', str(uuid.uuid4()))
        prod = Producto(
            id_producto=nuevo_id,
            id_empresa=data['id_empresa'],
            id_categoria=data.get('id_categoria'),
            codigo_producto=data.get('codigo_producto'),
            nombre=data.get('nombre'),
            descripcion=data.get('descripcion'),
            precio_venta=data.get('precio_venta', 0),
            precio_compra=data.get('precio_compra', 0),
            unidad_medida=data.get('unidad_medida'),
            imagen_url=data.get('imagen_url'),
            activo=data.get('activo', True)
        )
        db.session.add(prod)
        db.session.commit()
        return {"message": "Producto creado", "producto": prod.to_dict()}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def obtener_productos_service():
    prods = Producto.query.all()
    return [p.to_dict() for p in prods], 200

def obtener_producto_id_service(id_prod):
    prod = Producto.query.get(id_prod)
    if not prod: return {"error": "Producto no encontrado"}, 404
    
    # Devolver también los proveedores asociados con sus precios especiales
    resultado = prod.to_dict()
    # rel.to_dict() ya devuelve 'nombre_proveedor' (que viene de razon_social) gracias al cambio en models
    resultado['proveedores_asociados'] = [rel.to_dict() for rel in prod.proveedores_vinculados]
    return resultado, 200

def actualizar_producto_service(id_prod, data):
    prod = Producto.query.get(id_prod)
    if not prod: return {"error": "No encontrado"}, 404
    try:
        if 'nombre' in data: prod.nombre = data['nombre']
        if 'codigo_producto' in data: prod.codigo_producto = data['codigo_producto']
        if 'precio_venta' in data: prod.precio_venta = data['precio_venta']
        if 'precio_compra' in data: prod.precio_compra = data['precio_compra']
        if 'unidad_medida' in data: prod.unidad_medida = data['unidad_medida']
        if 'imagen_url' in data: prod.imagen_url = data['imagen_url']
        if 'id_categoria' in data: prod.id_categoria = data['id_categoria']
        
        db.session.commit()
        return {"message": "Actualizado", "producto": prod.to_dict()}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def eliminar_producto_service(id_prod):
    prod = Producto.query.get(id_prod)
    if not prod: return {"error": "No encontrado"}, 404
    try:
        db.session.delete(prod)
        db.session.commit()
        return {"message": "Eliminado"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500


# ==================== RELACIÓN PRODUCTO - PROVEEDOR ====================
def asignar_proveedor_a_producto_service(id_producto, data):
    try:
        id_proveedor = data.get('id_proveedor')
        if not id_proveedor: return {"error": "id_proveedor es necesario"}, 400
        
        # Verificar duplicados
        existe = ProductoProveedor.query.filter_by(id_producto=id_producto, id_proveedor=id_proveedor).first()
        if existe: return {"error": "Relación ya existe"}, 400

        relacion = ProductoProveedor(
            id_producto=id_producto,
            id_proveedor=id_proveedor,
            precio_compra=data.get('precio_compra', 0),
            tiempo_entrega_dias=data.get('tiempo_entrega_dias', 0),
            proveedor_preferido=data.get('proveedor_preferido', False)
        )
        db.session.add(relacion)
        db.session.commit()
        return {"message": "Proveedor asignado", "relacion": relacion.to_dict()}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def desvincular_proveedor_producto_service(id_producto, id_proveedor):
    try:
        relacion = ProductoProveedor.query.filter_by(id_producto=id_producto, id_proveedor=id_proveedor).first()
        if not relacion: return {"error": "Relación no encontrada"}, 404
            
        db.session.delete(relacion)
        db.session.commit()
        return {"message": "Desvinculado correctamente"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def actualizar_relacion_service(id_producto, id_proveedor, data):
    """
    Permite editar el precio, días de entrega o preferencia de una relación existente.
    """
    relacion = ProductoProveedor.query.filter_by(id_producto=id_producto, id_proveedor=id_proveedor).first()
    if not relacion:
        return {"error": "La relación entre este producto y proveedor no existe"}, 404
    
    try:
        if 'precio_compra' in data: 
            relacion.precio_compra = data['precio_compra']
        
        if 'tiempo_entrega_dias' in data: 
            relacion.tiempo_entrega_dias = data['tiempo_entrega_dias']
            
        if 'proveedor_preferido' in data: 
            relacion.proveedor_preferido = data['proveedor_preferido']
            
        db.session.commit()
        return {"message": "Datos de compra actualizados", "relacion": relacion.to_dict()}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def obtener_productos_por_proveedor_service(id_proveedor):
    """
    Lista todos los productos que vende un proveedor específico.
    """
    prov = Proveedor.query.get(id_proveedor)
    if not prov:
        return {"error": "Proveedor no encontrado"}, 404
        
    lista_productos = []
    # Usamos la relación definida en el modelo
    for relacion in prov.productos_vinculados:
        datos_prod = relacion.producto.to_dict()
        datos_prod['datos_compra'] = {
            'precio_pactado': float(relacion.precio_compra),
            'tiempo_entrega': relacion.tiempo_entrega_dias,
            'es_preferido': relacion.proveedor_preferido
        }
        lista_productos.append(datos_prod)
        
    return lista_productos, 200

def obtener_todas_las_relaciones_service():
    """
    Lista TODAS las relaciones (útil para reportes globales de compras).
    """
    relaciones = ProductoProveedor.query.all()
    resultado = []
    for rel in relaciones:
        dic = rel.to_dict()
        dic['nombre_producto'] = rel.producto.nombre
        # CAMBIO: Usamos razon_social en lugar de nombre
        dic['nombre_proveedor'] = rel.proveedor.razon_social
        resultado.append(dic)
    return resultado, 200

# ==================== CRUD INVENTARIO ====================
def crear_inventario_service(data):
    try:
        if 'id_producto' not in data:
            return {"error": "id_producto es obligatorio"}, 400
            
        nuevo_id = data.get('id_inventario', str(uuid.uuid4()))
        inv = Inventario(
            id_inventario=nuevo_id,
            id_producto=data['id_producto'],
            cantidad_actual=data.get('cantidad_actual', 0),
            stock_minimo=data.get('stock_minimo', 0),
            stock_maximo=data.get('stock_maximo'),
            ubicacion_fisica=data.get('ubicacion_fisica')
        )
        db.session.add(inv)
        db.session.commit()
        return {"message": "Registro de inventario creado", "inventario": inv.to_dict()}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def obtener_inventarios_service():
    items = Inventario.query.all()
    return [i.to_dict() for i in items], 200

def obtener_inventario_id_service(id_inv):
    item = Inventario.query.get(id_inv)
    return (item.to_dict(), 200) if item else ({"error": "No encontrado"}, 404)

def actualizar_inventario_service(id_inv, data):
    item = Inventario.query.get(id_inv)
    if not item: return {"error": "No encontrado"}, 404
    try:
        if 'cantidad_actual' in data: item.cantidad_actual = data['cantidad_actual']
        if 'stock_minimo' in data: item.stock_minimo = data['stock_minimo']
        if 'stock_maximo' in data: item.stock_maximo = data['stock_maximo']
        if 'ubicacion_fisica' in data: item.ubicacion_fisica = data['ubicacion_fisica']
        
        db.session.commit()
        return {"message": "Inventario actualizado", "inventario": item.to_dict()}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def eliminar_inventario_service(id_inv):
    item = Inventario.query.get(id_inv)
    if not item: return {"error": "No encontrado"}, 404
    try:
        db.session.delete(item)
        db.session.commit()
        return {"message": "Eliminado"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500