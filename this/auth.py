from .db import get_db
from .metadata import metadata
from flask import request, session, render_template, flash, redirect, Blueprint, g
from sqlalchemy.sql import select, insert, update
from sqlalchemy.engine import Result
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import abort
import re
import functools

bp = Blueprint('auth', __name__, template_folder='templates', static_folder='static')

md = metadata()
table = md.tables['users']

@bp.before_app_request
def current_user():
    user_id = session.get('user_id')
    connection = get_db()
    
    if user_id is None:
        g.user = None
    else:
        statement = select(table).where(table.c.id == user_id)
        user = connection.execute(statement)
        user = Result.one(user)
        g.user = user

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect("/")
        return view(**kwargs)
    return wrapped_view

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None:
        return redirect('/')
    if request.method == 'POST':
        error = None
        connection = get_db()

        email = request.form['email']
        password = request.form['password']
        statement = (
            select(table).where(table.c.email == email)
        )
        user = connection.execute(statement)
        user = Result.fetchone(user)

        if user is None:
            error = 'Incorrect email address or password'
        elif not check_password_hash(user[2], password):
            error = 'Incorrect email address or password'
        if error is None:
            try:
                session.clear()
                session['user_id'] = user[0]

                return redirect("/")
            finally:
                connection.close()
        flash(error)
    return render_template('login.html')