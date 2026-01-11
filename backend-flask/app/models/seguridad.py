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
    id_usuario = db.Column(db.String(50), primary_key=True)
    
    # AQUÍ ESTÁ LA MAGIA DEL CASCADE EN LA BASE DE DATOS:
    id_empresa = db.Column(db.String(50), db.ForeignKey('empresa.id_empresa', ondelete='CASCADE'), nullable=False)
    id_rol = db.Column(db.String(50), db.ForeignKey('rol.id_rol', ondelete='CASCADE')) # OJO: Si borras rol, se borra usuario
    
    nombre_completo = db.Column(db.String(255))
    email = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(255))
    telefono = db.Column(db.String(50))
    activo = db.Column(db.Boolean, default=True)
    ultimo_acceso = db.Column(db.DateTime)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        # ... (mismo to_dict de antes) ...
        return {'id_usuario': self.id_usuario, 'id_empresa': self.id_empresa, 'id_rol': self.id_rol, 'nombre_completo': self.nombre_completo, 'email': self.email, 'telefono': self.telefono, 'activo': self.activo}