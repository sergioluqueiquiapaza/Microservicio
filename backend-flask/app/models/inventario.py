from app.extensions import db
from datetime import datetime

class Categoria(db.Model):
    __tablename__ = 'categoria'
    id_categoria = db.Column(db.String(50), primary_key=True)
    id_empresa = db.Column(db.String(50), db.ForeignKey('empresa.id_empresa', ondelete='CASCADE'), nullable=False)
    nombre = db.Column(db.String(100))
    descripcion = db.Column(db.Text)
    activo = db.Column(db.Boolean, default=True)
    orden_visualizacion = db.Column(db.Integer, default=0)
    
    # Si borro categoría, borro productos (opcional, si no quieres esto, quita el cascade)
    productos = db.relationship('Producto', backref='categoria', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {'id_categoria': self.id_categoria, 'id_empresa': self.id_empresa, 'nombre': self.nombre, 'descripcion': self.descripcion, 'activo': self.activo}

class Proveedor(db.Model):
    __tablename__ = 'proveedor'
    
    id_proveedor = db.Column(db.String(50), primary_key=True)
    # Cascade configurado para cuando borres la tabla y la recrees
    id_empresa = db.Column(db.String(50), db.ForeignKey('empresa.id_empresa', ondelete='CASCADE'), nullable=False)
    
    # Campos corregidos según tu SQL
    nombre = db.Column(db.String(255))
    telefono = db.Column(db.String(50))
    email = db.Column(db.String(100))
    direccion = db.Column(db.Text)
    nit_ruc = db.Column(db.String(50))
    forma_pago = db.Column(db.Text)
    activo = db.Column(db.Boolean, default=True)

    # Relación inversa (opcional, para acceder desde proveedor a sus productos vinculados)
    productos_vinculados = db.relationship('ProductoProveedor', backref='proveedor', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id_proveedor': self.id_proveedor,
            'id_empresa': self.id_empresa,
            'nombre': self.nombre,
            'telefono': self.telefono,
            'email': self.email,
            'direccion': self.direccion,
            'nit_ruc': self.nit_ruc,
            'forma_pago': self.forma_pago,
            'activo': self.activo
        }

class Producto(db.Model):
    __tablename__ = 'producto'
    
    id_producto = db.Column(db.String(50), primary_key=True)
    id_empresa = db.Column(db.String(50), db.ForeignKey('empresa.id_empresa', ondelete='CASCADE'), nullable=False)
    id_categoria = db.Column(db.String(50), db.ForeignKey('categoria.id_categoria', ondelete='CASCADE'))
    
    # Campos exactos de tu SQL
    codigo_producto = db.Column(db.String(100))
    nombre = db.Column(db.String(255))
    descripcion = db.Column(db.Text)
    precio_venta = db.Column(db.Numeric(12, 2))
    precio_compra = db.Column(db.Numeric(12, 2)) # Precio base de compra
    unidad_medida = db.Column(db.String(50))
    imagen_url = db.Column(db.String(255))
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    # Relación inversa
    proveedores_vinculados = db.relationship('ProductoProveedor', backref='producto', lazy=True, cascade="all, delete-orphan")

    # Restricción Unique (Opcional en SQLAlchemy si ya está en BD, pero buena práctica)
    __table_args__ = (db.UniqueConstraint('id_empresa', 'codigo_producto', name='uk_codigo_empresa'),)

    def to_dict(self):
        return {
            'id_producto': self.id_producto,
            'id_empresa': self.id_empresa,
            'id_categoria': self.id_categoria,
            'codigo_producto': self.codigo_producto,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio_venta': float(self.precio_venta) if self.precio_venta else 0.0,
            'precio_compra': float(self.precio_compra) if self.precio_compra else 0.0,
            'unidad_medida': self.unidad_medida,
            'imagen_url': self.imagen_url,
            'activo': self.activo,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }

class ProductoProveedor(db.Model):
    __tablename__ = 'producto_proveedor'
    
    id_producto = db.Column(db.String(50), db.ForeignKey('producto.id_producto', ondelete='CASCADE'), primary_key=True)
    id_proveedor = db.Column(db.String(50), db.ForeignKey('proveedor.id_proveedor', ondelete='CASCADE'), primary_key=True)
    
    precio_compra = db.Column(db.Numeric(12, 2)) # Precio pactado con este proveedor específico
    tiempo_entrega_dias = db.Column(db.Integer)
    proveedor_preferido = db.Column(db.Boolean, default=False)

    def to_dict(self):
        # self.proveedor existe gracias al backref en la clase Proveedor
        return {
            'id_producto': self.id_producto,
            'id_proveedor': self.id_proveedor,
            'nombre_proveedor': self.proveedor.nombre if self.proveedor else None,
            'precio_compra': float(self.precio_compra) if self.precio_compra else 0.0,
            'tiempo_entrega_dias': self.tiempo_entrega_dias,
            'proveedor_preferido': self.proveedor_preferido
        }

class Inventario(db.Model):
    __tablename__ = 'inventario'
    
    id_inventario = db.Column(db.String(50), primary_key=True)
    # Si borro el producto, se borra su registro de inventario
    id_producto = db.Column(db.String(50), db.ForeignKey('producto.id_producto', ondelete='CASCADE'))
    
    cantidad_actual = db.Column(db.Integer, default=0)
    stock_minimo = db.Column(db.Integer, default=0)
    stock_maximo = db.Column(db.Integer)
    ubicacion_fisica = db.Column(db.String(100))
    ultima_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relación para acceder a info del producto desde aquí
    producto = db.relationship('Producto', backref=db.backref('inventario_items', cascade="all, delete-orphan"))

    def to_dict(self):
        return {
            'id_inventario': self.id_inventario,
            'id_producto': self.id_producto,
            'nombre_producto': self.producto.nombre if self.producto else None,
            'cantidad_actual': self.cantidad_actual,
            'stock_minimo': self.stock_minimo,
            'stock_maximo': self.stock_maximo,
            'ubicacion_fisica': self.ubicacion_fisica,
            'ultima_actualizacion': self.ultima_actualizacion.isoformat() if self.ultima_actualizacion else None
        }