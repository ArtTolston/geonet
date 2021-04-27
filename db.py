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
			print('user seccusfully added')
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