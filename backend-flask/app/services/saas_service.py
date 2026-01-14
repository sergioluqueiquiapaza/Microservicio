from app.extensions import db
from app.models.saas import AdminSaas, Plan, Suscripcion
from app.models.token_blocklist import TokenBlocklist
from app.models.empresa import Empresa
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, get_jwt
import uuid
from datetime import datetime

# ==========================================
# ADMINISTRADORES SAAS (CRUD & AUTH)
# ==========================================

def crear_admin_saas_service(data):
    try:
        # Validar campos obligatorios
        if not data.get('email') or not data.get('password'):
            return {"error": "Email y contraseña son obligatorios"}, 400
        
        # Verificar si ya existe
        if AdminSaas.query.filter_by(email=data['email']).first():
            return {"error": "El email ya está registrado como administrador"}, 400
        
        # Encriptar contraseña
        pass_hash = generate_password_hash(data['password'])
        
        nuevo_admin = AdminSaas(
            nombre=data.get('nombre'),
            email=data.get('email'),
            password_hash=pass_hash,
            rol=data.get('rol', 'SUPER_ADMIN'),
            activo=True
        )
        
        db.session.add(nuevo_admin)
        db.session.commit()
        
        return {"message": "Administrador SaaS creado", "admin": nuevo_admin.to_dict()}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def login_admin_saas_service(data):
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return {"error": "Email y contraseña requeridos"}, 400
    
    admin = AdminSaas.query.filter_by(email=email).first()
    
    if admin and check_password_hash(admin.password_hash, password):
        if not admin.activo:
            return {"error": "Cuenta desactivada"}, 401
        
        additional_claims = {"rol": "SUPER_ADMIN", "tipo": "SAAS"}
        token = create_access_token(identity=str(admin.id_admin), additional_claims=additional_claims)
        
        return {
            "message": "Login exitoso",
            "token": token,
            "admin": {
                "id": str(admin.id_admin),
                "nombre": admin.nombre,
                "email": admin.email
            }
        }, 200
    
    return {"error": "Credenciales inválidas"}, 401

