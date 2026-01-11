from app.extensions import db
from datetime import datetime
from app.models.inventario import Producto

class Cliente(db.Model):
    __tablename__ = 'cliente'
    
    id_cliente = db.Column(db.String(50), primary_key=True)
    # Si se borra la empresa, se borran los clientes
    id_empresa = db.Column(db.String(50), db.ForeignKey('empresa.id_empresa', ondelete='CASCADE'))
    
    nombre_completo = db.Column(db.String(255))
    nit_ci = db.Column(db.String(50))
    telefono = db.Column(db.String(50))
    email = db.Column(db.String(100))
    direccion = db.Column(db.Text)
    es_generico = db.Column(db.Boolean, default=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    total_compras = db.Column(db.Integer, default=0)
    monto_total_historico = db.Column(db.Numeric(15, 2), default=0.00)

    def to_dict(self):
        return {
            'id_cliente': self.id_cliente,
            'id_empresa': self.id_empresa,
            'nombre_completo': self.nombre_completo,
            'nit_ci': self.nit_ci,
            'telefono': self.telefono,
            'email': self.email,
            'direccion': self.direccion,
            'es_generico': self.es_generico,
            'total_compras': self.total_compras,
            'monto_total_historico': float(self.monto_total_historico or 0),
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None
        }

class Venta(db.Model):
    __tablename__ = 'venta'
    
    id_venta = db.Column(db.String(50), primary_key=True)
    
    # CASCADES: Si se borra Empresa, Cliente o Usuario, se borra la venta.
    # (Nota: En contabilidad real, a veces es mejor 'SET NULL' para no perder historial, 
    # pero pediste CASCADE, así que así lo configuramos).
    id_empresa = db.Column(db.String(50), db.ForeignKey('empresa.id_empresa', ondelete='CASCADE'))
    id_cliente = db.Column(db.String(50), db.ForeignKey('cliente.id_cliente', ondelete='CASCADE'))
    id_usuario = db.Column(db.String(50), db.ForeignKey('usuario.id_usuario', ondelete='CASCADE'))
    
    numero_factura = db.Column(db.String(100))
    subtotal = db.Column(db.Numeric(12, 2))
    impuesto = db.Column(db.Numeric(12, 2))
    descuento = db.Column(db.Numeric(12, 2))
    total = db.Column(db.Numeric(12, 2))
    fecha_venta = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.Boolean, default=True) # True = Valida, False = Anulada
    tipo_venta = db.Column(db.String(50)) # Contado, Crédito, etc.
    observaciones = db.Column(db.Text)

    # Restricción Unique
    __table_args__ = (db.UniqueConstraint('id_empresa', 'numero_factura', name='uk_factura_empresa'),)

    # Relaciones para facilitar consultas
    cliente = db.relationship('Cliente', backref=db.backref('ventas', cascade="all, delete-orphan"))
    usuario = db.relationship('app.models.seguridad.Usuario', backref='ventas_realizadas')

    def to_dict(self):
        return {
            'id_venta': self.id_venta,
            'id_empresa': self.id_empresa,
            'nombre_cliente': self.cliente.nombre_completo if self.cliente else None,
            'nombre_vendedor': self.usuario.nombre_completo if self.usuario else None,
            'numero_factura': self.numero_factura,
            'subtotal': float(self.subtotal or 0),
            'impuesto': float(self.impuesto or 0),
            'descuento': float(self.descuento or 0),
            'total': float(self.total or 0),
            'fecha_venta': self.fecha_venta.isoformat() if self.fecha_venta else None,
            'estado': self.estado,
            'tipo_venta': self.tipo_venta,
            'observaciones': self.observaciones
        }
    
class DetalleVenta(db.Model):
    __tablename__ = 'detalle_venta'
    
    id_detalle_venta = db.Column(db.String(50), primary_key=True)
    
    # Cascada: Si se borra la Venta O el Producto, se borra el detalle
    id_venta = db.Column(db.String(50), db.ForeignKey('venta.id_venta', ondelete='CASCADE'))
    id_producto = db.Column(db.String(50), db.ForeignKey('producto.id_producto', ondelete='CASCADE'))
    
    cantidad = db.Column(db.Integer)
    precio_unitario = db.Column(db.Numeric(12, 2))
    subtotal = db.Column(db.Numeric(12, 2))
    descuento_linea = db.Column(db.Numeric(12, 2), default=0.00)

    # Relación para obtener datos del producto (nombre, código) fácilmente
    producto = db.relationship('Producto', backref='detalles_ventas')

    def to_dict(self):
        return {
            'id_detalle_venta': self.id_detalle_venta,
            'id_venta': self.id_venta,
            'id_producto': self.id_producto,
            'nombre_producto': self.producto.nombre if self.producto else None,
            'cantidad': self.cantidad,
            'precio_unitario': float(self.precio_unitario or 0),
            'subtotal': float(self.subtotal or 0),
            'descuento_linea': float(self.descuento_linea or 0)
        }

class Pago(db.Model):
    __tablename__ = 'pago'
    
    id_pago = db.Column(db.String(50), primary_key=True)
    
    # Cascada: Si se borra la Venta, se borran sus pagos
    id_venta = db.Column(db.String(50), db.ForeignKey('venta.id_venta', ondelete='CASCADE'))
    
    metodo_pago = db.Column(db.String(50)) # Efectivo, Tarjeta, QR
    monto_pagado = db.Column(db.Numeric(12, 2))
    fecha_pago = db.Column(db.DateTime, default=datetime.utcnow)
    comprobante_url = db.Column(db.String(255))
    numero_transaccion = db.Column(db.String(100))
    estado = db.Column(db.String(50)) # Pendiente, Aprobado, Rechazado

    def to_dict(self):
        return {
            'id_pago': self.id_pago,
            'id_venta': self.id_venta,
            'metodo_pago': self.metodo_pago,
            'monto_pagado': float(self.monto_pagado or 0),
            'fecha_pago': self.fecha_pago.isoformat() if self.fecha_pago else None,
            'comprobante_url': self.comprobante_url,
            'numero_transaccion': self.numero_transaccion,
            'estado': self.estado
        }