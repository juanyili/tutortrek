#!/usr/local/bin/python2.7

# CS304 Assignment 5
# Wanyi Li
import cgi
import cgitb; cgitb.enable()
import MySQLdb
import dbconn
import wendy_dsn

def register(fillers, password):
	conn = connect()
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	curs.execute("insert into people (name, username, password, role) values (%s, %s, %s, 'Tutee');", (fillers['name'], fillers['username'], password,))
	
	row = curs.fetchone()
	print row
	message =  "<p>Message: Your info is registered. Your role is currently a tutee. If you are a tutor, please contact admin to add you."
	return message

def login(username, password, choice):
	conn = connect()
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('SELECT name, password, role FROM people WHERE username = %s;',(username,))
	row = curs.fetchone()
	if row == None:
		message = "<p>Message: error: your information is not registered yet.</p>"
		return [False, message, None]
	else:
		if '{password}'.format(**row) == password:
			role = '{role}'.format(**row)
			name = '{name}'.format(**row)
			if role == choice:
				message = "<p>Message: Successfully logged in!</p>"
				return [True, message, role, name]
			elif role == 'Tutor' and choice == 'Tutee': # this is a special case because tutors can log in as both a tutor or a tutee
				message = "<p>Message: Successfully logged in! You are a tutor but you are going to the tutee page right now.</p>"
				return [True, message, role, name]
			else:
				message = "<p>Message: Sorry you do not have the authorization for the role you selected. Please contact administrator if you have another role.</p>"
				return [False, message, role, name]
		else:
			message = "<p>Message: The information you entered is not correct.</p>"
			return [False, message, None]
	
def connect():
	dsn = wendy_dsn.DSN
	dsn['database'] = 'wli2_db'
	conn = dbconn.connect(dsn)
	return conn

if __name__ == '__main__':
	print main()