from flask_sqlalchemy import SQLAlchemy

# Inicializamos la instancia de SQLAlchemy sin pasarle la "app" todavía.
# Se vinculará después en el __init__.py con db.init_app(app)
db = SQLAlchemy()