from app.extensions import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

class AdminSaas(db.Model):
    __tablename__ = 'admin_saas'

    id_admin = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password_hash = db.Column(db.String(255))
    rol = db.Column(db.String(50))
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, server_default=func.now())

    # Relación inversa: Un Admin puede crear muchos Planes
    planes = db.relationship('Plan', backref='admin_creador', lazy=True)

    def to_dict(self):
        return {
            'id_admin': str(self.id_admin),
            'nombre': self.nombre,
            'email': self.email,
            'rol': self.rol,
            'activo': self.activo,
            'fecha_creacion': self.fecha_creacion
        }

class Plan(db.Model):
    __tablename__ = 'plan'

    id_plan = db.Column(db.String(50), primary_key=True)
    
    # Aquí aplicamos el ON DELETE SET NULL
    id_admin = db.Column(UUID(as_uuid=True), db.ForeignKey('admin_saas.id_admin', ondelete='SET NULL'), nullable=True)
    
    nombre = db.Column(db.String(255))
    precio_mensual = db.Column(db.Numeric(12, 2))
    max_usuarios = db.Column(db.Integer)
    max_productos = db.Column(db.Integer)
    acceso_reportes_avanzados = db.Column(db.Boolean)
    activo = db.Column(db.Boolean, default=True)

    # Relación inversa: Un Plan puede tener muchas Suscripciones
    suscripciones = db.relationship('Suscripcion', backref='plan', lazy=True)

    def to_dict(self):
        return {
            'id_plan': self.id_plan,
            'id_admin': str(self.id_admin) if self.id_admin else None,
            'nombre': self.nombre,
            'precio_mensual': float(self.precio_mensual) if self.precio_mensual else 0.0,
            'max_usuarios': self.max_usuarios,
            'max_productos': self.max_productos,
            'acceso_reportes_avanzados': self.acceso_reportes_avanzados,
            'activo': self.activo
        }

class Suscripcion(db.Model):
    __tablename__ = 'suscripcion'

    id_suscripcion = db.Column(db.String(50), primary_key=True)
    
    # Relación con Empresa (ON DELETE CASCADE)
    # Nota: 'empresa.id_empresa' asume que la tabla empresa se llama 'empresa' en la DB
    id_empresa = db.Column(db.String(50), db.ForeignKey('empresa.id_empresa', ondelete='CASCADE'), nullable=False)
    
    # Relación con Plan
    id_plan = db.Column(db.String(50), db.ForeignKey('plan.id_plan'), nullable=True)
    
    fecha_inicio = db.Column(db.DateTime)
    fecha_fin = db.Column(db.DateTime)
    estado = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id_suscripcion': self.id_suscripcion,
            'id_empresa': self.id_empresa,
            'id_plan': self.id_plan,
            'fecha_inicio': self.fecha_inicio,
            'fecha_fin': self.fecha_fin,
            'estado': self.estado
        }