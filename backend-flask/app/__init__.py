from flask import Flask
from flask_cors import CORS  # ← IMPORTAR CORS
from app.extensions import db
import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from app.models.token_blocklist import TokenBlocklist

# Cargar variables de entorno del archivo .env
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # ============================================
    # CONFIGURACIÓN CORS (CRÍTICO PARA REACT)
    # ============================================
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:5173", "http://localhost:3000"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    
    # Obtener la URL del .env.
    uri = os.getenv('DATABASE_URI')
    
    if not uri:
        print("⚠️ ADVERTENCIA: No se leyó DATABASE_URI del .env, revisa la carga de variables.")
    
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # --- CONFIGURACIÓN JWT ---
    app.config["JWT_SECRET_KEY"] = "clave-super-secreta-cambiala-en-produccion"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600 * 24  # Token dura 24 horas
    
    db.init_app(app)
    jwt = JWTManager(app)
    
    # Callback para verificar si un token está en la lista de bloqueo
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
        return token is not None
    
    # --- REGISTRO DE BLUEPRINTS ---
    from app.routes.empresa_routes import empresa_bp
    from app.routes.seguridad_routes import seguridad_bp
    from app.routes.inventario_routes import inventario_bp
    from app.routes.ventas_routes import ventas_bp
    from app.routes.compras_routes import compras_bp
    from app.routes.soporte_routes import soporte_bp
    from app.routes.saas_routes import saas_bp
    
    app.register_blueprint(empresa_bp, url_prefix='/api')
    app.register_blueprint(seguridad_bp, url_prefix='/api')
    app.register_blueprint(inventario_bp, url_prefix='/api')
    app.register_blueprint(ventas_bp, url_prefix='/api')
    app.register_blueprint(compras_bp, url_prefix='/api')
    app.register_blueprint(soporte_bp, url_prefix='/api')
    app.register_blueprint(saas_bp, url_prefix='/api')
    
    print("✅ Flask app inicializada correctamente con CORS habilitado")
    
    return app