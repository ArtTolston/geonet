import psycopg2
import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
	if 'db' not in g:
		g.db = psycopg2.connect(dbname=current_app.config['DATABASE'], user=current_app.config['USER'])
	return g.db


def close_db(e=None):
	db = g.pop('db', None)
	if db is not None:
		db.close()


def init_db():
    db = psycopg2.connect(user='udk2018', dbname='geonet')
    with open('schema.sql', 'r') as f:
        db.cursor().execute(f.read())
