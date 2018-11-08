#!/usr/bin/env python3

### Imports ###
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from itemdb import Base, Categories, Items, User
from flask import session as login_session
import random
import string
import json
from flask import make_response, Blueprint
import requests
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from wtforms import Form, TextField, PasswordField, validators
from google.oauth2 import id_token
from google.auth.transport import requests
import os
from flask_dance.contrib.google import make_google_blueprint, google


### DB Setup ###
engine = create_engine('postgresql://catalog:catalog@localhost/catalog')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('/var/www/html/server/itemCatalog/client_secrets.json', 'r').read())['web']['client_id']
CLIENT_SECRET = json.loads(
    open('/var/www/html/server/itemCatalog/client_secrets.json', 'r').read())['web']['client_secret']


secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
app.config['SECRET_KEY'] = secret_key

login_manager = LoginManager(app)
login_manager.login_view = "/login/general"

# Google blueprint for OAuth2
blueprint = make_google_blueprint(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    scope=["https://www.googleapis.com/auth/userinfo.profile"],
)

app.register_blueprint(blueprint, url_prefix="/login")
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


# Form for internal User creation/login
class UserLoginForm(Form):
    username = TextField('Username', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])


@login_manager.user_loader
def load_user(id):
    return session.query(User).get(int(id))


