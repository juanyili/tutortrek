#!/usr/local/bin/python2.7

# CS304 Final Project TutorTrek(Emma Hower & Wanyi Li)
# Author: Wanyi Li

import sys
import os
import cgi
import cgitb; cgitb.enable()
import cgi_utils_sda
import tutortrek_tutor
import tutortrek_utils

import Cookie
import pickle

PY_CGI_SESS_ID = 'PY_CGI_SESS_ID'   # a constant, the name of the cookie

def main():
  my_sess_dir = '/students/wli2/public_html/sessions/'
  print 'Content-type: text/html '
  sess_data = tutortrek_utils.session_start(PY_CGI_SESS_ID, my_sess_dir)
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
      fillers['navigation'] = "<nav><table id='menu'><tr><th><a href='tutortrek_main.cgi'>Registration Page</a></th><th><a href='tutortrek_tutor.cgi'>Tutor Page</a></th><th><a href='tutortrek_tutee.cgi'>Tutee Page</a></th></tr></table></nav>"
      tutorname = sess_data['name']
      if 'submit' in fs:
        message = "Please fill out all the information." 
        if fs.getfirst('submit') == 'Search Class':
          keyword = fs.getfirst('class')
          if keyword == None:
            fillers['class menu'] = tutortrek_utils.allClass()
          else:
            fillers['class menu'] = tutortrek_utils.searchClass(keyword)

        if fs.getfirst('submit') == 'Log Work Data':
          if 'cid' in fs and 'date' in fs and 'time' in fs and 'duration' in fs:
            fillers['cid'] = cgi.escape(fs['cid'].value)
            fillers['date'] = cgi.escape(fs['date'].value)
            fillers['time'] = cgi.escape(fs['time'].value)
            fillers['duration'] = cgi.escape(fs['duration'].value)
            fillers['class menu'] = tutortrek_utils.allClass(fillers['cid'])
            message = tutortrek_tutor.addSession(fillers)
          else:       
            fillers['class menu'] = tutortrek_utils.allClass()
      else:
        message = "Welcome to the Tutor page, dear "+ tutorname+ "!"
        fillers['class menu'] = tutortrek_utils.allClass()
        
      fillers['No messages'] = message
      tmpl = cgi_utils_sda.file_contents('tutortrek_tutor.html')
      page = tmpl.format(**fillers)

      if 'submit' in fs and fs.getfirst('submit') == 'Log Out':
          sess_data['success'] = False
          fillers['No messages'] = "You have successfully logged out. Bye bye!"
          tmpl = cgi_utils_sda.file_contents('tutortrek_main.html')
          page = tmpl.format(**fillers)
          
    else:
      fillers['No messages'] = "Please log in first. Thank you!"
      tmpl = cgi_utils_sda.file_contents('tutortrek_main.html')
      page = tmpl.format(**fillers)

  print page    
  tutortrek_utils.save_session(PY_CGI_SESS_ID, my_sess_dir,sess_data)

if __name__ == '__main__':
  #print 'Content-type: text/html'
  main()