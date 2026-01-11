from app.extensions import db
from app.models.soporte import Notificacion, Auditoria
import uuid
from datetime import datetime

# ==================== CRUD NOTIFICACIONES ====================
def crear_notificacion_service(data):
    try:
        nuevo_id = data.get('id_notificacion', str(uuid.uuid4()))
        noti = Notificacion(
            id_notificacion=nuevo_id,
            id_empresa=data.get('id_empresa'),
            id_usuario=data.get('id_usuario'),
            tipo=data.get('tipo'),
            categoria=data.get('categoria'),
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
        # 1. Estado de Lectura
        if 'leida' in data: 
            noti.leida = data['leida']
            # Si se marca como leída, actualizamos la fecha
            if data['leida']: 
                noti.fecha_lectura = datetime.utcnow()
            else:
                # Opcional: Si se marca como no leída, limpiamos la fecha
                noti.fecha_lectura = None
        
        # 2. Contenido (Lo que faltaba)
        if 'titulo' in data: noti.titulo = data['titulo']
        if 'mensaje' in data: noti.mensaje = data['mensaje']
        if 'tipo' in data: noti.tipo = data['tipo']
        if 'categoria' in data: noti.categoria = data['categoria']
        
        # 3. Datos JSON (Reemplazo total del JSON si se envía)
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
        nuevo_id = data.get('id_auditoria', str(uuid.uuid4()))
        audit = Auditoria(
            id_auditoria=nuevo_id,
            id_empresa=data.get('id_empresa'),
            id_usuario=data.get('id_usuario'),
            tabla_afectada=data.get('tabla_afectada'),
            accion=data.get('accion'),
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
    audit = Auditoria.query.get(id_audit)
    if not audit: return {"error": "No encontrada"}, 404
    try:
        db.session.delete(audit)
        db.session.commit()
        return {"message": "Registro eliminado"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500