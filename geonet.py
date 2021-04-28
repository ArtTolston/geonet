import os
from db import GeonetDB 
import psycopg2 
from login import UserLogin
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from flask import Flask, redirect, url_for, render_template, request, session, g, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask.cli import with_appcontext




app = Flask(__name__)
enviroment_configuration = os.environ['FLASK_CONFIGURATION_SETUP']
app.config.from_object(enviroment_configuration)

login_manager = LoginManager(app)


@app.route('/')
def index():
	return render_template('base.html', loggedin=current_user, groups=geodb.getUserGroups(user_id=current_user.get_id()))


@app.route('/map')
@login_required
def map():
	city='moscow'
	return render_template('map.html', city=city, loggedin=current_user, groups=geodb.getUserGroups(user_id=current_user.get_id()))


@app.route('/groups/<group_name>')
@login_required
def group(group_name):
	return group_name

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		user = geodb.getUserByLogin(request.form['login'])
		if user and check_password_hash(user['passwd'], request.form['passwd']):
			userLogin = UserLogin().create(user)
			login_user(userLogin)
			return redirect(url_for('index'))
	return render_template('login.html', loggedin=current_user, groups=geodb.getUserGroups(user_id=current_user.get_id()))

@app.route('/logout')
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
	return render_template('register.html', loggedin=current_user, groups=geodb.getUserGroups(user_id=current_user.get_id()))


@app.route('/profile')
@login_required
def profile():
	return render_template('profile.html', user_id=current_user.get_id(), loggedin=current_user, groups=geodb.getUserGroups(user_id=current_user.get_id()))


@login_manager.user_loader
def load_user(user_id):
	print('load user')
	print(user_id)
	return UserLogin().fromDB(user_id, geodb)



@app.route('/upload', methods=['POST'])
def upload():
	if request.method == 'POST':
		#description = request.form['description']
		file = request.files['file']

		hashs = str(abs(hash(file.read())))[:25] 
		filename = 'static/' + hashs + '.jpeg'
		print(hashs)
		with open(filename, 'wb') as f:
			f.write(file.read())
		db.cursor().execute('INSERT INTO images (name) VALUES (%s)', (hashs,));
		db.commit()
		cur.close()
		return redirect(url_for('map', city='moscow'))





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







if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', port='8000')
