from app.extensions import db
from app.models.seguridad import Rol, Usuario
from werkzeug.security import generate_password_hash, check_password_hash # Para encriptar
from flask_jwt_extended import create_access_token # Para generar token
from app.models.empresa import Empresa, ConfiguracionEmpresa
import uuid
from datetime import datetime

# ==================== CRUD ROL ====================

def crear_rol_service(data):
    try:
        # Generar ID si no viene
        nuevo_id = data.get('id_rol', str(uuid.uuid4()))
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

# === MODIFICADO: CREAR USUARIO CON HASH ===
def crear_usuario_service(data):
    try:
        # Validar obligatorios
        if not data.get('password'):
            return {"error": "La contraseña es obligatoria"}, 400

        nuevo_id = data.get('id_usuario', str(uuid.uuid4()))
        
        # ENCRIPTAR CONTRASEÑA
        pass_hash = generate_password_hash(data['password'])
        
        nuevo_usuario = Usuario(
            id_usuario=nuevo_id,
            id_empresa=data['id_empresa'],
            id_rol=data['id_rol'],
            nombre_completo=data.get('nombre_completo'),
            email=data.get('email'),
            password_hash=pass_hash, # GUARDAMOS EL HASH, NO EL TEXTO PLANO
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
    usuarios = Usuario.query.all()
    return [u.to_dict() for u in usuarios], 200

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
        if 'nombre_completo' in data: usuario.nombre_completo = data['nombre_completo']
        if 'email' in data: usuario.email = data['email']
        if 'id_rol' in data: usuario.id_rol = data['id_rol']
        if 'telefono' in data: usuario.telefono = data['telefono']
        if 'activo' in data: usuario.activo = data['activo']
        if 'password_hash' in data: usuario.password_hash = data['password_hash']
        
        db.session.commit()
        return {"message": "Usuario actualizado", "usuario": usuario.to_dict()}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def eliminar_usuario_service(id_usuario):
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
    
# === NUEVO: LOGIN ===
def login_usuario_service(data):
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return {"error": "Email y contraseña requeridos"}, 400
        
    usuario = Usuario.query.filter_by(email=email).first()
    
    # Verificar usuario y contraseña
    if usuario and check_password_hash(usuario.password_hash, password):
        if not usuario.activo:
            return {"error": "Usuario inactivo"}, 401
            
        # Crear Token con información extra (Claims)
        # Esto nos permite saber quién es sin consultar la BD a cada rato
        additional_claims = {
            "rol": usuario.id_rol, 
            "id_empresa": usuario.id_empresa
        }
        token = create_access_token(identity=usuario.id_usuario, additional_claims=additional_claims)
        
        # Actualizar último acceso
        usuario.ultimo_acceso = datetime.utcnow()
        db.session.commit()
        
        return {
            "message": "Login exitoso",
            "token": token,
            "usuario": {
                "nombre": usuario.nombre_completo,
                "rol": usuario.id_rol
            }
        }, 200
    
    return {"error": "Credenciales inválidas"}, 401

def registrar_empresa_y_dueno_service(data):
    """
    Crea la empresa, el usuario propietario y la configuración inicial en una sola transacción.
    Endpoint PÚBLICO.
    """
    try:
        # 1. Validaciones básicas
        if not data.get('nombre_empresa'): return {"error": "Falta nombre empresa"}, 400
        if not data.get('email'): return {"error": "Falta email"}, 400
        if not data.get('password'): return {"error": "Falta password"}, 400

        # Validar si el email ya existe
        if Usuario.query.filter_by(email=data['email']).first():
            return {"error": "El email ya está registrado"}, 400

        # 2. Generar IDs
        id_empresa_new = str(uuid.uuid4())
        id_usuario_new = str(uuid.uuid4())
        id_config_new = str(uuid.uuid4())

        # 3. Crear Objeto EMPRESA
        nueva_empresa = Empresa(
            id_empresa=id_empresa_new,
            nombre_comercial=data['nombre_empresa'],
            email=data['email'], # Email de contacto de la empresa
            activo=True
            # tenant_id se genera solo en BD o puedes generarlo aquí
        )

        # 4. Crear Objeto USUARIO (Propietario)
        pass_hash = generate_password_hash(data['password'])
        nuevo_usuario = Usuario(
            id_usuario=id_usuario_new,
            id_empresa=id_empresa_new,
            id_rol='PROPIETARIO', # <--- AQUÍ LE DAMOS EL PODER
            nombre_completo=data.get('nombre_completo', 'Administrador'),
            email=data['email'],
            password_hash=pass_hash,
            telefono=data.get('telefono'),
            activo=True
        )

        # 5. (Opcional) Crear CONFIGURACIÓN por defecto
        # Esto es muy útil para que no empiece con la configuración vacía
        nueva_config = ConfiguracionEmpresa(
            id_config=id_config_new,
            id_empresa=id_empresa_new,
            moneda_default='BOB', # O la que prefieras
            impuesto_iva=13.00,
            notif_stock_minimo=True
        )

        # 6. Guardar todo en una transacción
        db.session.add(nueva_empresa)
        db.session.add(nuevo_usuario)
        db.session.add(nueva_config)
        
        db.session.commit()

        # 7. (Opcional) Auto-Login: Devolver token inmediatamente
        # Para que no tenga que loguearse después de registrarse
        additional_claims = {"rol": "PROPIETARIO", "id_empresa": id_empresa_new}
        token = create_access_token(identity=id_usuario_new, additional_claims=additional_claims)

        return {
            "message": "Registro exitoso. ¡Bienvenido!",
            "token": token,
            "empresa": {"id": id_empresa_new, "nombre": nueva_empresa.nombre_comercial},
            "usuario": {"id": id_usuario_new, "nombre": nuevo_usuario.nombre_completo}
        }, 201

    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500