@app.route('/users', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username is None or password is None:
            print("missing arguments")
            abort(400)

        if session.query(User).filter_by(username=username).first() is not None:
            flash("User already exists")
            return redirect(url_for('showLogin'))

        user = User(username=username, authenticated=False)
        user.hash_password(password)
        session.add(user)
        session.commit()
        flash("Created new account")
        return redirect(url_for('showLogin'))
    else:
        return render_template('newuser.html')


# Directed to after google login so that we can internally create an account or log in
@app.route('/login/google', methods=['GET', 'POST'])
def googleLogin():
    name = request.args.get('name')
    username = name.replace(" ", "")
    print(username)
    testUser = session.query(User).filter_by(username=username).first()

    if not testUser:
        user = User(username=username, authenticated=True, oauth=True)
        session.add(user)
        session.commit()
        login_user(user, remember=True)
        flash("Welcome, %s. A new account has been created for you." % name)
        redirect(url_for('catHome'))
        return redirect(url_for('catHome'))

    else:
        print("Logging in...")
        user = session.query(User).filter_by(username=username).first()
        user.authenticated = True
        session.add(user)
        session.commit()
        login_user(user, remember=True)
        flash("Welcome, %s." % name)
        redirect(url_for('catHome'))
        return redirect(url_for('catHome'))


# Directed to on google logout to logout user locally
@app.route('/google/logout', methods=['GET', 'POST'])
def googleLogout():
    resp_json = google.get("/oauth2/v2/userinfo").json()
    user = session.query(User).filter_by(username=current_user.username).first()
    user.authenticated = False
    session.add(user)
    session.commit()
    logout_user()
    redirect(url_for('catHome'))
    return redirect(url_for('catHome'))


@app.route('/')
def catHome():
    categories = session.query(Categories).order_by(asc(Categories.name))
    items = session.query(Categories, Items).join(Items).filter(Items.cat_id == Categories.id).order_by(Items.time_added).limit(6)

    if (current_user.is_anonymous is not True) and (current_user.authenticated is True):
        return render_template('index.html', categories=categories, items=items)
    else:
        return render_template('publicindex.html', categories=categories, items=items)


@app.route('/catalog/<string:category>/items')
def indCat(category):
    categories = session.query(Categories).order_by(asc(Categories.name))
    indCategory = session.query(Categories).filter_by(name=category).one()
    items = session.query(Items).filter_by(cat_id=indCategory.id)
    count = items.count()
    if (current_user.is_anonymous is not True) and (current_user.authenticated is True) and (current_user.id is indCategory.owner_id):
        return render_template('itemlist.html', categories=categories, category=indCategory, items=items, count=count)
    else:
        return render_template('publicitemlist.html', categories=categories, category=indCategory, items=items, count=count)


@app.route('/catalog/<string:category>/<string:item>')
def indItem(category, item):
    categories = session.query(Categories).order_by(asc(Categories.name))
    indCategory = session.query(Categories).filter_by(name=category).one()
    indItem = session.query(Items).filter_by(name=item, cat_id=indCategory.id).one()
    if (current_user.is_anonymous is not True) and (current_user.authenticated is True) and (current_user.id is indItem.owner_id):
        return render_template('inditem.html', category=indCategory, item=indItem, categories=categories)
    else:
        return render_template('publicinditem.html', category=indCategory, item=indItem, categories=categories)


@app.route('/login/general', methods=['GET', 'POST'])
def showLogin():
    form = UserLoginForm(request.form)

    if request.method == 'POST' and form.validate():
        user = session.query(User).filter_by(username=form.username.data).first()
        if user:
            if user.verify_password(form.password.data):
                user.authenticated = True
                session.add(user)
                session.commit()
                login_user(user, remember=True)
                flash("Logged in as %s" % user.username)
                return redirect(url_for('catHome'))
            else:
                flash('Invalid username or password.')
                return redirect(url_for('showLogin'))

    return render_template('login.html', CLIENT_ID=CLIENT_ID, CLIENT_SECRET=CLIENT_SECRET)


@app.route('/categoryCreate', methods=['GET', 'POST'])
@login_required
def createCat():
    if request.method == 'POST':
        catName = request.form['name']
        newCat = Categories(name=catName, owner_id=current_user.id)
        session.add(newCat)
        session.commit()
        flash("Succussfully created the %s category!" % catName)
        return redirect(url_for('catHome'))
    else:
        return render_template('createcategory.html')


# Logout
@app.route('/disconnect')
@login_required
def disconnect():
    user = current_user
    if user.oauth is True:
        user.authenticated = False
        session.add(user)
        session.commit()
        logout_user()
        flash("You have been successfully logged out!")
        return redirect(url_for('googleLogout'))
    else:
        user.authenticated = False
        session.add(user)
        session.commit()
        logout_user()
        flash("You have been successfully logged out!")
        return redirect(url_for('catHome'))


@app.route('/create', methods=['GET', 'POST'])
@login_required
def createItem():
    categories = session.query(Categories).all()
    items = session.query(Items).all()
    if request.method == 'POST':
        catName = request.form['category']
        indCat = session.query(Categories).filter_by(name=catName).one()
        if current_user.id is not indCat.owner_id:
            flash("You are not the owner of that category. You can only edit your own items and categories")
            return redirect(url_for('catHome'))

        categories = session.query(Categories).all()
        for c in categories:
            if(c.name == catName):
                cat_id = c.id
        newItem = Items(name=request.form['name'], description=request.form['description'], cat_id=cat_id,  owner_id=current_user.id)
        session.add(newItem)
        session.commit()
        flash('Successfully Created %s' % newItem.name)
        return redirect(url_for('indCat', category=catName))
    else:
        return render_template('createitem.html', items=items, categories=categories)


@app.route('/catalog/<string:category>/<string:item>/edit', methods=['GET', 'POST'])
@login_required
def editItem(category, item):
    categories = session.query(Categories).order_by(asc(Categories.name))
    indCategory = session.query(Categories).filter_by(name=category).one()
    indItem = session.query(Items).filter_by(name=item, cat_id=indCategory.id).one()

    if request.method == 'POST'  and (current_user.id is indCategory.owner_id):
        catName = request.form['category']
        indCat = session.query(Categories).filter_by(name=catName).one()

        if current_user.id is not indCat.owner_id:
            flash("You are not the owner of that category. You can only edit your own items and categories")
            return redirect(url_for('indItem', category=catName, item=indItem.name))

        categories = session.query(Categories).all()
        for c in categories:
            if(c.name == catName):
                cat_id = c.id

        if request.form['name']:
            indItem.name = request.form['name']
            print(indItem.name)
        if request.form['description']:
            indItem.description = request.form['description']
            print(indItem.description)

        indItem.cat_id = cat_id
        session.add(indItem)
        session.commit()
        flash('Successfully edited %s' % indItem.name)
        return redirect(url_for('indItem', category=catName, item=indItem.name))

    else:
        return render_template('edititem.html', item=indItem, categories=categories, category=indCategory)


@app.route('/catalog/<string:category>/<string:item>/delete', methods=['GET', 'POST'])
@login_required
def deleteItem(category, item):
    indCategory = session.query(Categories).filter_by(name=category).one()
    indItem = session.query(Items).filter_by(name=item, cat_id=indCategory.id).one()
    if (request.method == 'POST') and (current_user.id is indCategory.owner_id):
        session.delete(indItem)
        session.commit()
        return redirect(url_for('indCat', category=indCategory.name))
    else:
        return render_template('deleteitem.html', item=indItem, category=indCategory)


@app.route('/catalog/<string:category>/delete', methods=['GET', 'POST'])
@login_required
def deleteCat(category):
    indCategory = session.query(Categories).filter_by(name=category).one()

    if request.method == 'POST':

        if current_user.id is not indCategory.owner_id:
            flash("You are not the owner of that category. You can only edit your own items and categories")
            return redirect(url_for('indCat', category=indCategory.name))

        items = session.query(Items).filter_by(cat_id=indCategory.id)

        for i in items:
            session.delete(i)

        session.delete(indCategory)
        session.commit()

        return redirect(url_for('catHome'))
    else:
        return render_template('deletecategory.html', cat=indCategory)


@app.route('/catalog/JSON')
def categoriesJSON():
    categories = session.query(Categories).order_by(asc(Categories.id))
    items = session.query(Items).all()

    return jsonify(Categories=[c.serialize for c in categories], Items=[i.serialize for i in items])


@app.route('/catalog/<string:category>/JSON')
def indCatJSON(category):
    indCategory = session.query(Categories).filter_by(name=category).one()
    items = session.query(Items).filter_by(cat_id=indCategory.id)

    return jsonify(categoryItems=[i.serialize for i in items])


@app.route('/catalog/<string:category>/<string:item>/JSON')
def indItemJSON(category, item):
    categories = session.query(Categories).order_by(asc(Categories.name))
    indCategory = session.query(Categories).filter_by(name=category).one()
    indItem = session.query(Items).filter_by(name=item, cat_id=indCategory.id).one()

    return jsonify(Item=indItem.serialize)

if __name__ == '__main__':
    app.config['SECRET_KEY'] = secret_key
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
