from app.extensions import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB

class Rol(db.Model):
    __tablename__ = 'rol'
    id_rol = db.Column(db.String(50), primary_key=True)
    nombre = db.Column(db.String(100))
    permisos_json = db.Column(JSONB)
    descripcion = db.Column(db.Text)
    
    # Cascade en la relación de SQLAlchemy (ayuda a limpiar la sesión)
    usuarios = db.relationship('Usuario', backref='rol', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {'id_rol': self.id_rol, 'nombre': self.nombre, 'permisos_json': self.permisos_json, 'descripcion': self.descripcion}

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id_usuario = db.Column(db.String(50), primary_key=True) # Faltaba declarar la PK explícitamente en tu código anterior
    
    id_empresa = db.Column(db.String(50), db.ForeignKey('empresa.id_empresa', ondelete='CASCADE'), nullable=False)
    
    # CAMBIO IMPORTANTE: ON DELETE SET NULL (Según tu SQL)
    id_rol = db.Column(db.String(50), db.ForeignKey('rol.id_rol', ondelete='SET NULL')) 
    
    # Nombres atomizados
    nombres = db.Column(db.String(100))
    apellido_paterno = db.Column(db.String(100))
    apellido_materno = db.Column(db.String(100))
    
    email = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(255))
    telefono = db.Column(db.String(50))
    activo = db.Column(db.Boolean, default=True)
    ultimo_acceso = db.Column(db.DateTime)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    token_recuperacion = db.Column(db.String(255))
    token_expiracion = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'id_usuario': self.id_usuario, 
            'id_empresa': self.id_empresa, 
            'id_rol': self.id_rol,
            'nombre_rol': self.rol.nombre if self.rol else None,
            # Devolvemos los nombres separados
            'nombres': self.nombres,
            'apellido_paterno': self.apellido_paterno,
            'apellido_materno': self.apellido_materno,
            # Campo auxiliar por si el frontend necesita el nombre completo string
            'nombre_completo_str': f"{self.nombres} {self.apellido_paterno}".strip(),
            'email': self.email, 
            'telefono': self.telefono, 
            'activo': self.activo
        }