from functools import wraps

from flask import request
from flask import session,url_for
from werkzeug.utils import redirect
from src.app import app

def requires_login(fnc):
    @wraps(fnc)
    def must_login(*args,**kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('users.user_login',next=request.path))
        return fnc(*args,**kwargs)
    return must_login


def requires_admin(fnc):
    @wraps(fnc)
    def admin(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('users.user_login'))
        if session['email'] not in app.config['ADMINS']:
            session['email']=None
            return redirect(url_for('users.user_login'))
        return fnc(*args,**kwargs)
    return admin
