import psycopg2
import click

import psycopg2.extras


class GeonetDB:
	def __init__(self, db):
		self.__db = db
		self.__cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)


	def get_user(self, user_id):
		try:
			self.__cursor.execute('SELECT * FROM users WHERE id = %s LIMIT 1', (user_id,))
			user = self.__cursor.fetchone()
			if not user:
				return False
			return user
		except psycopg2.Error as e:
			print(e.pgerror)
			return False

	def add_user(self, login, hash):
		try:
			self.__cursor.execute('INSERT INTO users (login, passwd) VALUES (%s, %s);', (login, hash))
			self.__cursor.execute('INSERT INTO groups (name) VALUES (%s)', (login + '_my_group', ))
			#добавляем записи в служебную таблицу
			self.__db.commit()
			self.__cursor.execute('SELECT id FROM users WHERE login = %s', (login,))
			usr_id = self.__cursor.fetchone()['id']
			self.__cursor.execute('SELECT id FROM groups WHERE name = %s', (login + '_my_group',))
			grp_id = self.__cursor.fetchone()['id']
			self.__cursor.execute('INSERT INTO service_t (usr, grp) VALUES (%s, %s)', (usr_id, grp_id))
			self.__db.commit()
		except psycopg2.Error as e:
			print(e.pgerror)

	def is_free_login(self, login):
		try:
			self.__cursor.execute('SELECT count(*) as cnt FROM users WHERE login = %s', (login,))
			amount = self.__cursor.fetchone()
			print(amount)
			if amount[0] == 0:
				return True
			else:
				return False
		except psycopg2.Error as e:
			print(e.pgerror)
			return False

	def get_user_by_login(self, login):
		self.__cursor.execute('SELECT * FROM users WHERE login = %s', (login,))
		user = self.__cursor.fetchone()
		return user


	def execute_script(self, script):
		self.__cursor.execute(script)
		self.__db.commit()


	def get_user_groups(self, user_id):
		try:
			self.__cursor.execute('SELECT g.id, g.name FROM groups as g JOIN service_t as srv ON g.id = srv.grp WHERE srv.usr = %s', (user_id,))
			groups = self.__cursor.fetchall()
			return groups
		except psycopg2.Error as e:
			print(e.pgerror)
			return None


	def add_group(self, name):
		try:
			self.__cursor.execute('INSERT INTO groups (name) VALUES (%s)', (name, ))
			self.__db.commit()
		except psycopg2.Error as e:
			print(e.pgerror)


	def add_users_to_group(self, name, logins):
		try:
			self.__cursor.execute('SELECT id FROM groups WHERE name = %s', (name,))
			grp_id = self.__cursor.fetchone()['id']
			for login in logins:
				self.__cursor.execute('SELECT id FROM users WHERE login = %s', (login,))
				usr_id = self.__cursor.fetchone()['id']
				self.__cursor.execute('INSERT INTO service_t (usr, grp) VALUES (%s, %s)', (usr_id, grp_id))
			self.__db.commit()
		except psycopg2.Error as e:
			print(e.pgerror)


	def get_users_logins(self):
		try:
			self.__cursor.execute('SELECT login FROM users')
			logins = [ data['login'] for data in self.__cursor.fetchall()]
			return logins
		except psycopg2.Error as e:
			print(e.pgerror)
			return False


	def add_event(self, name, description, group_id, lat, lng):
		try:
			self.__cursor.execute('INSERT INTO events (name, description, grp, longtitude, latitude) VALUES (%s, %s, %s, %s, %s)',
								(name, description, group_id, lng, lat)
			)
			self.__db.commit()
		except psycopg2.Error as e:
			print(e.pgerror)


	def get_event_id_by_name_and_group(self, name, group_id):
		try:
			self.__cursor.execute('SELECT id FROM events WHERE name = %s AND grp = %s',
								(name, group_id)
			)
			id = self.__cursor.fetchone()['id']
			return id
		except psycopg2.Error as e:
			print(e.pgerror)


	def add_media(self, media):
		try:
			self.__cursor.executemany('INSERT INTO media (owner, event, type, path) VALUES (%s, %s, %s, %s)', media)
			self.__db.commit()
		except psycopg2.Error as e:
			print(e.pgerror)


	def get_users_by_group_id(self, group_id):
		try:
			self.__cursor.execute('SELECT u.id as id, u.login as login FROM users AS u JOIN service_t as s ON u.id = s.usr WHERE s.grp = %s', (group_id, ))
			users = self.__cursor.fetchall()
			return users
		except psycopg2.Error as e:
			print(e.pgerror)


	def get_events_by_group_id(self, group_id):
		try:
			self.__cursor.execute('SELECT * FROM events WHERE grp = %s', (group_id, ))
			events = self.__cursor.fetchall()
			return events
		except psycopg2.Error as e:
			print(e.pgerror)


	def get_media_by_event_id(self, event_id):
		pass