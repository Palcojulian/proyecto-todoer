
import mysql.connector

import click
# click -> nos permite para ejecutar comandos en la terminal

from flask import current_app, g 
# current_app -> matiene la aplicacion que estamos ejecutando 
# g -> variable, le podemos asignar variables para utilizarlas en otra parte de la aplicación
# en este caso se va utilizar para almacenar el 'usuario' dentro de 'g'

from flask.cli import with_appcontext
# trae el contexto de la configuracion de la aplicación 

from .schema import instructions #va contener todas las scrips de la base de datos

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host=current_app.config['DATABASE_HOST'],
            user=current_app.config['DATABASE_USER'],
            password=current_app.config['DATABASE_PASSWORD'],
            database=current_app.config['DATABASE']
        )
        g.c = g.db.cursor(dictionary=True)

    return g.db, g.c

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db, c = get_db()

    for i in instructions:
        c.execute(i)
    
    db.commit()

@click.command('init-db') #Para llamardo desde de la terminal, para ejecutar esta funcion
@with_appcontext          #Para que la funcion puedan acceder a las variables de configuración
def init_db_command():
    init_db()
    click.echo('Base de datos inicializada')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)