# API Estação Meteorológica Python
## Instalação
https://www.python.org/
## Documentação
https://docs.python.org/3/
## IDE
https://code.visualstudio.com/docs/languages/python
## Instalar plugin Python
https://editorconfig.org/
## Virtual Environment
https://docs.python.org/3/library/venv.html?highlight=venv#module-venv

C:\<pasta do projeto>> python -m venv venv

C:\<pasta do projeto>> venv\Scripts\activate

C:\<pasta do projeto>> deactivate
## Módulos
https://pypi.org/project/pip/

C:\> pip install flask

C:\> pip install fontawesome

C:\> pip install flask-bootstrap


## Flask
https://flask.palletsprojects.com/en/1.1.x/
### LINUX
> FLASK_APP=app.py

> FLASK_ENV=development 	 
### WINDOWS
> $env:FLASK_APP = ‘app.py’

> $env:FLASK_ENV = ‘development’

## API REST endpoints
LIST get /api/v1.0/
GET get /api/v1.0/id
CREATE post /api/v1.0
UPDATE post /api/v1.0/id
DELETE post /api/v1.0/id/del
>>>>>> Atualizar endpoints!!!

## Flask-RESTful
https://flask-restful.readthedocs.io/en/latest/
Jinja2 Templates

https://palletsprojects.com/p/jinja/

## SQLAlchemy ORM
https://flask-sqlalchemy.palletsprojects.com/en/2.x/
3 barras significam path relativo, 4 path absoluto:
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
### Usar chave/valor para instanciar o modelo:
admin = User(username='admin', email='admin@example.com')
Só aceita os verbos GET e POST.
### Para inicializar o banco de dados:
Abrir sessão interativa do python
from app import db
db.create_all()
Na documentação oficial tem a informação sobre os modelos de relacionamento. Aqui a gente usou um para muitos.

## Application Factory
Modularização por extensões
Agrupamento de views por Blueprints

## Implementação de MVC
Imports absolutos e relativos
Circular imports

## API testes
Postman
Autenticação
https://pythonhosted.org/Flask-JWT/
https://blog.tecladocode.com/simple-jwt-authentication-with-flask-jwt/
https://learning.postman.com/docs/sending-requests/authorization/#bearer-token

## Criptografia
https://pythonprogramming.net/password-hashing-flask-tutorial/

## Visualização
https://seaborn.pydata.org/examples/index.html
https://www.highcharts.com/
https://www.openstreetmap.org/#map=11/-23.5401/-45.2450
https://leafletjs.com/
https://www.mapbox.com/
