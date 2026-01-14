from app.extensions import db
from app.models.seguridad import Rol, Usuario
from app.models.empresa import Empresa, ConfiguracionEmpresa
from app.models.saas import Suscripcion
from app.models.token_blocklist import TokenBlocklist
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, get_jwt
from datetime import datetime
import uuid

# ==================== CRUD ROL ====================
def crear_rol_service(data):
    try:
        nuevo_id = data.get('id_rol', str(uuid.uuid4()))
        
        if Rol.query.get(nuevo_id):
            return {"error": f"El rol {nuevo_id} ya existe"}, 400
        
        nuevo_rol = Rol(
            id_rol=nuevo_id,
            nombre=data.get('nombre'),
            permisos_json=data.get('permisos_json', {}),
            descripcion=data.get('descripcion')
        )
        db.session.add(nuevo_rol)
        db.session.commit()
        return {"message": "Rol creado exitosamente", "rol": nuevo_rol.to_dict()}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def obtener_roles_service():
    roles = Rol.query.all()
    return [r.to_dict() for r in roles], 200

def obtener_rol_por_id_service(id_rol):
    rol = Rol.query.get(id_rol)
    if not rol:
        return {"error": "Rol no encontrado"}, 404
    return rol.to_dict(), 200

def actualizar_rol_service(id_rol, data):
    rol = Rol.query.get(id_rol)
    if not rol:
        return {"error": "Rol no encontrado"}, 404
    try:
        if 'nombre' in data: rol.nombre = data['nombre']
        if 'permisos_json' in data: rol.permisos_json = data['permisos_json']
        if 'descripcion' in data: rol.descripcion = data['descripcion']
        
        db.session.commit()
        return {"message": "Rol actualizado", "rol": rol.to_dict()}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def eliminar_rol_service(id_rol):
    rol = Rol.query.get(id_rol)
    if not rol:
        return {"error": "Rol no encontrado"}, 404
    try:
        db.session.delete(rol)
        db.session.commit()
        return {"message": "Rol eliminado correctamente"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": "Error al eliminar (posiblemente esté asignado a usuarios): " + str(e)}, 500

# ==================== CRUD USUARIO ====================
def crear_usuario_service(data):
    try:
        if not data.get('password'):
            return {"error": "La contraseña es obligatoria"}, 400
        if not data.get('email'):
            return {"error": "El email es obligatorio"}, 400
        
        if Usuario.query.filter_by(email=data['email']).first():
            return {"error": "El email ya está registrado"}, 400
        
        nuevo_id = data.get('id_usuario', str(uuid.uuid4()))
        pass_hash = generate_password_hash(data['password'])
        
        nuevo_usuario = Usuario(
            id_usuario=nuevo_id,
            id_empresa=data['id_empresa'],
            id_rol=data['id_rol'],
            nombres=data.get('nombres'),
            apellido_paterno=data.get('apellido_paterno'),
            apellido_materno=data.get('apellido_materno'),
            email=data.get('email'),
            password_hash=pass_hash,
            telefono=data.get('telefono'),
            activo=True
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        return {"message": "Usuario registrado", "usuario": nuevo_usuario.to_dict()}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def obtener_usuarios_service():
    """Obtiene usuarios ACTIVOS filtrados por empresa del token JWT"""
    try:
        claims = get_jwt()
        id_empresa = claims.get('id_empresa')
        
        # Si es SUPER_ADMIN, mostrar todos los usuarios
        if claims.get('rol') == 'SUPER_ADMIN':
            usuarios = Usuario.query.filter_by(activo=True).all()
        else:
            # Filtrar por empresa y solo activos
            usuarios = Usuario.query.filter_by(id_empresa=id_empresa, activo=True).all()
        
        return [u.to_dict() for u in usuarios], 200
    except Exception as e:
        return {"error": str(e)}, 500

def obtener_usuarios_inactivos_service():
    """Obtiene usuarios INACTIVOS filtrados por empresa del token JWT"""
    try:
        claims = get_jwt()
        id_empresa = claims.get('id_empresa')
        
        # Si es SUPER_ADMIN, mostrar todos los usuarios inactivos
        if claims.get('rol') == 'SUPER_ADMIN':
            usuarios = Usuario.query.filter_by(activo=False).all()
        else:
            # Filtrar por empresa y solo inactivos
            usuarios = Usuario.query.filter_by(id_empresa=id_empresa, activo=False).all()
        
        return [u.to_dict() for u in usuarios], 200
    except Exception as e:
        return {"error": str(e)}, 500

def obtener_usuario_por_id_service(id_usuario):
    usuario = Usuario.query.get(id_usuario)
    if not usuario:
        return {"error": "Usuario no encontrado"}, 404
    return usuario.to_dict(), 200

def actualizar_usuario_service(id_usuario, data):
    usuario = Usuario.query.get(id_usuario)
    if not usuario:
        return {"error": "Usuario no encontrado"}, 404
    try:
        if 'nombres' in data: usuario.nombres = data['nombres']
        if 'apellido_paterno' in data: usuario.apellido_paterno = data['apellido_paterno']
        if 'apellido_materno' in data: usuario.apellido_materno = data['apellido_materno']
        
        if 'email' in data: usuario.email = data['email']
        if 'id_rol' in data: usuario.id_rol = data['id_rol']
        if 'telefono' in data: usuario.telefono = data['telefono']
        if 'activo' in data: usuario.activo = data['activo']
        
        if 'password' in data and data['password']:
            usuario.password_hash = generate_password_hash(data['password'])
        
        db.session.commit()
        return {"message": "Usuario actualizado", "usuario": usuario.to_dict()}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def desactivar_usuario_service(id_usuario):
    """Desactiva un usuario (eliminación lógica)"""
    usuario = Usuario.query.get(id_usuario)
    if not usuario:
        return {"error": "Usuario no encontrado"}, 404
    
    # Validar que no sea el propietario
    if usuario.id_rol == 'PROPIETARIO':
        return {"error": "No se puede desactivar al propietario de la empresa"}, 400
    
    try:
        usuario.activo = False
        db.session.commit()
        return {"message": "Usuario desactivado correctamente"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def activar_usuario_service(id_usuario):
    """Reactiva un usuario desactivado"""
    usuario = Usuario.query.get(id_usuario)
    if not usuario:
        return {"error": "Usuario no encontrado"}, 404
    
    try:
        usuario.activo = True
        db.session.commit()
        return {"message": "Usuario activado correctamente"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def eliminar_usuario_service(id_usuario):
    """Eliminación física del usuario (solo SUPER_ADMIN)"""
    usuario = Usuario.query.get(id_usuario)
    if not usuario:
        return {"error": "Usuario no encontrado"}, 404
    try:
        db.session.delete(usuario)
        db.session.commit()
        return {"message": "Usuario eliminado correctamente"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

# ==================== LOGIN Y AUTH ====================
def login_usuario_service(data):
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return {"error": "Email y contraseña requeridos"}, 400
    
    usuario = Usuario.query.filter_by(email=email).first()
    
    if usuario and check_password_hash(usuario.password_hash, password):
        if not usuario.activo:
            return {"error": "Usuario inactivo. Contacte al administrador."}, 401
        
        additional_claims = {
            "rol": usuario.id_rol,
            "id_empresa": usuario.id_empresa
        }
        token = create_access_token(identity=usuario.id_usuario, additional_claims=additional_claims)
        
        usuario.ultimo_acceso = datetime.utcnow()
        db.session.commit()
        
        nombre_visual = f"{usuario.nombres} {usuario.apellido_paterno}".strip()
        
        return {
            "message": "Login exitoso",
            "token": token,
            "usuario": {
                "id_usuario": usuario.id_usuario,
                "nombres": usuario.nombres,
                "apellido_paterno": usuario.apellido_paterno,
                "apellido_materno": usuario.apellido_materno,
                "nombre_completo_str": nombre_visual,
                "email": usuario.email,
                "rol": usuario.id_rol,
                "id_empresa": usuario.id_empresa
            }
        }, 200
    
    return {"error": "Credenciales inválidas"}, 401

def logout_service():
    try:
        jti = get_jwt()["jti"]
        revoked_token = TokenBlocklist(jti=jti)
        db.session.add(revoked_token)
        db.session.commit()
        
        return {"message": "Sesión cerrada exitosamente. Token invalidado."}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def registrar_empresa_y_dueno_service(data):
    """
    Endpoint PÚBLICO para el registro de nuevas cuentas.
    Crea: Empresa + Configuración + Usuario Propietario + Suscripción FREE
    """
    try:
        # 1. Validaciones
        if not data.get('nombre_empresa'):
            return {"error": "Falta nombre empresa"}, 400
        if not data.get('email'):
            return {"error": "Falta email"}, 400
        if not data.get('password'):
            return {"error": "Falta password"}, 400
        if not data.get('nombres'):
            return {"error": "Falta nombres"}, 400
        if not data.get('paterno'):
            return {"error": "Falta apellido paterno"}, 400
        
        # Verificar email único
        if Usuario.query.filter_by(email=data['email']).first():
            return {"error": "El email ya está registrado"}, 400
        
        # 2. Generar IDs
        id_empresa_new = str(uuid.uuid4())
        id_usuario_new = str(uuid.uuid4())
        id_config_new = str(uuid.uuid4())
        id_suscripcion_new = str(uuid.uuid4())
        
        # 3. Crear EMPRESA
        nueva_empresa = Empresa(
            id_empresa=id_empresa_new,
            nombre_comercial=data['nombre_empresa'],
            email=data['email'],
            activo=True
        )
        
        # 4. Crear CONFIGURACIÓN POR DEFECTO
        nueva_config = ConfiguracionEmpresa(
            id_config=id_config_new,
            id_empresa=id_empresa_new,
            moneda_default='BOB',
            impuesto_iva=13.00,
            notif_stock_minimo=True,
            notif_ventas=True,
            zona_horaria='America/La_Paz'
        )
        
        # 5. Crear USUARIO DUEÑO
        rol_inicial = 'PROPIETARIO'
        pass_hash = generate_password_hash(data['password'])
        
        nuevo_usuario = Usuario(
            id_usuario=id_usuario_new,
            id_empresa=id_empresa_new,
            id_rol=rol_inicial,
            nombres=data.get('nombres'),
            apellido_paterno=data.get('paterno'),
            apellido_materno=data.get('materno', ''),
            email=data['email'],
            password_hash=pass_hash,
            telefono=data.get('telefono'),
            activo=True
        )
        
        # 6. Crear SUSCRIPCIÓN FREE por defecto
        nueva_suscripcion = Suscripcion(
            id_suscripcion=id_suscripcion_new,
            id_empresa=id_empresa_new,
            id_plan='FREE',
            fecha_inicio=datetime.utcnow(),
            fecha_fin=None,
            estado=True
        )
        
        # 7. Guardar todo en una transacción
        db.session.add(nueva_empresa)
        db.session.add(nueva_config)
        db.session.add(nuevo_usuario)
        db.session.add(nueva_suscripcion)
        
        db.session.commit()
        
        # 8. Auto-Login
        additional_claims = {"rol": rol_inicial, "id_empresa": id_empresa_new}
        token = create_access_token(identity=id_usuario_new, additional_claims=additional_claims)
        
        return {
            "message": "Registro exitoso. ¡Bienvenido!",
            "token": token,
            "empresa": {
                "id": id_empresa_new,
                "nombre": nueva_empresa.nombre_comercial
            },
            "usuario": {
                "id": id_usuario_new,
                "nombre": f"{nuevo_usuario.nombres} {nuevo_usuario.apellido_paterno}",
                "rol": rol_inicial,
                "id_empresa": id_empresa_new
            },
            "suscripcion": {
                "id": id_suscripcion_new,
                "plan": "FREE"
            }
        }, 201
    except Exception as e:
        db.session.rollback()
        return {"error": "Error en el registro: " + str(e)}, 500