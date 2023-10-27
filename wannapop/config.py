import os
"""Flask App configuration."""

# General Config
SECRET_KEY = "Valor aleatori molt llarg i super secret"
basedir = os.path.abspath(os.path.dirname(__file__)) 
SQLALCHEMY_DATABASE_URI = "sqlite:///" + basedir + "/../database.db"
SQLALCHEMY_ECHO = True