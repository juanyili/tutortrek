#!/usr/local/bin/python2.7

# CS304 Final Project TutorTrek(Emma Howey & Wanyi Li)
# Author: Wanyi Li

import sys
import os
import cgi
import cgitb; cgitb.enable()
import cgi_utils_sda
import tutortrek_tutee
import tutortrek_utils

import Cookie
import pickle
import cgi_utils_sda
 
PY_CGI_SESS_ID='PY_CGI_SESS_ID'   # a constant, the name of the cookie

def main():
  # generate header
  my_sess_dir = '/students/wli2/public_html/sessions/'
  print 'Content-type: text/html '
  sess_data = tutortrek_utils.session_start(PY_CGI_SESS_ID,my_sess_dir)
  print
  #sessid = session_id()

  fillers = {}
  fillers['scriptname'] = os.environ['SCRIPT_NAME'] if 'SCRIPT_NAME' in os.environ else ''
  fs = cgi.FieldStorage()

  # check if username is already in the session data or not
  if 'username' not in sess_data:
    fillers['No messages'] = 'Sorry, you are not logged in. Please log in.'
    tmpl = cgi_utils_sda.file_contents('tutortrek_main.html')
    page = tmpl.format(**fillers)
  else:
    if sess_data['success'] == True and sess_data['role'] != 'Admin': #any tutor or tutee can use the tutee page
      fillers['username'] = sess_data['username'] #this is the tutee's username
      tuteename = sess_data['name']
      message = "Welcome to the Tutee page, dear "+ tuteename+ "!"
      # generate default dropdown menus
      fillers['class menu'] = tutortrek_utils.allClass()
      fillers['rating menu'] = '<select name ="rating"><option selected disabled>You have not chosen a session yet</option></select>'
      fillers['session menu'] = '<select name ="session"><option selected disabled>You have not chosen a class yet</option></select>'
      #generate navigation bar depending onthe role of the user.
      if sess_data['role'] == 'Tutor':
        fillers['navigation'] = "<nav><table id='menu'><tr><th><a href='tutortrek_main.cgi'>Registration Page</a></th><th><a href='tutortrek_tutor.cgi'>Tutor Page</a></th><th><a href='tutortrek_tutee.cgi'>Tutee Page</a></th></tr></table></nav>"
      else:
        fillers['navigation'] = "<nav><table id='menu'><tr><th><a href='tutortrek_main.cgi'>Registration Page</a></th><th><a href='tutortrek_tutee.cgi'>Tutee Page</a></th></tr></table></nav>"
      
      if 'submit' in fs:
        message = "Please fill out all the information."
        submit = fs.getfirst('submit')

        if submit == "Search Class Title" and 'search title' in fs:
          fillers['class menu'] = tutortrek_utils.searchClass(cgi.escape(fs.getfirst('search title')))
          fillers['rating menu'] = '<select name ="rating"><option selected disabled>You have not chosen a session yet</option></select>'
          fillers['session menu'] = '<select name ="session"><option selected disabled>You have not chosen a class yet</option></select>'

        if submit == "Choose Class" and 'cid' in fs:
          fillers['session menu'] = tutortrek_tutee.generateSession(fs.getfirst('cid'))
          fillers['rating menu'] = '<select name ="rating"><option selected disabled>You have not chosen a session yet</option></select>'
          fillers['class menu'] = tutortrek_utils.allClass(fs.getfirst('cid'))

        if submit == 'Attend' and 'sid' in fs and 'cid' in fs:
          fillers['class menu'] = tutortrek_utils.allClass(fs.getfirst('cid'))
          fillers['session menu'] = tutortrek_tutee.generateSession(fs.getfirst('cid'), fs.getfirst('sid'))
          fillers['rating menu'] = '<select name ="rating"><option value="3">Great!</option><option value="2">Okay</option><option value="1">Bad</option></select>'
          message += tutortrek_tutee.logAttendance(fs.getfirst('sid'))

        if submit == 'Rate this session' and 'sid' in fs and 'cid' in fs and 'rating' in fs:
          rating = fs['rating'].value
          sid = fs['sid'].value
          fillers['class menu'] = tutortrek_utils.allClass(fs.getfirst('cid'))
          fillers['session menu'] = tutortrek_tutee.generateSession(fs.getfirst('cid'), fs.getfirst('sid'))
          if 'rating' == 3:
            fillers['rating menu'] = '<select name ="rating"><option selected value="3">Great!</option><option value="2">Okay</option><option value="1">Bad</option></select>'
          if 'rating' == 2:
            fillers['rating menu'] = '<select name ="rating"><option value="3">Great!</option><option selected value="2">Okay</option><option value="1">Bad</option></select>'
          if 'rating' == 1:
            fillers['rating menu'] = '<select name ="rating"><option value="3">Great!</option><option value="2">Okay</option><option selected value="1">Bad</option></select>'
          message += tutortrek_tutee.rateSession(fs.getfirst('sid'), fs.getfirst('rating'), sess_data['username'])

      fillers['No messages'] = message
      tmpl = cgi_utils_sda.file_contents('tutortrek_tutee.html')
      page = tmpl.format(**fillers)

      if 'submit' in fs and submit == 'Log Out':
          sess_data['success'] = False
          fillers['No messages'] = "You have successfully logged out. Bye bye!"
          tmpl = cgi_utils_sda.file_contents('tutortrek_main.html')
          page = tmpl.format(**fillers)

    else:
      fillers['No messages'] = 'Sorry, you did not have the authorization to use tutee page. Please log in as an tutee.'
      tmpl = cgi_utils_sda.file_contents('tutortrek_main.html')
      page = tmpl.format(**fillers)

  print page
  tutortrek_utils.save_session(PY_CGI_SESS_ID, my_sess_dir,sess_data)

if __name__ == '__main__':
  print main()