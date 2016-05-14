#!/usr/local/bin/python2.7

# CS304 Final project
# Wanyi Li

############################################
# This is a module that provides helper methods 
# for other python modules in tutortrek.
############################################
import sys
import os
import cgi
import cgitb; cgitb.enable()
import cgi_utils_sda
import MySQLdb
import dbconn
import wendy_dsn

import Cookie
import pickle

 

def session_id(PY_CGI_SESS_ID):
    '''Intended to mimic the behavior of the PHP function of this name'''
    
    sesscookie = cgi_utils_sda.getCookieFromRequest(PY_CGI_SESS_ID)
    if sesscookie == None:
        sessid = cgi_utils_sda.unique_id()
        if sessid == None:
            print("I give up; couldn't create a session. No session id")
            return
    else:
        sessid=sesscookie.value   # get value out of morsel
    return sessid
     
def session_start(PY_CGI_SESS_ID,dir):
    '''Intended to mimic the behavior of the PHP function of this name,
except that instead of creating a "superglobal," this will just return
a data structure that can be used in set_session_value and get_session_value.
It takes as an argument the directory to read session data from.'''
    sessid = session_id(PY_CGI_SESS_ID)
    # Set a cookie and print that header
    sesscookie = Cookie.SimpleCookie()
    cgi_utils_sda.setCookie(sesscookie,PY_CGI_SESS_ID,sessid)
    print sesscookie
    # check to see if there's any session data
    if not os.path.isfile(dir+sessid):
        return {}
    output = open(dir+sessid,'r+')
    # session already exists, so load saved data
    # rb for read binary
    input = open(dir+sessid,'r')
    sess_data = pickle.load(input)
    input.close()
    if isinstance(sess_data,dict):
        return sess_data
    else:
        raise Exception ("Possibly corrupted session data; not a dictionary: "
                         +sess_data)
        return
 
def save_session(PY_CGI_SESS_ID, dir,data):
    '''Save the session data to the filesystem.'''
    sessid = session_id(PY_CGI_SESS_ID)
    output = open(dir+sessid,'w+')
    pickle.dump(data,output,-1)
    output.close()

#############################################
# This method generates a dropdown menu
# of all the classes in the database.
# 'chosen' is the input for class ID (cid).
# If 'chosen' is not None, then the selector
# will select the 'chosen' option. This is used
# when user clicks on a class, the dropdown menu
# should autimatically stay at the option that the
# user has chosen.
###########################################
def allClass(chosen=None):
	conn = connect()
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	menu = "<select name ='cid'><option selected disabled>Class List</option>"
	if chosen == None:
		curs.execute('SELECT cid, title FROM class;')
		row = curs.fetchone()
		while row != None:
			menu+="<option value={cid}>{title}</option>".format(**row)
			row = curs.fetchone()
	else:
		curs.execute('SELECT cid, title FROM class;')
		row = curs.fetchone()
		while row != None:
			if '{cid}'.format(**row) == chosen:
				menu+="<option selected value={cid}>{title}</option>".format(**row)
			else:
				menu+="<option value={cid}>{title}</option>".format(**row)
			row = curs.fetchone()
	menu+="</select>"
	return menu


############################################
# This method generates a dropdown menu
# of all the tutors in the database.
# 'chosen' is the input for tutor username (tutor_id).
# If 'chosen' is not None, then the selector
# will select the 'chosen' option. This is used
# when user clicks on a tutor, the dropdown menu
# should autimatically stay at the option that the
# user has chosen.
############################################
def allTutor(chosen=None):
	conn = connect()
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	menu = "<select name ='tutor_id'><option selected disabled>Tutors List</option>"
	if chosen == None:
		curs.execute('SELECT username, name FROM people where role = "Tutor";')
		row = curs.fetchone()
		while row != None:
			menu+="<option value={username}>{name}</option>".format(**row)
			row = curs.fetchone()
	else:
		curs.execute('SELECT username, name FROM people where role = "Tutor";')
		row = curs.fetchone()
		while row != None:
			if '{username}'.format(**row) == chosen:
				menu+="<option selected value={username}>{name}</option>".format(**row)
			else:
				menu+="<option value={username}>{name}</option>".format(**row)
			row = curs.fetchone()
	menu+="</select>"
	return menu

############################################
# This method generates a dropdown menu
# of the classes of which the titles match the
# search queary 'search' in the database.
# For example, a user searches 'data', then
# the drop down menu returns two options: 'data
# science' and 'databases'.
###########################################
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

############################################
# This modules generates a dropdown menu
# of the tutors of which the titles match the
# search queary 'search' in the database.
# For example, a user searches 'Emma', then 
# the drop down menu returns 'Emma'.
###########################################
def searchTutor(search):
	conn = connect()
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	menu = "<select name ='tutor_id'><option selected disabled>Tutors List</option>"
	curs.execute("SELECT username, name FROM people where role = 'Tutor' and name like %s;", ('%'+search+'%',))
	row = curs.fetchone()
	if row == None:
		menu = allTutor()
	else:
		while row!= None:
			menu+="<option value={username}>{name}</option>".format(**row)
			row = curs.fetchone()
	menu += "</select>"
	return menu

######################################
# This is a helper method that uses the DSN
# file to connect to the database and return
# the conntection to the database.
######################################
def connect():
	dsn = wendy_dsn.DSN
	dsn['database'] = 'wli2_db'
	conn = dbconn.connect(dsn)
	return conn