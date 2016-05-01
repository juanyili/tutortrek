#!/usr/local/bin/python2.7

# CS304 Final Project
# Wanyi Li
import cgi
import cgitb; cgitb.enable()
import MySQLdb
import dbconn
import wendy_dsn

def addTutor(conn, fillers, tutor_list):
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	message = "<p>no message."
	for i in range(len(tutor_list)):
		if tutor_list[i] == True:
			tid = 'tid'+str(i)
			cid = 'cid'+str(i)
			cname = 'cname'+str(i)
			data = (int(fillers[tid]),)
			curs.execute("SELECT * from people where uid = %s;", data)
			row = curs.fetchone()
			if row == None:
				message = "<p>Message: This person is not registered in the database yet. You can not add them before they register on the main page.</p>"
			else:
				curs.execute("UPDATE people SET people.role = 'Tutor' where people.uid=%s;", data)
				data = (int(fillers[cid]), fillers[cname])
				curs.execute("insert into class (cid, title) values (%s, %s);", data)
				message = "<p>Message: The tutor and class information is added.</p>"
	#print message
	return message

def searchTutor(conn, fillers):
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	tid = fillers['tutor_id']
	curs.execute("SELECT uid, name, role from people where uid = %s;", (tid,))
	row = curs.fetchone()
	if row == None:
		message = '<p>This person is not in the database.'
	elif '{role}'.format(**row) !='Tutor':
		message = 'Student with ID {uid} is called {name}. Please add them as a tutor first.'.format(**row)
	else:
		message = '<p>This tutor is {name}.\n'.format(**row)
		curs.execute("SELECT sid, cid, session_date, length from session where tutor_id = %s;", (tid,))
		row = curs.fetchone()
		while row != None:
			message += '<li>session {sid} for class {cid} was on {session_date} for {length} hours.'.format(**row)
			row = curs.fetchone()
		else:
			message+='<p>There are no more sessions.'
	#print message
	return message

def searchClass(conn, fillers):
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	cid = fillers['class_id']
	curs.execute("SELECT cid, title from class where cid = %s", (cid,))
	row = curs.fetchone()
	if row!=None:
		message = '<li>Class {cid} is {title}'.format(**row)
		curs.execute("SELECT sid, cid, session_date, length from session where cid = %s;", (cid,))
		row = curs.fetchone()
		while row!=None:
			message += '<li>session {sid} for class {cid} was on {session_date} for {length} hours.'.format(**row)
			row = curs.fetchone()
		else:
			message += '<p>There are no more sessions.'
	else:
		message = '<p>The class you are looking for does not exist. Please check again!'
	#print message
	return message

def main(submit, fillers, tutor_list):
	dsn = wendy_dsn.DSN
	dsn['database'] = 'wli2_db'
	conn = dbconn.connect(dsn)
	if submit == 'StoreInfo':
		return  addTutor(conn, fillers, tutor_list)
	elif submit == 'LookupTutor':
		return searchTutor(conn, fillers)
	elif submit == 'LookupClass':
		return searchClass(conn, fillers)

if __name__ == '__main__':
	print main()