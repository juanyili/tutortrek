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

def connect():
	dsn = wendy_dsn.DSN
	dsn['database'] = 'wli2_db'
	conn = dbconn.connect(dsn)
	return conn

if __name__ == '__main__':
	print main()