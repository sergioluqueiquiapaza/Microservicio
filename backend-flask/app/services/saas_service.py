from app.extensions import db
from app.models.saas import AdminSaas, Plan, Suscripcion
from app.models.token_blocklist import TokenBlocklist
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, get_jwt
import uuid
from datetime import datetime

# ==========================================
#        ADMINISTRADORES SAAS (CRUD & AUTH)
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
            # id_admin se genera automático por el modelo (default=uuid.uuid4)
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
        
        # Token con claim especial para diferenciar de usuarios normales
        additional_claims = {"rol": "SUPER_ADMIN", "tipo": "SAAS"}
        # Convertimos el UUID a string para el token
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
    """
    Cierra la sesión del Administrador SaaS.
    Podríamos agregar logs de auditoría aquí en el futuro.
    """
    try:
        # 1. Obtener el identificador único del token (JTI)
        jti = get_jwt()["jti"]
        
        # 2. Guardarlo en la Blocklist
        revoked_token = TokenBlocklist(jti=jti)
        db.session.add(revoked_token)
        db.session.commit()
        
        return {"message": "Admin SaaS: Sesión cerrada correctamente"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": "Error al cerrar sesión: " + str(e)}, 500

def obtener_admins_saas_service():
    admins = AdminSaas.query.all()
    return [a.to_dict() for a in admins], 200

# ==========================================
#            PLANES (CATÁLOGO)
# ==========================================

def crear_plan_service(data):
    try:
        if 'id_plan' not in data:
            return {"error": "El id_plan (código único) es obligatorio"}, 400

        # Verificar si el código de plan ya existe
        if Plan.query.get(data['id_plan']):
            return {"error": "Ya existe un plan con ese ID"}, 400

        nuevo_plan = Plan(
            id_plan=data['id_plan'],
            id_admin=data.get('id_admin'), # UUID del admin que lo crea (puede ser null)
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
    # Retorna todos los planes (puedes filtrar por activos si prefieres)
    planes = Plan.query.all()
    return [p.to_dict() for p in planes], 200

def obtener_plan_id_service(id_plan):
    plan = Plan.query.get(id_plan)
    return (plan.to_dict(), 200) if plan else ({"error": "Plan no encontrado"}, 404)

def actualizar_plan_service(id_plan, data):
    plan = Plan.query.get(id_plan)
    if not plan: return {"error": "Plan no encontrado"}, 404

    try:
        if 'nombre' in data: plan.nombre = data['nombre']
        if 'precio_mensual' in data: plan.precio_mensual = data['precio_mensual']
        if 'max_usuarios' in data: plan.max_usuarios = data['max_usuarios']
        if 'max_productos' in data: plan.max_productos = data['max_productos']
        if 'acceso_reportes_avanzados' in data: plan.acceso_reportes_avanzados = data['acceso_reportes_avanzados']
        if 'activo' in data: plan.activo = data['activo']
        
        db.session.commit()
        return {"message": "Plan actualizado", "plan": plan.to_dict()}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def eliminar_plan_service(id_plan):
    plan = Plan.query.get(id_plan)
    if not plan: return {"error": "Plan no encontrado"}, 404
    try:
        # Nota: Si hay suscripciones activas vinculadas, esto podría fallar 
        # a menos que la BD tenga CASCADE, pero configuramos SET NULL o RESTRICT.
        db.session.delete(plan)
        db.session.commit()
        return {"message": "Plan eliminado"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": "No se puede eliminar el plan (posiblemente en uso): " + str(e)}, 500

# ==========================================
#          SUSCRIPCIONES (EMPRESA -> PLAN)
# ==========================================

def crear_suscripcion_service(data):
    try:
        if 'id_empresa' not in data or 'id_plan' not in data:
            return {"error": "id_empresa e id_plan son obligatorios"}, 400

        nuevo_id = data.get('id_suscripcion', str(uuid.uuid4()))

        # Manejo de Fechas (Strings ISO a Objetos Datetime)
        f_inicio = None
        f_fin = None
        
        if data.get('fecha_inicio'):
            try:
                # Intenta parsear "2023-01-01" o ISO completo
                f_inicio = datetime.fromisoformat(str(data['fecha_inicio']).replace('Z', ''))
            except:
                pass # Si falla, queda None o puedes lanzar error

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
    # Obtener el historial o la suscripción activa
    subs = Suscripcion.query.filter_by(id_empresa=id_empresa).all()
    return [s.to_dict() for s in subs], 200

def actualizar_suscripcion_service(id_suscripcion, data):
    sub = Suscripcion.query.get(id_suscripcion)
    if not sub: return {"error": "Suscripción no encontrada"}, 404

    try:
        if 'id_plan' in data: sub.id_plan = data['id_plan']
        if 'estado' in data: sub.estado = data['estado']
        
        # Actualizar fechas si vienen
        if 'fecha_inicio' in data and data['fecha_inicio']:
            sub.fecha_inicio = datetime.fromisoformat(str(data['fecha_inicio']).replace('Z', ''))
            
        if 'fecha_fin' in data and data['fecha_fin']:
            sub.fecha_fin = datetime.fromisoformat(str(data['fecha_fin']).replace('Z', ''))

        db.session.commit()
        return {"message": "Suscripción actualizada", "suscripcion": sub.to_dict()}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500