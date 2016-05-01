#!/usr/local/bin/python2.7

# CS304 Final project
# Wanyi Li
import cgi
import cgitb; cgitb.enable()
import MySQLdb
import dbconn
import wendy_dsn

def addSession(conn, fillers, work_list):
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	tutor_data = (int(fillers['uid']),fillers['name'])
	curs.execute('SELECT uid, name, role FROM people WHERE people.uid = %s;',(int(fillers['uid']),))
	row = curs.fetchone()
	if row == None:
		message = "<p>Message: error: your information is not registered yet.</p>"
	elif '{role}'.format(**row) != 'Tutor':
		message = "<p>Message: errow: you are not a tutor. Please contact admin to add you as a tutor."
	else:
		for i in range(len(work_list)):
			if work_list[i] == True:
				cid = 'cid'+str(i)
				date = 'date'+str(i)
				#time = 'time'+str(i)
				duration = 'duration'+str(i)
				session_data = (int(fillers[cid]), fillers[date], float(fillers[duration]), int(fillers['uid']))			
				curs.execute('INSERT INTO session (cid, session_date, length, tutor_id) values (%s, %s, %s, %s);', session_data)
				message = "<p>Message: Your works sessions are stored in the database.</p>"
	return message

def main(fillers, work_list):
	dsn = wendy_dsn.DSN
	dsn['database'] = 'wli2_db'
	conn = dbconn.connect(dsn)
	return addSession(conn,fillers, work_list)

if __name__ == '__main__':
	print main()