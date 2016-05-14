#!/usr/local/bin/python2.7

# CS304 Final Project TutorTrek(Emma Hower & Wanyi Li)
# Author: Wanyi Li

import sys
import os
import cgi
import cgitb; cgitb.enable()
import cgi_utils_sda
import tutortrek_main
import tutortrek_utils

import Cookie
import pickle
import cgi_utils_sda
 
PY_CGI_SESS_ID='PY_CGI_SESS_ID'   # a constant, the name of the cookie

def main():
  my_sess_dir = '/students/wli2/public_html/sessions/'
  print 'Content-type: text/html'
  sess_data = tutortrek_utils.session_start(PY_CGI_SESS_ID, my_sess_dir)
  print

  fillers = {}
  fillers['scriptname'] = os.environ['SCRIPT_NAME'] if 'SCRIPT_NAME' in os.environ else ''

  fs = cgi.FieldStorage()
  if 'submit' not in fs: # if the user is just loading the page
    fillers['No messages'] = "Welcome to TutorTrek!"
    tmpl = cgi_utils_sda.file_contents('tutortrek_main.html')
    page = tmpl.format(**fillers)
  else:
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

    else:  # if the user clicks 'Log In':
      if 'username' in fs and 'choice' in fs:
        fillers['username'] = cgi.escape(fs['username'].value)
        sess_data['username'] = fillers['username']
        fillers['choice'] = cgi.escape(fs["choice"].value)

        success, message, role, name = tutortrek_main.login(fillers['username'], cgi.escape(fs["password"].value), fillers['choice'])
        sess_data['success'] = success
        sess_data['role'] = role
        sess_data['name'] = name
        fillers['No messages'] = message
        if success: 
          if fillers['choice'] == "Tutor":
            page = cgi_utils_sda.file_contents('tutor_initial.html')
            #page = tmpl.format(**fillers)
          if fillers['choice'] == "Admin":
            page = cgi_utils_sda.file_contents('admin_initial.html')
            #page = tmpl.format(**fillers)
          if fillers['choice'] == "Tutee":
            page = cgi_utils_sda.file_contents('tutee_initial.html')
            #page = tmpl.format(**fillers)
        else:
          fillers['No messages'] = message
          tmpl = cgi_utils_sda.file_contents('tutortrek_main.html')
          page = tmpl.format(**fillers)
      else:
        fillers['No messages'] = "Please log in with the role you want to choose."
        tmpl = cgi_utils_sda.file_contents('tutortrek_main.html')
        page = tmpl.format(**fillers)

  print page
  tutortrek_utils.save_session(PY_CGI_SESS_ID, my_sess_dir,sess_data)

if __name__ == '__main__':
  main()