from flask import Blueprint,request,session,render_template,url_for

from src.models.users.user import User
from werkzeug.utils import redirect
import src.models.users.error as UserErrors
import src.models.users.decorators as UserDecorators


user_blueprint=Blueprint('users',__name__)


@user_blueprint.route('/login',methods=['GET', 'POST'])
def user_login():
    if session['email']!=None:
        return redirect(url_for('home'))
    if request.method == 'POST':
        email=request.form['email']
        password=request.form['password']
        try:
            if User.is_login_valid(email,password):
                session['email']=email
                return redirect(url_for('.user_alerts'))
        except UserErrors.UserError as error:
                return error.message
    return render_template('users/login.html')  #????send the user an error for wrong password


@user_blueprint.route('/register',methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        email=request.form['email']
        password=request.form['password']
        try:
            if User.register_user(email,password):
                session['email']=email
                return redirect(url_for('.user_alerts'))
        except UserErrors.UserError as error:
                return error.message

    return render_template('users/register.html')  #????send the user an error for wrong password


@user_blueprint.route('/logout')
@UserDecorators.requires_login
def user_logout():
    session['email']=None
    return redirect(url_for('home'))


@user_blueprint.route('/alerts')
@UserDecorators.requires_login
def user_alerts():
    user = User.get_by_email(session['email'])
    alerts = user.get_user_alerts()
    return render_template('users/alerts.html', alerts=alerts)


@user_blueprint.route('/check_alerts/<string:user_id>')
@UserDecorators.requires_login
def check_user_alerts(user_id):
    pass