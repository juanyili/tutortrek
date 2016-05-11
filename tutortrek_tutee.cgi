#!/usr/local/bin/python2.7

# CS304 Final Project TutorTrek(Emma Howey & Wanyi Li)
# Author: Wanyi Li

import sys
import os
import cgi
import cgitb; cgitb.enable()
import cgi_utils_sda
import tutortrek_tutee

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
  sessid = session_id()

  fillers = {}
  fillers['scriptname'] = os.environ['SCRIPT_NAME'] if 'SCRIPT_NAME' in os.environ else ''
  fs = cgi.FieldStorage()

  if 'username' not in sess_data:
    fillers['No messages'] = 'Sorry, you are not logged in. Please log in.'
    tmpl = cgi_utils_sda.file_contents('tutortrek_main.html')
    page = tmpl.format(**fillers)
  else:
    if sess_data['success'] == True and sess_data['role'] != 'Admin': #any tutor or tutee can use the tutee page
      fillers['username'] = sess_data['username'] #this is the tutee's username
      tuteename = sess_data['name']
      if 'submit' in fs:
        message = "Please fill out all the information."
        submit = fs['submit'].value
        if submit == "Search Class Title" and 'search title' in fs:
          fillers['class menu'] = tutortrek_tutee.searchClass(cgi.escape(fs['search title'].value))
          fillers['rating menu'] = '<select name ="rating"><option selected disabled>You have not chosen a session yet</option></select>'
          fillers['session menu'] = '<select name ="session"><option selected disabled>You have not chosen a class yet</option></select>'

        if submit == "Choose Class" and 'cid' in fs:
          fillers['session menu'] = tutortrek_tutee.generateSession(fs['cid'].value)
          fillers['rating menu'] = '<select name ="rating"><option selected disabled>You have not chosen a session yet</option></select>'
          fillers['class menu'] = tutortrek_tutee.allClass(fs['cid'].value)

        if submit == 'Attend' and 'sid' in fs and 'cid' in fs:
          fillers['class menu'] = tutortrek_tutee.allClass(fs['cid'].value)
          fillers['session menu'] = tutortrek_tutee.generateSession(fs['cid'].value, fs['sid'].value)
          fillers['rating menu'] = '<select name ="rating"><option value="3">Great!</option><option value="2">Okay</option><option value="1">Bad</option></select>'
          message += tutortrek_tutee.logAttendance(fs['sid'].value)

        if submit == 'Rate this session' and 'sid' in fs and 'cid' in fs and 'rating' in fs:
          rating = fs['rating'].value
          sid = fs['sid'].value
          fillers['class menu'] = tutortrek_tutee.allClass(fs['cid'].value)
          fillers['session menu'] = tutortrek_tutee.generateSession(fs['cid'].value, fs['sid'].value)
          if 'rating' == 3:
            fillers['rating menu'] = '<select name ="rating"><option selected value="3">Great!</option><option value="2">Okay</option><option value="1">Bad</option></select>'
          if 'rating' == 2:
            fillers['rating menu'] = '<select name ="rating"><option value="3">Great!</option><option selected value="2">Okay</option><option value="1">Bad</option></select>'
          if 'rating' == 1:
            fillers['rating menu'] = '<select name ="rating"><option value="3">Great!</option><option value="2">Okay</option><option selected value="1">Bad</option></select>'
          message += tutortrek_tutee.rateSession(fs['sid'].value, fs['rating'].value, sess_data['username'])

        # ################################################
        # if submit == 'Log Attedance Date':
        #   if 'cid' in fs and 'date' in fs and 'tutor' in fs and 'rating' in fs:
        #     fillers['cid'] = cgi.escape(fs['cid'].value)
        #     fillers['date'] = cgi.escape(fs['date'].value)
        #     fillers['tutor'] = cgi.escape(fs['tutor'].value)
        #     fillers['rating'] = cgi.escape(fs['rating'].value)
        #     message = tutortrek_tutee.addSession(fillers)
        #   else:
        #     message = "Please fill out all the information."
        ################################################

      else:
        message = "Welcome to the Tutee page, dear "+ tuteename+ "!"
        fillers['class menu'] = tutortrek_tutee.allClass()
        fillers['rating menu'] = '<select name ="rating"><option selected disabled>You have not chosen a session yet</option></select>'
        fillers['session menu'] = '<select name ="session"><option selected disabled>You have not chosen a class yet</option></select>'

      fillers['No messages'] = message
      tmpl = cgi_utils_sda.file_contents('tutortrek_tutee.html')
      page = tmpl.format(**fillers)

    else:
      fillers['No messages'] = 'Sorry, you did not have the authorization to use tutee page. Please log in as an tutee.'
      tmpl = cgi_utils_sda.file_contents('tutortrek_main.html')
      page = tmpl.format(**fillers)

  print page
  save_session(my_sess_dir,sess_data)

if __name__ == '__main__':
  print main()