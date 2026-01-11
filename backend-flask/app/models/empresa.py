from app.extensions import db
from datetime import datetime
import uuid

class Empresa(db.Model):
    __tablename__ = 'empresa'
    
    id_empresa = db.Column(db.String(50), primary_key=True)
    tenant_id = db.Column(db.String(36), unique=True, default=lambda: str(uuid.uuid4()))
    nombre_comercial = db.Column(db.String(255))
    razon_social = db.Column(db.String(255))
    nit_ruc = db.Column(db.String(50))
    telefono = db.Column(db.String(50))
    email = db.Column(db.String(100))
    direccion = db.Column(db.Text)
    logo_url = db.Column(db.String(255))
    horario_atencion = db.Column(db.String(100))
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)

    # cascade="all, delete-orphan" para borrar planes/config si se borra la empresa
    planes = db.relationship('PlanSuscripcion', backref='empresa', lazy=True, cascade="all, delete-orphan")
    configuracion = db.relationship('ConfiguracionEmpresa', backref='empresa', uselist=False, lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id_empresa': self.id_empresa,
            'tenant_id': self.tenant_id,  # Importante para multi-tenancy
            'nombre_comercial': self.nombre_comercial,
            'razon_social': self.razon_social,
            'nit_ruc': self.nit_ruc,
            'telefono': self.telefono,
            'email': self.email,
            'direccion': self.direccion,
            'logo_url': self.logo_url,      # Ahora el frontend podrá ver el logo
            'horario_atencion': self.horario_atencion,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None,
            'activo': self.activo
        }

# --- PLAN SUSCRIPCION (Actualizado completo) ---
class PlanSuscripcion(db.Model):
    __tablename__ = 'plan_suscripcion'
    id_plan = db.Column(db.String(50), primary_key=True)
    id_empresa = db.Column(db.String(50), db.ForeignKey('empresa.id_empresa'), nullable=False)
    tipo_plan = db.Column(db.String(50))
    precio_mensual = db.Column(db.Numeric(12, 2))
    fecha_inicio = db.Column(db.Date)
    fecha_vencimiento = db.Column(db.Date)
    activo = db.Column(db.Boolean, default=True)
    max_usuarios = db.Column(db.Integer)
    max_productos = db.Column(db.Integer)
    acceso_reportes_avanzados = db.Column(db.Boolean)

    def to_dict(self):
        return {
            'id_plan': self.id_plan,
            'id_empresa': self.id_empresa,
            'tipo_plan': self.tipo_plan,
            'precio_mensual': float(self.precio_mensual) if self.precio_mensual else 0.0,
            'fecha_inicio': str(self.fecha_inicio) if self.fecha_inicio else None,
            'fecha_vencimiento': str(self.fecha_vencimiento) if self.fecha_vencimiento else None,
            'activo': self.activo,
            'max_usuarios': self.max_usuarios,
            'max_productos': self.max_productos,
            'acceso_reportes_avanzados': self.acceso_reportes_avanzados
        }

# --- CONFIGURACION EMPRESA (Actualizado completo) ---
class ConfiguracionEmpresa(db.Model):
    __tablename__ = 'configuracion_empresa'
    id_config = db.Column(db.String(50), primary_key=True)
    id_empresa = db.Column(db.String(50), db.ForeignKey('empresa.id_empresa'), nullable=False)
    moneda_default = db.Column(db.String(10))
    impuesto_iva = db.Column(db.Numeric(5, 2))
    formato_factura = db.Column(db.String(50))
    notif_stock_minimo = db.Column(db.Boolean, default=True)
    notif_ventas = db.Column(db.Boolean, default=True)
    zona_horaria = db.Column(db.String(50))

    def to_dict(self):
        return {
            'id_config': self.id_config,
            'id_empresa': self.id_empresa,
            'moneda_default': self.moneda_default,
            'impuesto_iva': float(self.impuesto_iva) if self.impuesto_iva else 0.0,
            'formato_factura': self.formato_factura,
            'notif_stock_minimo': self.notif_stock_minimo,
            'notif_ventas': self.notif_ventas,
            'zona_horaria': self.zona_horaria
        }