import os
import json
import uuid

import psycopg2 
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from flask import Flask, redirect, url_for, render_template, request, session, g, current_app
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash, check_password_hash

from db import GeonetDB
from login import UserLogin

app = Flask(__name__)
app.config.from_object(os.environ['FLASK_CONFIGURATION_SETUP'])

login_manager = LoginManager(app)

@app.route('/')
def index():
	print(current_user)
	return render_template('main.html',
			loggedin=current_user,
			groups=geodb.getUserGroups(user_id=current_user.get_id() if current_user else None),
			logins=geodb.getUsersLogins()
	)

@app.route('/map')
@login_required
def map():
	city='moscow'
	return render_template('map.html',
			city=city,
			loggedin=current_user,
			groups=geodb.getUserGroups(user_id=current_user.get_id() if current_user.is_authenticated() else None)
	)

@app.route('/groups/<group_name>')
@login_required
def group(group_name):
	return group_name

@app.route('/addgroup', methods=['GET', 'POST'])
@login_required
def addgroup():
	if request.method == 'POST':
		group_name = request.form['name']
		group_users = []
		group_users.append(current_user.get_login())
		for i in range(0, len(request.form) - 1):
			group_users.append(request.form['login' + str(i)])
		geodb.addGroup(group_name)
		geodb.addUsersToGroup(group_name ,group_users)
	return render_template('addgroup.html',
			loggedin=current_user,
			groups=geodb.getUserGroups(user_id=current_user.get_id() if current_user else None)
	)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		user = geodb.getUserByLogin(request.form['login'])
		if user and check_password_hash(user['passwd'], request.form['passwd']):
			userLogin = UserLogin().create(user)
			login_user(userLogin)
			return redirect(url_for('index'))
	return render_template('login.html',
			loggedin=current_user,
			groups=geodb.getUserGroups(user_id=current_user.get_id() if current_user else None)
	)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		if len(request.form['login']) >= 0 and len(request.form['passwd1']) >= 0 and (request.form['passwd1'] == request.form['passwd2']):
			if geodb.isFreeLogin(request.form['login']):	
				print('reg new user\n')				
				hash = generate_password_hash(request.form['passwd1'])
				geodb.addUser(request.form['login'], hash)
				return redirect(url_for('login'))
	return render_template('register.html',
			loggedin=current_user,
			groups=geodb.getUserGroups(user_id=current_user.get_id() if current_user else None)
	)

@app.route('/profile')
@login_required
def profile():
	return render_template('profile.html',
			user_id=current_user.get_id() if current_user else None,
			loggedin=current_user,
			groups=geodb.getUserGroups(user_id=current_user.get_id() if current_user else None)
	)

@login_manager.user_loader
def load_user(user_id):
	print('load user')
	print(user_id)
	return UserLogin().fromDB(user_id, geodb)

@app.route('/upload', methods=['POST'])
@login_required
def upload():
	if request.method == 'POST':
		geodb.addEvent(name=request.form['name'],
				description=request.form['description'],
				groupId=1,#подправить
				lat=request.form['lat'],
				lng=request.form['lng'],
		)
		user_id = int(current_user.get_id())
		event_id = 1
		media = []
		for f in request.files.getlist('photo'):
			name = get_free_name()
			mediatype = None
			_, ext = os.path.splitext(f.filename)
			if ext in ['.jpg', '.jpeg', '.png']:
				mediatype = 'photo'
				f.save(os.path.join('static', name + ext))
				media.append((user_id, event_id, mediatype, name))
		for f in request.files.getlist('video'):
			print('i')
			name = get_free_name()
			mediatype = None
			_, ext = os.path.splitext(f.filename)
			if ext in ['.avi', '.mkv']:
				mediatype = 'video'
				f.save(os.path.join('static', name + ext))
				media.append((user_id, event_id, mediatype, name))
		geodb.addMedia(media)
	return 'hello'

		
	

geodb = None
@app.before_request
def before_request():
	global geodb
	db = get_db()
	geodb = GeonetDB(db)

@app.teardown_appcontext
def close_db(error=None):
	if hasattr(g, 'db'):
		g.db.close()

def get_db():
	if not hasattr(g, 'db'):
		g.db = psycopg2.connect(dbname=current_app.config['DATABASE'], user=current_app.config['USER'])
	return g.db

def get_free_name():
	name = str(uuid.uuid4())
	pathname = os.path.join('static', name)
	while os.path.exists(pathname):
		name = str(uuid.uuid4())
		pathname = os.path.join('static', name)
	return name

if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', port='8000')