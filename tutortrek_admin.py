#!/usr/local/bin/python2.7

# CS304 Assignment 5
# Wanyi Li
import cgi
import cgitb; cgitb.enable()
import MySQLdb
import dbconn
import wendy_dsn

def addTutor(conn, fillers, tutor_list):
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	for i in range(len(tutor_list)):
		if tutor_list[i] == True:
			tid = 'tid'+str(i)
			cid = 'cid'+str(i)
			cname = 'cname'+str(i)
			data = (int(fillers[tid]),)			
			curs.execute("insert into tutor (tutor_id) values (%s);", data)
			data = (int(fillers[cid]), fillers[cname])
			curs.execute("insert into class (class_id, title) values (%s, %s);", data)
			print "<p>Message: The tutor and class information is added.</p>"

def searchTutor(conn, fillers):
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	tid = fillers['tutor_id']
	curs.execute("select * from tutor where tutor_id = %s;", (tid,))
	row =  curs.fetchone()
	print row

def searchClass(conn, fillers):
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	cid = fillers['class_id']
	curs.execute("select * from class where class_id = %s", (cid,))
	row =  curs.fetchone()
	print row	

def main(submit, fillers, tutor_list):
	dsn = wendy_dsn.DSN
	dsn['database'] = 'wli2_db'
	conn = dbconn.connect(dsn)
	if submit == 'StoreInfo':
		return addTutor(conn, fillers, tutor_list)
	elif submit == 'LookupTutor':
		return searchTutor(conn, fillers)
	elif submit == 'LookupClass':
		return searchClass(conn, fillers)

if __name__ == '__main__':
	print main()