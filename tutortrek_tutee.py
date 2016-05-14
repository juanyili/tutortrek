#!/usr/local/bin/python2.7

# CS304 Final project
# Wanyi Li

############################################
# This is a module that provides helper methods 
# for the tutee page of tutortrek.
############################################

import cgi
import cgitb; cgitb.enable()
import MySQLdb
import dbconn
import wendy_dsn
import tutortrek_utils

############################################
# This method generates a dropdown menu of
# all the sessions of a class that the user has
# chosen (cid).
# 'sid' is the input for the session id. If it 
# is not None, then the selector will select the
# 'sid' option. This is used when user clicks 
# on a session, the dropdown menu should automatically
# stay at the option that the user has chosen.
############################################
def generateSession(cid, sid = None):
	conn = tutortrek_utils.connect()
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	menu = "<select name ='sid'>"
	curs.execute('SELECT sid, session_date, tutor from session where cid = %s', (cid,))
	row = curs.fetchone()
	if row == None:
		menu+='<option selected disabled>No sessions</option>'
	else:
		if sid == None:
			while row != None:
				menu+="<option value={sid}>{session_date} with {tutor}</option>".format(**row)
				row = curs.fetchone()
		else:
			while row != None:
				if '{sid}'.format(**row) == sid:
					menu+="<option selected value={sid}>{session_date} with {tutor}</option>".format(**row)
				else:
					menu+="<option value={sid}>{session_date} with {tutor}</option>".format(**row)
				row = curs.fetchone()
	menu += "</select>"
	return menu

############################################
# This method takes a session id and stores
# the attendance data into each session which
# just increment the 'attendance' value by 1.
############################################
def logAttendance(sid):
	conn = tutortrek_utils.connect()
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	curs.execute('UPDATE session SET attendance = attendance+1 where sid = %s;', (sid,))
	return "We have logged your attendance."

############################################
# This method takes a session id, rating score
# and a tutee username to store the rating score
# the tutee has rated a session. The tutee information
# is stored but administrators cannot see them.
# We still stored the information in case there will
# be irresponsible ratings, we can trace back.
############################################
def rateSession(sid, rating, tutee):
	conn = tutortrek_utils.connect()
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	curs.execute('INSERT INTO ratings (tutee, sid, rating_score) values (%s, %s, %s);', (tutee, sid, int(rating),))
	return "You have successfully rated this session."

