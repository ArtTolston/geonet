import psycopg2
import click

import psycopg2.extras


class GeonetDB:
	def __init__(self, db):
		self.__db = db
		self.__cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)


	def getUser(self, user_id):
		try:
			self.__cursor.execute('SELECT * FROM users WHERE id = %s LIMIT 1', (user_id,))
			user = self.__cursor.fetchone()
			if not user:
				return False
			return user
		except psycopg2.Error as e:
			print(e.pgerror)
			return False

	def addUser(self, login, hash):
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

	def isFreeLogin(self, login):
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

	def getUserByLogin(self, login):
		self.__cursor.execute('SELECT * FROM users WHERE login = %s', (login,))
		user = self.__cursor.fetchone()
		return user


	def executeScript(self, script):
		self.__cursor.execute(script)
		self.__db.commit()


	def getUserGroups(self, user_id):
		try:
			self.__cursor.execute('SELECT g.name FROM groups as g JOIN service_t as srv ON g.id = srv.grp WHERE srv.usr = %s', (user_id,))
			groups = self.__cursor.fetchall()
			return groups
		except psycopg2.Error as e:
			print(e.pgerror)
			return None


	def addGroup(self, name):
		try:
			self.__cursor.execute('INSERT INTO groups (name) VALUES (%s)', (name, ))
			self.__db.commit()
		except psycopg2.Error as e:
			print(e.pgerror)


	def addUsersToGroup(self, name, logins):
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


	def getUsersLogins(self):
		try:
			self.__cursor.execute('SELECT login FROM users')
			logins = [ data['login'] for data in self.__cursor.fetchall()]
			return logins
		except psycopg2.Error as e:
			print(e.pgerror)
			return False