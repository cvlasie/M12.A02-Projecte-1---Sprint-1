from sqlalchemy_seed import load_fixture_files, load_fixtures
from yourapp import db  # Importa la instància de SQLAlchemy de la teva aplicació
from yourapp.models import Status  # Importa el model Status

# Defineix la ubicació dels fitxers de fixtures
fixtures = load_fixture_files('seeders', ['statuses.json'])

# Carrega les fixtures a la base de dades
load_fixtures(db.session, fixtures)

# Si necessites controlar la transacció manualment, pots utilitzar:
# with db.session.begin_nested():
#     load_fixtures(db.session, fixtures)
# db.session.commit()
