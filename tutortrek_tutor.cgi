#!/usr/local/bin/python2.7

# CS304 Final Project TutorTrek(Emma Hower & Wanyi Li)
# Author: Wanyi Li

import sys
import os
import cgi
import cgitb; cgitb.enable()
import cgi_utils_sda
import tutortrek_tutor

import Cookie
import pickle
import cgi_utils_sda
 
PY_CGI_SESS_ID='PY_CGI_SESS_ID'   # a constant, the name of the cookie
 
def session_id():
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
     
def session_start(dir):
    '''Intended to mimic the behavior of the PHP function of this name,
except that instead of creating a "superglobal," this will just return
a data structure that can be used in set_session_value and get_session_value.
It takes as an argument the directory to read session data from.'''
    sessid = session_id()
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
 
def save_session(dir,data):
    '''Save the session data to the filesystem.'''
    sessid = session_id()
    output = open(dir+sessid,'w+')
    pickle.dump(data,output,-1)
    output.close()

def main():
  my_sess_dir = '/students/wli2/public_html/sessions/'
  print 'Content-type: text/html '
  sess_data = session_start(my_sess_dir)
  print

  fillers = {}
  fillers['scriptname'] = os.environ['SCRIPT_NAME'] if 'SCRIPT_NAME' in os.environ else ''
  fillers['Message'] = 'You have no new message right now'

  fs = cgi.FieldStorage()

  if 'username' not in sess_data:
    fillers['No messages'] = 'Sorry, you are not logged in. Please log in.'
    tmpl = cgi_utils_sda.file_contents('tutortrek_main.html')
    page = tmpl.format(**fillers)

  else:
    if sess_data['success'] == True and sess_data['role'] == 'Tutor': # only tutor can access this page
      fillers['username'] = sess_data['username']
      tutorname = sess_data['name']
      if 'submit' in fs: # the tutee clicked "Log attendance data"
        if 'cid' in fs and 'date' in fs and 'time' in fs and 'duration' in fs:
          fillers['cid'] = cgi.escape(fs['cid'].value)
          fillers['date'] = cgi.escape(fs['date'].value)
          fillers['time'] = cgi.escape(fs['time'].value)
          fillers['duration'] = cgi.escape(fs['duration'].value)
          fillers['class menu'] = tutortrek_tutor.generateClass(fillers['cid'])
          message = tutortrek_tutor.addSession(fillers)
        else:
          fillers['class menu'] = tutortrek_tutor.generateClass()
          message = "Please fill out all the information." 
      else:
        message = "Welcome to the Tutor page, dear "+ tutorname+ "!"
        fillers['class menu'] = tutortrek_tutor.generateClass()
        
      fillers['No messages'] = message
      tmpl = cgi_utils_sda.file_contents('tutortrek_tutor.html')
      page = tmpl.format(**fillers)
    else:
      fillers['No messages'] = "Please log in first. Thank you!"
      tmpl = cgi_utils_sda.file_contents('tutortrek_main.html')
      page = tmpl.format(**fillers)

  print page    
  save_session(my_sess_dir,sess_data)

if __name__ == '__main__':
  #print 'Content-type: text/html'
  main()