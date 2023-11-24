# M12.A02-Projecte-1-Sprint-1


Proposta de solució de l'sprint 0 del projecte 1 dins del mòdul de projecte (M12) de 2n de DAW.


## Setup


### Python Virtual Environment


Crea l'entorn:


    python3 -m venv .venv


Activa'l:


    source .venv/bin/activate


Instal·la el requisits:


    pip install -r requirements.txt


Per a generar el fitxer de requiriments:


    pip freeze > requirements.txt


Per desactivar l'entorn:


    deactivate


### Instalar


pip install Flask-Login
pip install Python-dotenv
pip install email-validator
pip install flask-principal
pip install flask_wtf
pip install sqlalchemyseed
pip install sqlalchemy-seed

### Base de dades


La base de dades [SQLite](https://www.sqlite.org) s'ha de dir `database.db`. S'ha creat amb l'script [database.sql](./database.sql).


## Run des de terminal


Executa:


   flask run --debug


I obre un navegador a l'adreça: [http://127.0.0.1:5000](http://127.0.0.1:5000).


Aquesta comanda executa el codi de `wsgi.py`


## Debug amb Visual Code


Des de l'opció de `Run and Debug`, crea un fitxer anomenat `launch.json` amb el contingut següent:


```json
{
   "version": "0.2.0",
   "configurations": [
       {
           "name": "WANNAPOP",
           "type": "python",
           "request": "launch",
           "module": "flask",
           "env": {
               "FLASK_APP": "wsgi.py",
               "FLASK_DEBUG": "1"
           },
           "args": [
               "run",
               "--no-debugger",
               "--no-reload"
           ],
           "jinja": true,
           "justMyCode": true
       }
   ]
}
```

## Importar csv a la Base de dades des de DB Browser For SQLite Pas per Pas

1. Obrir DB Browser for SQLite: Inicia el programa al teu ordinador.

2. Obrir Base de Dades Existents o Crear-ne Una de Nova:

    2.a. Si ja tens una base de dades, fes clic a "File" > "Open Database... (ctrl + O)" i selecciona el teu arxiu .db. > fes clic a "Open".
    
    2.b. Si necessites crear una nova base de dades, fes clic a "File" > "New Database... (ctrl + N)", assigna-li un nom i desa-la en una ubicació.

3. Importar CSV:

    3.1. Fes clic a la pestanya "Database Structure".

    3.2. Després, fes clic a "File" > fes clic a "Import" > "Table from CSV file".

    3.3. Navega fins al fitxer CSV que vols importar i selecciona'l.

4. Configurar les Opcions d'Importació:

    4.1. Un cop seleccionat el fitxer CSV, se't presentarà una finestra amb diverses opcions.

    4.2. Assigna un nom a la nova taula.

    4.3. Configura les opcions com el delimitador de camps (comú en CSV és la coma o punt i coma), codificació de text, si la primera fila conté els noms de les columnes, etc.

    4.4. Revisa les opcions i ajusta-les segons les necessitats del teu fitxer CSV.

5. Previsualització i Ajustaments:

    5.1. DB Browser mostrarà una previsualització de com es veurà la taula.

    5.2. Pots fer ajustaments en la tipologia de dades de cada columna si és necessari (per exemple, canviar de TEXT a INTEGER).

6. Importar: Un cop estiguis satisfet amb la configuració i la previsualització, fes clic a "OK" o "Import" per començar el procés d'importació.

7. Guardar els Canvis: Després de la importació, no oblidis guardar els canvis a la base de dades. Pots fer-ho fent clic a "File" > "Write Changes".
