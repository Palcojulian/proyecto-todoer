import functools
from flask import (
    Blueprint, flash, g, render_template, request, url_for, session, redirect
)

from werkzeug.security import check_password_hash, generate_password_hash

from todo.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET','POST']) #Vista de registrar
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db, c = get_db()
        error = None
        mensaje = ''
        c.execute(
            'select id from user where username = %s', (username,)
        )
        if not username:
            error = mensaje = 'Username es requerido'
        if not password:
            error = mensaje = 'Password es requerido'
        elif c.fetchone() is not None:
            error = mensaje = 'El usuario {} se encuentra registrado.'.format(username)
        
        if error is None:
            c.execute(
                'insert into user(username, password) values(%s,%s)',
                (username,generate_password_hash(password))
            )
            db.commit()
            mensaje = '¡Usuario creado con exito!'
        
        flash(mensaje)

        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST']) #Vista de iniciar sesión
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db, c = get_db()
        error = None

        c.execute(
            'select * from user where username = %s',(username,)
        )

        user = c.fetchone()

        if user is None:
            error = 'Usuario y/o contraseña invalido'
        elif not check_password_hash(user['password'], password):
            error = 'Usuario y/o contraseña invalido' 
        
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('todo.index'))
    
        if error != None:
            flash(error)

    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))



#Funcion decoradora, que se va encargar de colocar el usuario dentro de g
#verificar antes de cada peticion, si es que el usuario se encuentra, si se encuentra vamos a guardar el "id"
@bp.before_app_request
def load_logged_in_user(): #Funcion que se va encargar de cargar a nuestro usuario
    user_id = session.get('user_id')#Guarda el id con session.get, es de la sesion que se ha iniciado, de la linea 64. 

    if user_id is None: #Si no encuentra un usuario que no haya iniciado seseion, entonces se guarda None dentro de g.user
        g.user = None   #Ya que no encontro el usuario, por lo tanto no han iniciado sesión.
    else:
        db, c = get_db() #Si el usuario si inicio sesion, entonces llamanos el metodo que nos traer la conexion con la base de datos
        c.execute(
            'select * from user where id = %s', (user_id,)  #Traemos la información de la tabla "user"
        )
        g.user = c.fetchone()  #Nos devuelve el primer elemento que este encuentre



#Funcion que protege nuestras rutas
def login_required(view): #Funcion decoradora "view" -> funcion de la vista, que define nuestros endpoints
    @functools.wraps(view) #Envolver la función  con wraps
    def wrapped_view(**kwargs):
        if g.user is None:                          #Trae g.user de la linea 80, como es None, entonces lo redirecciona a la pagina para que inicie sesion
            return redirect(url_for('auth.login'))  #Con un usuario valido
        
        return view(**kwargs) # A la vista le pasamos todos los argumentos
    
    return wrapped_view