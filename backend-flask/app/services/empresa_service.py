from app.extensions import db
# IMPORTANTE: Ya no importamos PlanSuscripcion aquí porque se movió al módulo SaaS
from app.models.empresa import Empresa, ConfiguracionEmpresa
import uuid

# ==========================================
#               EMPRESA (CRUD)
# ==========================================

def crear_empresa_service(data):
    try:
        if 'id_empresa' not in data:
            return {"error": "El campo 'id_empresa' es obligatorio"}, 400

        # Validar si ya existe
        if Empresa.query.get(data['id_empresa']):
             return {"error": "Ya existe una empresa con ese ID"}, 400

        nueva_empresa = Empresa(
            id_empresa=data['id_empresa'],
            # tenant_id se genera automáticamente en el modelo/BD
            nombre_comercial=data.get('nombre_comercial'),
            razon_social=data.get('razon_social'),
            nit_ruc=data.get('nit_ruc'),
            telefono=data.get('telefono'),
            email=data.get('email'),
            direccion=data.get('direccion'),
            logo_url=data.get('logo_url'),
            horario_atencion=data.get('horario_atencion'),
            activo=data.get('activo', True)
        )
        
        # Opcional: Crear configuración por defecto automáticamente al crear empresa
        config_default = ConfiguracionEmpresa(
            id_config=str(uuid.uuid4()),
            id_empresa=nueva_empresa.id_empresa,
            moneda_default='BOB',
            impuesto_iva=13.00,
            formato_factura='carta',
            notif_stock_minimo=True,
            notif_ventas=True,
            zona_horaria='America/La_Paz'
        )
        
        db.session.add(nueva_empresa)
        db.session.add(config_default) # Guardamos también la config
        db.session.commit()
        
        return {"message": "Empresa creada exitosamente", "empresa": nueva_empresa.to_dict()}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def obtener_empresas_service():
    empresas = Empresa.query.all()
    return [e.to_dict() for e in empresas], 200

def obtener_empresa_por_id_service(id_empresa):
    empresa = Empresa.query.get(id_empresa)
    if not empresa:
        return {"error": "Empresa no encontrada"}, 404
    return empresa.to_dict(), 200

def actualizar_empresa_service(id_empresa, data):
    empresa = Empresa.query.get(id_empresa)
    if not empresa:
        return {"error": "Empresa no encontrada"}, 404
    
    try:
        if 'nombre_comercial' in data: empresa.nombre_comercial = data['nombre_comercial']
        if 'razon_social' in data: empresa.razon_social = data['razon_social']
        if 'nit_ruc' in data: empresa.nit_ruc = data['nit_ruc']
        if 'telefono' in data: empresa.telefono = data['telefono']
        if 'email' in data: empresa.email = data['email']
        if 'direccion' in data: empresa.direccion = data['direccion']
        if 'logo_url' in data: empresa.logo_url = data['logo_url']
        if 'horario_atencion' in data: empresa.horario_atencion = data['horario_atencion']
        if 'activo' in data: empresa.activo = data['activo']
        
        db.session.commit()
        return {"message": "Empresa actualizada correctamente", "empresa": empresa.to_dict()}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def eliminar_empresa_service(id_empresa):
    empresa = Empresa.query.get(id_empresa)
    if not empresa:
        return {"error": "Empresa no encontrada"}, 404
    
    try:
        # Al borrar la empresa, el CASCADE de la base de datos borrará TODO lo demás (Usuarios, Productos, Config, etc.)
        db.session.delete(empresa)
        db.session.commit()
        return {"message": "Empresa y todos sus datos asociados eliminados correctamente"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": "Error al eliminar: " + str(e)}, 500

# ==========================================
#        CONFIGURACION EMPRESA (CRUD)
# ==========================================

def crear_config_service(data):
    try:
        if 'id_empresa' not in data:
             return {"error": "Falta id_empresa"}, 400

        nuevo_id = data.get('id_config', str(uuid.uuid4()))
        nueva_config = ConfiguracionEmpresa(
            id_config=nuevo_id,
            id_empresa=data['id_empresa'],
            moneda_default=data.get('moneda_default', 'BOB'),
            impuesto_iva=data.get('impuesto_iva', 13.00),
            formato_factura=data.get('formato_factura', 'carta'),
            notif_stock_minimo=data.get('notif_stock_minimo', True),
            notif_ventas=data.get('notif_ventas', True),
            zona_horaria=data.get('zona_horaria', 'America/La_Paz')
        )
        db.session.add(nueva_config)
        db.session.commit()
        return {"message": "Configuración creada", "configuracion": nueva_config.to_dict()}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def obtener_configs_service():
    configs = ConfiguracionEmpresa.query.all()
    return [c.to_dict() for c in configs], 200

def obtener_config_por_id_service(id_config):
    config = ConfiguracionEmpresa.query.get(id_config)
    if not config:
        return {"error": "Configuración no encontrada"}, 404
    return config.to_dict(), 200

def actualizar_config_service(id_config, data):
    config = ConfiguracionEmpresa.query.get(id_config)
    if not config:
        return {"error": "Configuración no encontrada"}, 404
    
    try:
        if 'moneda_default' in data: config.moneda_default = data['moneda_default']
        if 'impuesto_iva' in data: config.impuesto_iva = data['impuesto_iva']
        if 'formato_factura' in data: config.formato_factura = data['formato_factura']
        if 'notif_stock_minimo' in data: config.notif_stock_minimo = data['notif_stock_minimo']
        if 'notif_ventas' in data: config.notif_ventas = data['notif_ventas']
        if 'zona_horaria' in data: config.zona_horaria = data['zona_horaria']
        
        db.session.commit()
        return {"message": "Configuración actualizada", "configuracion": config.to_dict()}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def eliminar_config_service(id_config):
    config = ConfiguracionEmpresa.query.get(id_config)
    if not config:
        return {"error": "Configuración no encontrada"}, 404
    try:
        db.session.delete(config)
        db.session.commit()
        return {"message": "Configuración eliminada"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500