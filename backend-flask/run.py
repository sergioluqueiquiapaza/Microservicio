from app import create_app
from app.extensions import db

# Crea la instancia de la aplicación usando la fábrica que definimos en __init__.py
app = create_app()

if __name__ == '__main__':
    # Esto asegura que las tablas se creen en la BD si no existen
    # (Muy útil para desarrollo rápido antes de usar migraciones)
    with app.app_context():
        # Importamos los modelos para que SQLAlchemy sepa que existen antes de crear las tablas
        from app.models import empresa  # Asegúrate de importar tus modelos aquí
        db.create_all()
        print(">>> Base de datos conectada y tablas verificadas.")

    # Inicia el servidor de desarrollo
    # debug=True permite que el servidor se reinicie al guardar cambios en el código
    app.run(host='0.0.0.0', port=5000, debug=True)