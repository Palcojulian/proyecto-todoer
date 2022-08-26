from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from todo.auth import login_required
from todo.db import get_db

bp = Blueprint('todo', __name__)

@bp.route('/')
@login_required #funcion decoradora que se encuentra dentro de auth.py, se encarga de proteger la funcion index
def index():
    db, c = get_db()
    c.execute(
        'select t.id, t.description, u.username, t.completed, t.created_at from todo t JOIN user u on t.create_by = u.id order by created_at desc'
    )

    todos = c.fetchall()

    return render_template('todo/index.html', todos = todos)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        description = request.form['description']
        error = None
        mensaje = ''

        if not description:
            error = 'Descripcion requerida'

        if error is not None:
            flash(error)
        else:
            db, c = get_db()

            c.execute(
                'insert into todo (description, completed, create_by)'
                'values(%s,%s,%s)',
                (description, False, g.user['id'])
            )
            db.commit()
            mensaje = 'Tarea creada con exito'
            flash(mensaje)
            return redirect(url_for('todo.index'))
        
    return render_template('todo/create.html')

@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    
    return render_template('todo/update.html', todo=todo)

@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    
    return ''