#!/usr/local/bin/python2.7

# CS304 Assignment 5
# Wanyi Li
import cgi
import cgitb; cgitb.enable()
import MySQLdb
import dbconn
import wendy_dsn

def addSession(conn, fillers, work_list):
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	actor_data = (int(fillers['uid']),fillers['name'])
	curs.execute('select * from tutor where tutor.uid = %s;',(int(fillers['uid']),))
	if curs.fetchone() != None:
		print "<p>Message: error: actor already in the database.</p>"
	else:
		curs.execute('insert into person (nm, name, birthdate, addedby) values (%s,%s,%s, 1202);', actor_data)
		print "<p>Message: Actor %s is sucessfully added. </p>" %(fillers['actorname'],)

	for i in range(len(work_list)):
		if work_list[i] == True:
			cid = 'cid'+str(i)
			date = 'date'+str(i)
			time = 'time'+str(i)
			duration = 'duration'+str(i)			
		    curs.execute('select tt from movie where movie.title = %s;',(fillers[title],))
			row = curs.fetchone()
			if row == None: # if the movie already not yet exist in the movie table
				if tt not in fillers or title not in fillers:
					print "<p>Message: Movie %s doesn't exist in our database yet. Please fill out all information about this movie.</p>"%(fillers[title],)
				else:
					movie_data = (int(fillers[tt]), fillers[title], int(fillers[release]))
					curs.execute('insert into movie (tt, title, `release`) values (%s, %s, %s);', movie_data)
					print "<p>Message: Movie %s is sucessfully added.</p>" %(fillers[title],)
			else:
				fillers[tt] = row['tt']
			curs.execute('insert into credit (nm, tt) values (%s,%s);', (int(fillers['actornm']),fillers[tt]))
			print "<p>Message: The credential is inserted for movie %s.</p>" %(fillers[title],)


def main(fillers, movie_list):
	dsn = wendy_dsn.DSN
	dsn['database'] = 'wli2_db'
	conn = dbconn.connect(dsn)
	return addSession(conn,fillers, work_list)

if __name__ == '__main__':
	print main()