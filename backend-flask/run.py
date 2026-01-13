from app import create_app
from app.extensions import db

# Crea la instancia de la aplicación usando la fábrica que definimos en __init__.py
app = create_app()

if __name__ == '__main__':
    # Esto asegura que las tablas se creen en la BD si no existen
    with app.app_context():
        # --- IMPORTANTE: Importar TODOS los modelos aquí ---
        # Si no los importas, SQLAlchemy no sabrá que existen y no creará las tablas.
        
        from app.models import saas        # <--- ¡CRÍTICO! Para las tablas nuevas
        from app.models import empresa     # Configuración y Empresa
        from app.models import seguridad   # Usuarios y Roles
        from app.models import inventario  # Productos, Proveedores, Categorías
        from app.models import ventas      # Clientes, Ventas, Pagos
        from app.models import compras     # Compras
        from app.models import soporte     # Notificaciones, Auditoría

        # Crea todas las tablas definidas en los modelos importados
        db.create_all()
        print(">>> Base de datos conectada. Tablas verificadas y creadas exitosamente.")

    # Inicia el servidor de desarrollo
    app.run(host='0.0.0.0', port=5000, debug=True)