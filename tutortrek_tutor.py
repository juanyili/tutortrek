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
	curs.execute('SELECT username, name, role FROM people WHERE people.username = %s;',(fillers['username'],))
	row = curs.fetchone()
	if row == None:
		message = "<p>Message: error: your information is not registered yet.</p>"
	elif '{role}'.format(**row) != 'Tutor':
		message = "<p>Message: errow: you are not a tutor. Please contact admin to add you as a tutor."
	else:
		session_data = (int(fillers['cid']), fillers['date'], float(fillers['duration']), fillers['username'])			
		curs.execute('INSERT INTO session (cid, session_date, length, tutor, attendance) values (%s, %s, %s, %s,0);', session_data)
		message = "<p>Message: Your works sessions are stored in the database.</p>"
	return message

def generateClass(cid=None):
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



def connect():
	dsn = wendy_dsn.DSN
	dsn['database'] = 'wli2_db'
	conn = dbconn.connect(dsn)
	return conn

if __name__ == '__main__':
	print main()