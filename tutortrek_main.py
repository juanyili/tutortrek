#!/usr/local/bin/python2.7

# CS304 Assignment 5
# Wanyi Li

############################################
# This is a module that provides helper methods 
# for the main page of tutortrek.
############################################
import cgi
import cgitb; cgitb.enable()
import MySQLdb
import dbconn
import tutortrek_utils

#################################################
# This method takes in information like
# name, username and password and register the
# user into the database with the default role
# of a tutee. Since the database asks username
# to be unique, it catches the error ofduplicate
# username (MySQL Error 1062) and pring the error
# message.
################################################
def register(fillers, password):
	conn = tutortrek_utils.connect()
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	try:
		curs.execute("insert into people (name, username, password, role) values (%s, %s, %s, 'Tutee');", (fillers['name'], fillers['username'], password,))
		row = curs.fetchone()
		message =  "<p>Message: Your info is registered. Your role is currently a tutee. If you are a tutor, please contact admin to add you."
	except MySQLdb.Error, e:
		if e.args[0] == 1062:
			message = "Sorry, this username already exists in the database. Please choose another one. Thank you!"
		else:
			message = "Sorry, MySQL error [%d] has occured: %s" % (e.args[0], e.args[1])
	return message

############################################
# This methods does the log in function in
# the main page and returns data to be stored
# in each session data (sess_data).
# sess_data['success'] will be True if the
# login is successful. At the same time, it 
# returns a message about the login and the role
# and the name of the user, for the session to
# to keep track later.
############################################
def login(username, password, choice):
	conn = tutortrek_utils.connect()
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('SELECT name, password, role FROM people WHERE username = %s;',(username,))
	row = curs.fetchone()
	if row == None:
		message = "<p>Message: error: your information is not registered yet.</p>"
		return [False, message, None, None]
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
			return [False, message, None, None]