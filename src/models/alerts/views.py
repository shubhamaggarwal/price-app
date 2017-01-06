from flask import Blueprint,render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.utils import redirect
import src.models.users.decorators as UserDecorators

from src.models.alerts.alert import Alert

alert_blueprint=Blueprint('alerts',__name__)


@alert_blueprint.route('/new',methods=['GET','POST'])
@UserDecorators.requires_login
def create_alert():
    if request.method=='POST':

        name=request.form['name']
        price_limit=float(request.form['alert_limit'])
        url=request.form['url']

        item=Alert.convert_data_for_alert_to_item(name,url)

        alert=Alert(user_email=session['email'],item_id=item._id,price_limit=price_limit)
        alert.load_item_price()
        return redirect(url_for('users.user_alerts'))
    return render_template('/alerts/create_alert.html')


@alert_blueprint.route('/edit/<string:alert_id>',methods=['GET','POST'])
@UserDecorators.requires_login
def edit_alert(alert_id):
    if request.method=='POST':
        price_limit=float(request.form['alert_limit'])

        alert=Alert.get_by_id(alert_id)

        alert.price_limit=price_limit
        alert.active=True
        alert.load_item_price()
        return redirect(url_for('users.user_alerts'))
    return render_template('/alerts/edit_alert.html',alert=Alert.get_by_id(alert_id))



@alert_blueprint.route('/deactivate/<string:alert_id>')
@UserDecorators.requires_login
def deactivate_alert(alert_id):
    alert=Alert.get_by_id(alert_id)
    alert.deactivate()
    return redirect(url_for('users.user_alerts',alert_id=alert._id))


@alert_blueprint.route('/delete/<string:alert_id>')
@UserDecorators.requires_login
def delete_alert(alert_id):
    alert=Alert.get_by_id(alert_id)
    alert.delete()
    return redirect(url_for('users.user_alerts',alert_id=alert._id))


@alert_blueprint.route('/activate/<string:alert_id>')
@UserDecorators.requires_login
def activate_alert(alert_id):
    alert=Alert.get_by_id(alert_id)
    alert.activate()
    return redirect(url_for('users.user_alerts',alert_id=alert._id))


@alert_blueprint.route('/<string:alert_id>')
@UserDecorators.requires_login
def get_alert_page(alert_id):
    user_alert = Alert.get_by_id(alert_id)
    return render_template('alerts/alert.html',alert=user_alert)


@alert_blueprint.route('/check_alert_price/<string:alert_id>')
@UserDecorators.requires_login
def check_alert_price(alert_id):
    alert=Alert.get_by_id(alert_id)
    alert.load_item_price()
    return redirect(url_for('.get_alert_page',alert_id=alert_id))


