from app.extensions import db
from app.models.soporte import Notificacion, Auditoria
import uuid
from datetime import datetime

# ==================== CRUD NOTIFICACIONES ====================
def crear_notificacion_service(data):
    try:
        # Validaciones de integridad (Evitar error 500 si faltan datos)
        if 'id_empresa' not in data or 'id_usuario' not in data:
            return {"error": "Faltan datos obligatorios (id_empresa, id_usuario)"}, 400

        nuevo_id = data.get('id_notificacion', str(uuid.uuid4()))
        noti = Notificacion(
            id_notificacion=nuevo_id,
            id_empresa=data['id_empresa'],
            id_usuario=data['id_usuario'],
            tipo=data.get('tipo', 'INFO'),
            categoria=data.get('categoria', 'GENERAL'),
            titulo=data.get('titulo'),
            mensaje=data.get('mensaje'),
            datos_adicionales_json=data.get('datos_adicionales_json', {})
        )
        db.session.add(noti)
        db.session.commit()
        return {"message": "Notificación creada", "notificacion": noti.to_dict()}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def obtener_notificaciones_service():
    # Nota: En un futuro SaaS real, aquí deberías filtrar por id_empresa
    notis = Notificacion.query.all()
    return [n.to_dict() for n in notis], 200

def obtener_notificacion_id_service(id_noti):
    noti = Notificacion.query.get(id_noti)
    return (noti.to_dict(), 200) if noti else ({"error": "No encontrada"}, 404)

def actualizar_notificacion_service(id_noti, data):
    noti = Notificacion.query.get(id_noti)
    if not noti: 
        return {"error": "Notificación no encontrada"}, 404
    
    try:
        # 1. Lógica de "Leída" automática
        if 'leida' in data: 
            noti.leida = data['leida']
            if data['leida']: 
                noti.fecha_lectura = datetime.utcnow()
            else:
                noti.fecha_lectura = None
        
        # 2. Actualizar contenido
        if 'titulo' in data: noti.titulo = data['titulo']
        if 'mensaje' in data: noti.mensaje = data['mensaje']
        if 'tipo' in data: noti.tipo = data['tipo']
        if 'categoria' in data: noti.categoria = data['categoria']
        
        # 3. Datos JSON
        if 'datos_adicionales_json' in data: 
            noti.datos_adicionales_json = data['datos_adicionales_json']
        
        db.session.commit()
        return {"message": "Notificación actualizada", "notificacion": noti.to_dict()}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def eliminar_notificacion_service(id_noti):
    noti = Notificacion.query.get(id_noti)
    if not noti: return {"error": "No encontrada"}, 404
    try:
        db.session.delete(noti)
        db.session.commit()
        return {"message": "Notificación eliminada"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

# ==================== CRUD AUDITORIA ====================
def crear_auditoria_service(data):
    try:
        # Validar campos críticos para que el log sea útil
        required = ['id_empresa', 'id_usuario', 'tabla_afectada', 'accion']
        for campo in required:
            if campo not in data: return {"error": f"Falta campo obligatorio: {campo}"}, 400

        nuevo_id = data.get('id_auditoria', str(uuid.uuid4()))
        audit = Auditoria(
            id_auditoria=nuevo_id,
            id_empresa=data['id_empresa'],
            id_usuario=data['id_usuario'],
            tabla_afectada=data['tabla_afectada'],
            accion=data['accion'], # Ej: INSERT, UPDATE, DELETE
            datos_anteriores_json=data.get('datos_anteriores_json', {}),
            datos_nuevos_json=data.get('datos_nuevos_json', {})
        )
        db.session.add(audit)
        db.session.commit()
        return {"message": "Registro de auditoría creado", "auditoria": audit.to_dict()}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def obtener_auditorias_service():
    audits = Auditoria.query.all()
    return [a.to_dict() for a in audits], 200

def obtener_auditoria_id_service(id_audit):
    audit = Auditoria.query.get(id_audit)
    return (audit.to_dict(), 200) if audit else ({"error": "No encontrada"}, 404)

def eliminar_auditoria_service(id_audit):
    # Nota: Generalmente las auditorías NO deberían borrarse, pero lo dejamos por si acaso.
    audit = Auditoria.query.get(id_audit)
    if not audit: return {"error": "No encontrada"}, 404
    try:
        db.session.delete(audit)
        db.session.commit()
        return {"message": "Registro eliminado"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500