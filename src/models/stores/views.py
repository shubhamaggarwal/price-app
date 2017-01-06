import json

from flask import Blueprint
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.utils import redirect

from src.models.stores.store import Store
import src.models.users.decorators as UserDecorators

store_blueprint = Blueprint('stores', __name__)


@store_blueprint.route('/')
def index():
    stores=Store.get_stores()
    return render_template('/stores/store_index.html',stores=stores)


@store_blueprint.route('/new', methods=['GET','POST'])
@UserDecorators.requires_admin
def create_store():
    if request.method=='POST':
        url_prefix=request.form['url_prefix']
        name=request.form['name']
        tag_name=request.form['tag_name']
        query=json.loads(request.form['query'])
        Store(name,url_prefix,tag_name,query).save_to_mongo()
        return redirect(url_for('.index'))
    return render_template('/stores/create_store.html')


@store_blueprint.route('/<string:store_id>')
def show_store(store_id):
    store=Store.get_store_by_id(store_id)
    return render_template('/stores/store.html',store=store)


@store_blueprint.route('/edit/<string:store_id>', methods=['GET','POST'])
@UserDecorators.requires_admin
def edit_store(store_id):
    print("dsa")
    if request.method=='POST':
        store=Store.get_store_by_id(store_id)
        store.name=request.form['name']
        store.tag_name = request.form['tag_name']
        store.query = request.form['query']
        store.url_prefix = request.form['url_prefix']
        store.save_to_mongo()
        return redirect(url_for('.index'))
    return render_template('/stores/edit_store.html',store=Store.get_store_by_id(store_id))


@store_blueprint.route('/delete/<string:store_id>')
@UserDecorators.requires_admin
def delete_store(store_id):
    store=Store.get_store_by_id(store_id)
    store.delete_store()
    return redirect(url_for('.index'))
