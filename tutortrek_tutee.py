#!/usr/local/bin/python2.7

# CS304 Final project
# Wanyi Li
import cgi
import cgitb; cgitb.enable()
import MySQLdb
import dbconn
import wendy_dsn

def addSession(conn, fillers, attedance_list):
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	tutor_data = (int(fillers['uid']),fillers['name'])
	curs.execute('SELECT * FROM people WHERE people.uid = %s;',(int(fillers['uid']),))
	if curs.fetchone() == None:
		print "<p>Message: error: your information is not registered yet.</p>"
	else:
		for i in range(len(attendance_list)):
			if work_list[i] == True:
				cid = 'cid'+str(i)
				date = 'date'+str(i)
				#time = 'time'+str(i)
				tutor = 'tutor'+str(i)
				attendance_data = (int(fillers[cid]), fillers[date], int(fillers[tutor]))			
			    curs.execute('SELECT sid from session (cid, session_date, tutor_id) where cid = %s and session_date = %s \
			    	and tutor_id = (SELECT uid from people where name=%s and role="Tutor");', attendance_data)
			    row = curs.fetchone()
			    if row == None:
			    	print "<p>Message: your session information is invalid. Please check if you have all the correct information."
			    else:
			    	sid = '{sid}'.format(**row)
			    	curs.execute('UPDATE session SET attendance = attendance+1 where sid = %s;', (sid,))
				print "<p>Message: Your attendance information is stored in the database.</p>"


def main(fillers, attendance_list):
	dsn = wendy_dsn.DSN
	dsn['database'] = 'wli2_db'
	conn = dbconn.connect(dsn)
	return addSession(conn,fillers, attendance_list)

if __name__ == '__main__':
	print main()