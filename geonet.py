import os
import json
import uuid

import psycopg2 
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from flask import Flask, redirect, url_for, render_template, request, session, g, current_app, flash
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
			groups=geodb.get_user_groups(user_id=current_user.get_id() if current_user else None),
			logins=geodb.get_users_logins()
	)

@app.route('/map')
@login_required
def map():
	return render_template('map.html',
			city='moscow',
			loggedin=current_user,
			groups=geodb.get_user_groups(user_id=current_user.get_id() if current_user.is_authenticated() else None)
	)

@app.route('/groups/<group_id>')
@login_required
def group(group_id):
	return render_template('group_info.html',
			loggedin=current_user,
			users=geodb.get_users_by_group_id(group_id),
			events=geodb.get_events_by_group_id(group_id),
			groups=geodb.get_user_groups(user_id=current_user.get_id() if current_user else None)
	)

@app.route('/addgroup', methods=['GET', 'POST'])
@login_required
def addgroup():
	if request.method == 'POST':
		group_name = request.form['name']
		group_users = []
		group_users.append(current_user.get_login())
		for i in range(0, len(request.form) - 1):
			group_users.append(request.form['login' + str(i)])
		geodb.add_group(group_name)
		geodb.add_users_to_group(group_name ,group_users)
	return render_template('addgroup.html',
			loggedin=current_user,
			groups=geodb.get_user_groups(user_id=current_user.get_id() if current_user else None)
	)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		user = geodb.get_user_by_login(request.form['login'])
		if user and check_password_hash(user['passwd'], request.form['passwd']):
			userLogin = UserLogin().create(user)
			login_user(userLogin)
			return redirect(url_for('index'))
	return render_template('login.html',
			loggedin=current_user,
			groups=geodb.get_user_groups(user_id=current_user.get_id() if current_user else None)
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
			if geodb.is_free_login(request.form['login']):	
				print('reg new user\n')				
				hash = generate_password_hash(request.form['passwd1'])
				geodb.add_user(request.form['login'], hash)
				return redirect(url_for('login'))
	return render_template('register.html',
			loggedin=current_user,
			groups=geodb.get_user_groups(user_id=current_user.get_id() if current_user else None)
	)

@app.route('/profile')
@login_required
def profile():
	return render_template('profile.html',
			user_id=current_user.get_id() if current_user else None,
			loggedin=current_user,
			groups=geodb.get_user_groups(user_id=current_user.get_id() if current_user else None)
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
		
		geodb.add_event(name=request.form['name'],
				description=request.form['description'],
				group_id=request.form['group'],
				lat=request.form['lat'],
				lng=request.form['lng'],
		)
		user_id = int(current_user.get_id())
		event_id = geodb.get_event_id_by_name_and_group(name=request.form['name'], group_id=request.form['group'])
		media = []
		for f in request.files.getlist('photo'):
			if not f.content_length:
				continue
			name = get_free_name()
			mediatype = 'photo'
			_, ext = os.path.splitext(f.filename)
			if ext in ['.jpg', '.jpeg', '.png']:
				f.save(os.path.join(current_app.config['MEDIA_PATH'], name + ext))
				media.append((user_id, event_id, mediatype, name))
			else:
				flash('Неправильный формат фото')
				return redirect(url_for('map'))
		for f in request.files.getlist('video'):
			if not f.content_length:
				continue
			name = get_free_name()
			mediatype = 'video'
			_, ext = os.path.splitext(f.filename)
			if ext in ['.avi', '.mkv']:
				f.save(os.path.join(current_app.config['MEDIA_PATH'], name + ext))
				media.append((user_id, event_id, mediatype, name))
			else:
				flash('Неправильный формат видео')
				return redirect(url_for('map'))
		geodb.add_media(media)
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
	pathname = os.path.join(current_app.config['MEDIA_PATH'], name)
	while os.path.exists(pathname):
		name = str(uuid.uuid4())
		pathname = os.path.join(current_app.config['MEDIA_PATH'], name)
	return name

if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', port='8000')