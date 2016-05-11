#!/usr/local/bin/python2.7

# CS304 Final Project TutorTrek(Emma Hower & Wanyi Li)
# Author: Wanyi Li

import sys
import os
import cgi
import cgitb; cgitb.enable()
import cgi_utils_sda
import tutortrek_main

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
  print(sesscookie)
  # check to see if there's any session data
  if not os.path.isfile(dir+sessid):
    return {}
  output = open(dir+sessid,'r+')
  # print dir+sessid
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
  print 'Content-type: text/html'
  sess_data = session_start(my_sess_dir)
  print
  sessid = session_id()

  fillers = {}
  fillers['scriptname'] = os.environ['SCRIPT_NAME'] if 'SCRIPT_NAME' in os.environ else ''

  fs = cgi.FieldStorage()
  if fs['submit'].value == 'Register':
    if "name" not in fs or "password" not in fs or "username" not in fs or "password" not in fs:
      message = "<p> Message: Please fill out all the information for registration."
    else:
      fillers['name'] = cgi.escape(fs["name"].value)
      fillers['username'] = cgi.escape(fs["username"].value)
      sess_data['username'] = fillers['username']
      if cgi.escape(fs["password"].value) != cgi.escape(fs["re-password"].value):
        message = "<p> Message: Please retype your password!"
      else:
        message = tutortrek_main.register(fillers, cgi.escape(fs["password"].value))

    fillers['No messages'] = message
    tmpl = cgi_utils_sda.file_contents('tutortrek_main.html')
    page = tmpl.format(**fillers)

  else: #if user clicks 'Log In':
    fillers['username'] = cgi.escape(fs['username'].value)
    sess_data['username'] = fillers['username']
    fillers['choice'] = cgi.escape(fs["choice"].value)

    success, message, role = tutortrek_main.login(fillers['username'], cgi.escape(fs["password"].value), fillers['choice'])
    sess_data['success'] = success
    sess_data['role'] = role
    fillers['No messages'] = message
    if success: 
      if fillers['choice'] == "Tutor":
        tmpl = cgi_utils_sda.file_contents('tutortrek_tutor.html')
        page = tmpl.format(**fillers)
      if fillers['choice'] == "Admin":
        tmpl = cgi_utils_sda.file_contents('tutortrek_admin.html')
        page = tmpl.format(**fillers)
      if fillers['choice'] == "Tutee":
        tmpl = cgi_utils_sda.file_contents('tutortrek_tutee.html')
        page = tmpl.format(**fillers)
    else:
      fillers['No messages'] = message
      tmpl = cgi_utils_sda.file_contents('tutortrek_main.html')
      page = tmpl.format(**fillers)

  print page
  save_session(my_sess_dir,sess_data)

if __name__ == '__main__':
  main()