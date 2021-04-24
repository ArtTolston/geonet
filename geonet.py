import os
from flask import Flask, redirect, url_for, render_template, request, session, g
from db import get_db



app = Flask(__name__)
enviroment_configuration = os.environ['FLASK_CONFIGURATION_SETUP']
app.config.from_object(enviroment_configuration)


@app.route('/')
def index():
   return render_template('base.html')

@app.route('/map')
def map():
	city='moscow'
	return render_template('map.html', city=city)

#добавить загрузку имени пользователя через файл и кинуть файл в gitignore

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
		#db.cursor().execute('INSERT INTO events (description, imgId, userId, shirota, dolgota) VALUES ()') #сделать нормальную схему таблицы, добавить авторизацию, чтобы можно было заполнить юзеров
		db.commit()
		cur.close()
		return redirect(url_for('map', city='moscow'))





db = None
@app.before_request
def before_request():
	global db
	db = get_db()

@app.teardown_appcontext
def close_db(error=None):
	db = g.pop('db', None)
	if db is not None:
		db.close()


if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', port='8000')
