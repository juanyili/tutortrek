#!/usr/local/bin/python2.7

# CS304 Final Project
# Wanyi Li
import cgi
import cgitb; cgitb.enable()
import MySQLdb
import dbconn
import wendy_dsn

def addTutor(fillers, tutor_list):
	conn = connect()
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	message = "<p>no message."
	for i in range(len(tutor_list)):
		if tutor_list[i] == True:
			tid = 'tid'+str(i)
			cid = 'cid'+str(i)
			cname = 'cname'+str(i)
			curs.execute("SELECT * from people where username = %s;", (fillers[tid],))
			row = curs.fetchone()
			if row == None:
				message += "<p>Message: This person is not registered in the database yet. You can not add them before they register on the main page.</p>"
			else:
				curs.execute("UPDATE people SET people.role = 'Tutor' where people.username=%s;", (fillers[tid],))
				data = (int(fillers[cid]), fillers[cname])
				curs.execute("INSERT into class (cid, title) values (%s, %s);", data)
				message += "<p>Message: The tutor and class information is added.</p>"
	return message

def searchTutor(fillers):
	conn = connect()
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	tid = fillers['tutor_id']
	curs.execute("SELECT username, name, role from people where username = %s;", (tid,))
	row = curs.fetchone()
	if row == None:
		message = '<p>This person is not in the database.'
	elif '{role}'.format(**row) !='Tutor':
		message = 'Student with ID {uid} is {name}. Please add them as a tutor first.'.format(**row)
	else:
		message = '<p>This tutor is {name}.\n'.format(**row)
		curs.execute("SELECT sid, cid, session_date, length, attendance from session where tutor = %s;", (tid,))
		row = curs.fetchone()
		while row != None:
			message += '<li>session {sid} for class {cid} was on {session_date} for {length} hours. {attendance} students came.'.format(**row)
			row = curs.fetchone()
		else:
			message+=''
	return message

def searchClass(fillers):
	conn = connect()
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	cid = fillers['class_id']
	curs.execute("SELECT cid, title from class where cid = %s", (cid,))
	row = curs.fetchone()
	if row!=None:
		message = 'Class {cid} is {title}.'.format(**row)
		curs.execute("SELECT sid, cid, session_date, length, attendance from session where cid = %s;", (cid,))
		row = curs.fetchone()
		while row!=None:
			message += '<li>session {sid} for class {cid} was on {session_date} for {length} hours. {attendance} students came.'.format(**row)
			row = curs.fetchone()
		else:
			message += ''
	else:
		message = '<p>The class you are looking for does not exist. Please check again!'
	return message

def connect():
	dsn = wendy_dsn.DSN
	dsn['database'] = 'wli2_db'
	conn = dbconn.connect(dsn)
	return conn

if __name__ == '__main__':
	print main()