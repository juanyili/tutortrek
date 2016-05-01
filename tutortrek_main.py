#!/usr/local/bin/python2.7

# CS304 Assignment 5
# Wanyi Li
import cgi
import cgitb; cgitb.enable()
import MySQLdb
import dbconn
import wendy_dsn

def register(conn, fillers):
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	data = (fillers['name'], fillers['username'])
	curs.execute("insert into people (name, username, role) values (%s, %s, 'Tutee');", data)
	curs.execute("select uid from people where username = %s;", (fillers['username']))
	row = curs.fetchone()
	print "<p>Message: Your info is registered. Your role is currently a tutee. If you are a tutor, please contact admin to add you. Your ID is ", row

def main(fillers):
	dsn = wendy_dsn.DSN
	dsn['database'] = 'wli2_db'
	conn = dbconn.connect(dsn)
	return register(conn, fillers)

if __name__ == '__main__':
	print main()