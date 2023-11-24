# my_app/seeders/categories-seeder.py

from sqlalchemy_seed import load_fixture_files, load_fixtures
from my_app import db_manager

# Accede a la instancia de la base de datos a través de db_manager
db = db_manager.db

# Define la ubicación de los archivos de fixtures
fixtures = load_fixture_files('seeders', ['categories.json'])

# Obtén la sesión de la base de datos desde db_manager
db_session = db_manager.session

# Carga las fixtures en la base de datos
load_fixtures(db_session, fixtures)
