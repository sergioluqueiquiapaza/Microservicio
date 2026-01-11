from app.extensions import db
from datetime import datetime
from app.models.inventario import Producto

class Compra(db.Model):
    __tablename__ = 'compra'
    
    id_compra = db.Column(db.String(50), primary_key=True)
    
    # Cascadas: Si se borra Empresa, Proveedor o Usuario, se borra la compra
    id_empresa = db.Column(db.String(50), db.ForeignKey('empresa.id_empresa', ondelete='CASCADE'))
    id_proveedor = db.Column(db.String(50), db.ForeignKey('proveedor.id_proveedor', ondelete='CASCADE'))
    id_usuario = db.Column(db.String(50), db.ForeignKey('usuario.id_usuario', ondelete='CASCADE'))
    
    numero_compra = db.Column(db.String(100))
    subtotal = db.Column(db.Numeric(12, 2))
    impuesto = db.Column(db.Numeric(12, 2))
    total = db.Column(db.Numeric(12, 2))
    fecha_compra = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_entrega_estimada = db.Column(db.DateTime)
    estado = db.Column(db.String(50)) # Solicitada, Recibida, Cancelada
    observaciones = db.Column(db.Text)

    __table_args__ = (db.UniqueConstraint('id_empresa', 'numero_compra', name='uk_compra_empresa'),)

    # Relaciones
    proveedor = db.relationship('app.models.inventario.Proveedor', backref='compras')
    usuario = db.relationship('app.models.seguridad.Usuario', backref='compras_registradas')

    def to_dict(self):
        return {
            'id_compra': self.id_compra,
            'id_empresa': self.id_empresa,
            'nombre_proveedor': self.proveedor.nombre if self.proveedor else None,
            'nombre_usuario': self.usuario.nombre_completo if self.usuario else None,
            'numero_compra': self.numero_compra,
            'subtotal': float(self.subtotal or 0),
            'impuesto': float(self.impuesto or 0),
            'total': float(self.total or 0),
            'fecha_compra': self.fecha_compra.isoformat() if self.fecha_compra else None,
            'fecha_entrega_estimada': self.fecha_entrega_estimada.isoformat() if self.fecha_entrega_estimada else None,
            'estado': self.estado,
            'observaciones': self.observaciones
        }
    
class DetalleCompra(db.Model):
    __tablename__ = 'detalle_compra'
    
    id_detalle_compra = db.Column(db.String(50), primary_key=True)
    
    # Cascada: Si se borra la compra o el producto, se elimina el detalle
    id_compra = db.Column(db.String(50), db.ForeignKey('compra.id_compra', ondelete='CASCADE'))
    id_producto = db.Column(db.String(50), db.ForeignKey('producto.id_producto', ondelete='CASCADE'))
    
    cantidad = db.Column(db.Integer)
    precio_unitario = db.Column(db.Numeric(12, 2))
    subtotal = db.Column(db.Numeric(12, 2))

    # Relación para traer nombre del producto fácilmente
    producto = db.relationship('Producto', backref='detalles_compras')

    def to_dict(self):
        return {
            'id_detalle_compra': self.id_detalle_compra,
            'id_compra': self.id_compra,
            'id_producto': self.id_producto,
            'nombre_producto': self.producto.nombre if self.producto else None,
            'cantidad': self.cantidad,
            'precio_unitario': float(self.precio_unitario or 0),
            'subtotal': float(self.subtotal or 0)
        }