def logout_admin_saas_service():
    try:
        jti = get_jwt()["jti"]
        revoked_token = TokenBlocklist(jti=jti)
        db.session.add(revoked_token)
        db.session.commit()
        
        return {"message": "Admin SaaS: Sesión cerrada correctamente"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": "Error al cerrar sesión: " + str(e)}, 500

def obtener_admins_saas_service():
    # Solo admins activos
    admins = AdminSaas.query.filter_by(activo=True).all()
    return [a.to_dict() for a in admins], 200

def obtener_admin_saas_por_id_service(id_admin):
    admin = AdminSaas.query.get(id_admin)
    if not admin:
        return {"error": "Administrador no encontrado"}, 404
    return admin.to_dict(), 200

def actualizar_admin_saas_service(id_admin, data):
    admin = AdminSaas.query.get(id_admin)
    if not admin:
        return {"error": "Administrador no encontrado"}, 404
    
    try:
        if 'nombre' in data:
            admin.nombre = data['nombre']
        if 'email' in data:
            # Verificar que el email no esté en uso por otro admin
            existing = AdminSaas.query.filter_by(email=data['email']).first()
            if existing and str(existing.id_admin) != id_admin:
                return {"error": "El email ya está en uso"}, 400
            admin.email = data['email']
        if 'password' in data and data['password']:
            admin.password_hash = generate_password_hash(data['password'])
        
        db.session.commit()
        return {"message": "Administrador actualizado", "admin": admin.to_dict()}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def desactivar_admin_saas_service(id_admin):
    """Desactiva un admin (eliminación lógica)"""
    admin = AdminSaas.query.get(id_admin)
    if not admin:
        return {"error": "Administrador no encontrado"}, 404
    
    try:
        admin.activo = False
        db.session.commit()
        return {"message": "Administrador desactivado correctamente"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def activar_admin_saas_service(id_admin):
    """Reactiva un admin desactivado"""
    admin = AdminSaas.query.get(id_admin)
    if not admin:
        return {"error": "Administrador no encontrado"}, 404
    
    try:
        admin.activo = True
        db.session.commit()
        return {"message": "Administrador activado correctamente"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def obtener_admins_saas_inactivos_service():
    """Obtiene todos los admins desactivados"""
    admins = AdminSaas.query.filter_by(activo=False).all()
    return [a.to_dict() for a in admins], 200

# ==========================================
# PLANES (CATÁLOGO)
# ==========================================

def crear_plan_service(data):
    try:
        if 'id_plan' not in data:
            return {"error": "El id_plan (código único) es obligatorio"}, 400
        
        if Plan.query.get(data['id_plan']):
            return {"error": "Ya existe un plan con ese ID"}, 400
        
        nuevo_plan = Plan(
            id_plan=data['id_plan'],
            id_admin=data.get('id_admin'),
            nombre=data.get('nombre'),
            precio_mensual=data.get('precio_mensual', 0),
            max_usuarios=data.get('max_usuarios'),
            max_productos=data.get('max_productos'),
            acceso_reportes_avanzados=data.get('acceso_reportes_avanzados', False),
            activo=data.get('activo', True)
        )
        
        db.session.add(nuevo_plan)
        db.session.commit()
        return {"message": "Plan creado correctamente", "plan": nuevo_plan.to_dict()}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def obtener_planes_service():
    planes = Plan.query.all()
    return [p.to_dict() for p in planes], 200

def obtener_plan_id_service(id_plan):
    plan = Plan.query.get(id_plan)
    return (plan.to_dict(), 200) if plan else ({"error": "Plan no encontrado"}, 404)

def actualizar_plan_service(id_plan, data):
    plan = Plan.query.get(id_plan)
    if not plan:
        return {"error": "Plan no encontrado"}, 404
    
    try:
        if 'nombre' in data:
            plan.nombre = data['nombre']
        if 'precio_mensual' in data:
            plan.precio_mensual = data['precio_mensual']
        if 'max_usuarios' in data:
            plan.max_usuarios = data['max_usuarios']
        if 'max_productos' in data:
            plan.max_productos = data['max_productos']
        if 'acceso_reportes_avanzados' in data:
            plan.acceso_reportes_avanzados = data['acceso_reportes_avanzados']
        if 'activo' in data:
            plan.activo = data['activo']
        
        db.session.commit()
        return {"message": "Plan actualizado", "plan": plan.to_dict()}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def eliminar_plan_service(id_plan):
    plan = Plan.query.get(id_plan)
    if not plan:
        return {"error": "Plan no encontrado"}, 404
    
    try:
        db.session.delete(plan)
        db.session.commit()
        return {"message": "Plan eliminado"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": "No se puede eliminar el plan (posiblemente en uso): " + str(e)}, 500

# ==========================================
# SUSCRIPCIONES (EMPRESA -> PLAN)
# ==========================================

def crear_suscripcion_service(data):
    try:
        if 'id_empresa' not in data or 'id_plan' not in data:
            return {"error": "id_empresa e id_plan son obligatorios"}, 400
        
        nuevo_id = data.get('id_suscripcion', str(uuid.uuid4()))
        
        f_inicio = None
        f_fin = None
        
        if data.get('fecha_inicio'):
            try:
                f_inicio = datetime.fromisoformat(str(data['fecha_inicio']).replace('Z', ''))
            except:
                pass
        
        if data.get('fecha_fin'):
            try:
                f_fin = datetime.fromisoformat(str(data['fecha_fin']).replace('Z', ''))
            except:
                pass
        
        suscripcion = Suscripcion(
            id_suscripcion=nuevo_id,
            id_empresa=data['id_empresa'],
            id_plan=data['id_plan'],
            fecha_inicio=f_inicio,
            fecha_fin=f_fin,
            estado=data.get('estado', True)
        )
        
        db.session.add(suscripcion)
        db.session.commit()
        return {"message": "Suscripción registrada", "suscripcion": suscripcion.to_dict()}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def obtener_suscripcion_por_empresa_service(id_empresa):
    subs = Suscripcion.query.filter_by(id_empresa=id_empresa).all()
    return [s.to_dict() for s in subs], 200

def obtener_todas_suscripciones_service():
    """Obtiene todas las suscripciones con información de empresa y plan"""
    suscripciones = Suscripcion.query.all()
    resultado = []
    
    for sub in suscripciones:
        sub_dict = sub.to_dict()
        
        # Agregar información de empresa
        empresa = Empresa.query.get(sub.id_empresa)
        if empresa:
            sub_dict['empresa'] = {
                'nombre_comercial': empresa.nombre_comercial,
                'razon_social': empresa.razon_social,
                'email': empresa.email
            }
        
        # Agregar información de plan
        plan = Plan.query.get(sub.id_plan)
        if plan:
            sub_dict['plan'] = {
                'nombre': plan.nombre,
                'precio_mensual': float(plan.precio_mensual) if plan.precio_mensual else 0
            }
        
        resultado.append(sub_dict)
    
    return resultado, 200

def actualizar_suscripcion_service(id_suscripcion, data):
    sub = Suscripcion.query.get(id_suscripcion)
    if not sub:
        return {"error": "Suscripción no encontrada"}, 404
    
    try:
        if 'id_plan' in data:
            sub.id_plan = data['id_plan']
        if 'estado' in data:
            sub.estado = data['estado']
        
        if 'fecha_inicio' in data and data['fecha_inicio']:
            sub.fecha_inicio = datetime.fromisoformat(str(data['fecha_inicio']).replace('Z', ''))
        
        if 'fecha_fin' in data and data['fecha_fin']:
            sub.fecha_fin = datetime.fromisoformat(str(data['fecha_fin']).replace('Z', ''))
        
        db.session.commit()
        return {"message": "Suscripción actualizada", "suscripcion": sub.to_dict()}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

# ==========================================
# ESTADÍSTICAS PARA DASHBOARD
# ==========================================

def obtener_estadisticas_dashboard_service():
    """Obtiene estadísticas generales para el dashboard del admin"""
    try:
        # Total de empresas
        total_empresas = Empresa.query.count()
        empresas_activas = Empresa.query.filter_by(activo=True).count()
        empresas_inactivas = total_empresas - empresas_activas
        
        # Suscripciones por plan
        suscripciones_free = Suscripcion.query.filter_by(id_plan='FREE', estado=True).count()
        suscripciones_basic = Suscripcion.query.filter_by(id_plan='BASIC', estado=True).count()
        suscripciones_premium = Suscripcion.query.filter_by(id_plan='PREMIUM', estado=True).count()
        
        # Ingresos mensuales (suma de planes activos)
        ingresos = 0
        suscripciones_activas = Suscripcion.query.filter_by(estado=True).all()
        for sub in suscripciones_activas:
            plan = Plan.query.get(sub.id_plan)
            if plan and plan.precio_mensual:
                ingresos += float(plan.precio_mensual)
        
        # Pagos pendientes (suscripciones con estado False)
        pagos_pendientes = Suscripcion.query.filter_by(estado=False).count()
        
        return {
            "empresas": {
                "total": total_empresas,
                "activas": empresas_activas,
                "inactivas": empresas_inactivas
            },
            "suscripciones": {
                "free": suscripciones_free,
                "basic": suscripciones_basic,
                "premium": suscripciones_premium
            },
            "ingresos": round(ingresos, 2),
            "pagosPendientes": pagos_pendientes
        }, 200
    except Exception as e:
        return {"error": str(e)}, 500

def obtener_empresas_recientes_service(limit=10):
    """Obtiene las empresas registradas más recientemente"""
    try:
        empresas = Empresa.query.order_by(Empresa.fecha_registro.desc()).limit(limit).all()
        resultado = []
        
        for empresa in empresas:
            empresa_dict = empresa.to_dict()
            
            # Obtener suscripción activa
            suscripcion = Suscripcion.query.filter_by(
                id_empresa=empresa.id_empresa,
                estado=True
            ).first()
            
            if suscripcion:
                plan = Plan.query.get(suscripcion.id_plan)
                empresa_dict['plan'] = plan.nombre if plan else 'N/A'
            else:
                empresa_dict['plan'] = 'Sin plan'
            
            resultado.append(empresa_dict)
        
        return resultado, 200
    except Exception as e:
        return {"error": str(e)}, 500

def obtener_pagos_pendientes_service():
    """Obtiene suscripciones pendientes de validación"""
    try:
        suscripciones = Suscripcion.query.filter_by(estado=False).all()
        resultado = []
        
        for sub in suscripciones:
            sub_dict = sub.to_dict()
            
            # Información de empresa
            empresa = Empresa.query.get(sub.id_empresa)
            if empresa:
                sub_dict['empresa_nombre'] = empresa.nombre_comercial
            
            # Información de plan
            plan = Plan.query.get(sub.id_plan)
            if plan:
                sub_dict['plan_nombre'] = plan.nombre
                sub_dict['monto'] = float(plan.precio_mensual) if plan.precio_mensual else 0
            
            resultado.append(sub_dict)
        
        return resultado, 200
    except Exception as e:
        return {"error": str(e)}, 500
    
# Agregar esta función al archivo saas_service.py existente

def obtener_empresas_con_propietarios_service():
    """Obtiene todas las empresas con información de su propietario"""
    try:
        from app.models.empresa import Empresa
        from app.models.seguridad import Usuario
        from app.models.saas import Suscripcion, Plan
        
        empresas = Empresa.query.all()
        resultado = []
        
        for empresa in empresas:
            empresa_dict = empresa.to_dict()
            
            # Buscar el propietario de la empresa
            propietario = Usuario.query.filter_by(
                id_empresa=empresa.id_empresa,
                id_rol='PROPIETARIO'
            ).first()
            
            if propietario:
                empresa_dict['propietario'] = {
                    'id': propietario.id_usuario,
                    'nombre_completo': f"{propietario.nombres} {propietario.apellido_paterno}".strip(),
                    'email': propietario.email,
                    'telefono': propietario.telefono,
                    'activo': propietario.activo
                }
            else:
                empresa_dict['propietario'] = None
            
            # Obtener suscripción activa
            suscripcion = Suscripcion.query.filter_by(
                id_empresa=empresa.id_empresa,
                estado=True
            ).first()
            
            if suscripcion:
                plan = Plan.query.get(suscripcion.id_plan)
                empresa_dict['plan_actual'] = {
                    'id_plan': suscripcion.id_plan,
                    'nombre': plan.nombre if plan else 'N/A',
                    'fecha_inicio': suscripcion.fecha_inicio.isoformat() if suscripcion.fecha_inicio else None,
                    'fecha_fin': suscripcion.fecha_fin.isoformat() if suscripcion.fecha_fin else None
                }
            else:
                empresa_dict['plan_actual'] = None
            
            # Contar usuarios de la empresa
            total_usuarios = Usuario.query.filter_by(id_empresa=empresa.id_empresa).count()
            usuarios_activos = Usuario.query.filter_by(id_empresa=empresa.id_empresa, activo=True).count()
            
            empresa_dict['estadisticas'] = {
                'total_usuarios': total_usuarios,
                'usuarios_activos': usuarios_activos
            }
            
            resultado.append(empresa_dict)
        
        return resultado, 200
    except Exception as e:
        return {"error": str(e)}, 500