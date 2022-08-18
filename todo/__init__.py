import os
from flask import Flask

def create_app():
    app = Flask(__name__)

    app.config.from_mapping( #Metodo from_mapping, nos permitira definir variables de configuración 
        SECRET_KEY='mikey',  #Llave para definir, generar las sesiones en la aplicación, nombre tecnico 'cookie' 
        DATABASE_HOST= os.environ.get('FLASK_DATABASE_HOST'),
        DATABASE_PASSWORD= os.environ.get('FLASK_DATABASE_PASSWORD'),
        DATABASE_USER= os.environ.get('FLASK_DATABASE_USER'),
        DATABASE= os.environ.get('FLASK_DATABASE'),
    )

    @app.route('/hello')
    def hello():
        return 'Helloo!'

    return app