#!/usr/local/bin/python2.7

# CS304 Final project
# Wanyi Li
import cgi
import cgitb; cgitb.enable()
import MySQLdb
import dbconn
import wendy_dsn

def addSession(fillers):
	conn = connect()
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	curs.execute('SELECT * FROM people WHERE people.username = %s;',(fillers['username'],))
	if curs.fetchone() == None:
		message = "<p>Message: error: something went very wrong.</p>"
	else:
		attendance_data = (int(fillers['cid']), fillers['date'], fillers['tutor'],)			
		curs.execute('SELECT sid from session where cid = %s and session_date = %s\
			and tutor = (SELECT username from people where name=%s and role="Tutor");', attendance_data)
		row = curs.fetchone()
		if row == None:
			message = "<p>Message: your session information is invalid. Please check if you have all the correct information."
		else: # information is all correct!
			sid = '{sid}'.format(**row)
			curs.execute('UPDATE session SET attendance = attendance+1 where sid = %s;', (sid,))
			message = "<p>Message: Your attendance information is stored in the database.</p>"
	return message


def allClass(cid=None):
	conn = connect()
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	menu = "<select name ='cid'><option selected disabled>Class title</option>"
	if cid == None:
		curs.execute('SELECT cid, title FROM class;')
		row = curs.fetchone()
		while row != None:
			menu+="<option value={cid}>{title}</option>".format(**row)
			row = curs.fetchone()
	else:
		curs.execute('SELECT cid, title FROM class;')
		row = curs.fetchone()
		while row != None:
			if '{cid}'.format(**row) == cid:
				menu+="<option selected value={cid}>{title}</option>".format(**row)
			else:
				menu+="<option value={cid}>{title}</option>".format(**row)
			row = curs.fetchone()
	menu+="</select>"
	return menu

def searchClass(search):
	conn = connect()
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	menu= "<select name ='cid'><option selected disabled>Class title</option>"
	curs.execute('SELECT cid, title FROM class where title like %s;', ('%'+search+'%',))
	row = curs.fetchone()
	if row == None:
		menu = allClass()
	else:
		while row!= None:
			menu+="<option value={cid}>{title}</option>".format(**row)
			row = curs.fetchone()
	menu += "</select>"
	return menu


def generateSession(cid, sid = None):
	conn = connect()
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

def logAttendance(sid):
	conn = connect()
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	curs.execute('UPDATE session SET attendance = attendance+1 where sid = %s;', (sid,))
	return "We have logged your attendance."

def rateSession(sid, rating, tutee):
	conn = connect()
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	curs.execute('INSERT INTO ratings (tutee, sid, rating_score) values (%s, %s, %s);', (tutee, sid, int(rating),))
	return "You have successfully rated this session."

def connect():
	dsn = wendy_dsn.DSN
	dsn['database'] = 'wli2_db'
	conn = dbconn.connect(dsn)
	return conn

if __name__ == '__main__':
	print main()