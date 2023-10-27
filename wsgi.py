#
# Aquest fitxer el busca automaticament la comanda flask run
#
from wannapop import create_app
from flask import Flask

create_app()

app = Flask(__name__)
app.config.from_pyfile("config.py")