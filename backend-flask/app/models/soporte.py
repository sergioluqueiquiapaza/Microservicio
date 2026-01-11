from app.extensions import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB

class Notificacion(db.Model):
    __tablename__ = 'notificacion'
    
    id_notificacion = db.Column(db.String(50), primary_key=True)
    
    # Cascada: Si se borra la empresa o usuario, adiós notificaciones
    id_empresa = db.Column(db.String(50), db.ForeignKey('empresa.id_empresa', ondelete='CASCADE'))
    id_usuario = db.Column(db.String(50), db.ForeignKey('usuario.id_usuario', ondelete='CASCADE'))
    
    tipo = db.Column(db.String(50)) # Ej: ALERTA, INFO, ERROR
    categoria = db.Column(db.String(50)) # Ej: INVENTARIO, VENTAS
    titulo = db.Column(db.String(255))
    mensaje = db.Column(db.Text)
    leida = db.Column(db.Boolean, default=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_lectura = db.Column(db.DateTime)
    datos_adicionales_json = db.Column(JSONB) # Datos extra flexibles

    def to_dict(self):
        return {
            'id_notificacion': self.id_notificacion,
            'id_empresa': self.id_empresa,
            'id_usuario': self.id_usuario,
            'tipo': self.tipo,
            'categoria': self.categoria,
            'titulo': self.titulo,
            'mensaje': self.mensaje,
            'leida': self.leida,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'datos_adicionales_json': self.datos_adicionales_json
        }

class Auditoria(db.Model):
    __tablename__ = 'auditoria'
    
    id_auditoria = db.Column(db.String(50), primary_key=True)
    
    # Cascada activada
    id_empresa = db.Column(db.String(50), db.ForeignKey('empresa.id_empresa', ondelete='CASCADE'))
    id_usuario = db.Column(db.String(50), db.ForeignKey('usuario.id_usuario', ondelete='CASCADE'))
    
    tabla_afectada = db.Column(db.String(100))
    accion = db.Column(db.String(50)) # INSERT, UPDATE, DELETE
    datos_anteriores_json = db.Column(JSONB)
    datos_nuevos_json = db.Column(JSONB)
    fecha_hora = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id_auditoria': self.id_auditoria,
            'id_empresa': self.id_empresa,
            'id_usuario': self.id_usuario,
            'tabla_afectada': self.tabla_afectada,
            'accion': self.accion,
            'datos_anteriores_json': self.datos_anteriores_json,
            'datos_nuevos_json': self.datos_nuevos_json,
            'fecha_hora': self.fecha_hora.isoformat() if self.fecha_hora else None
        }