from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
    """Base config."""
    SECRETKEY = environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + basedir + "/" + environ.get('SQLITE_FILE_RELATIVE_PATH')    