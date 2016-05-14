#!/usr/local/bin/python2.7

# CS304 Final project
# Wanyi Li

############################################
# This is a module that provides helper methods 
# for the tutor page of tutortrek.
############################################

import cgi
import cgitb; cgitb.enable()
import MySQLdb
import dbconn
import wendy_dsn
import tutortrek_utils

############################################
# This method add tutoring sessions that tutor
# has worked for. After this informaiton is stored,
# tutees can select 'attend' these sessions.
# It takes informaiton like class id, data,
# duration, username and store a new session.
############################################
def addSession(fillers):
	conn = tutortrek_utils.connect()
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	curs.execute('SELECT username, name, role FROM people WHERE people.username = %s;',(fillers['username'],))
	row = curs.fetchone()
	if row == None:
		message = "<p>Message: error: your information is not registered yet.</p>"
	elif '{role}'.format(**row) != 'Tutor':
		message = "<p>Message: error: you are not a tutor. Please contact admin to add you as a tutor."
	else:
		session_data = (int(fillers['cid']), fillers['date'], float(fillers['duration']), fillers['username'])			
		curs.execute('INSERT INTO session (cid, session_date, length, tutor, attendance) values (%s, %s, %s, %s,0);', session_data)
		message = "<p>Message: Your works sessions are stored in the database.</p>"
	return message
