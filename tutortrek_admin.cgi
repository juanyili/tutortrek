#!/usr/local/bin/python2.7

# CS304 Final Project TutorTrek(Emma Hower & Wanyi Li)
# Author: Wanyi Li

import sys
import os
import cgi
import cgitb; cgitb.enable()
import cgi_utils_sda
import tutortrek_admin
import tutortrek_utils

import Cookie
import pickle
import cgi_utils_sda
 
PY_CGI_SESS_ID='PY_CGI_SESS_ID'   # a constant, the name of the cookie

def main():
  #generate header
  my_sess_dir = '/students/wli2/public_html/sessions/'
  print 'Content-type: text/html'
  sess_data = tutortrek_utils.session_start(PY_CGI_SESS_ID,my_sess_dir)
  print
  #sessid = session_id()

  fillers = {}
  fillers['scriptname'] = os.environ['SCRIPT_NAME'] if 'SCRIPT_NAME' in os.environ else ''
  fs = cgi.FieldStorage()

  if 'username' not in sess_data:
    fillers['No messages'] = 'Sorry, you are not logged in.'
    tmpl = cgi_utils_sda.file_contents('tutortrek_main.html')
    page = tmpl.format(**fillers)
    print page
  else:
    if sess_data['success'] == True and sess_data['role'] == 'Admin':
      fillers['username'] = sess_data['username'] #this is the admin's username
      adminname = sess_data['name']

      fillers['Tutor List'] = tutortrek_utils.allTutor()
      fillers['Class List'] = tutortrek_utils.allClass()
      message = "Welcome to the Administrator Portal, dear "+adminname+"!"

      if 'submit' in fs:
        submit = fs.getfirst('submit')
        if submit == 'SearchTutorButton':
          keyword = fs.getfirst('search tutor')
          if keyword != None:
            fillers['Tutor List'] = tutortrek_utils.searchTutor(keyword)
        if submit == 'SearchClassButton':
          keyword = fs.getfirst('search tutor')
          if keyword != None:
            fillers['Class List'] = tutortrek_utils.searchClass(keyword)

        if 'tutor_id' in fs and submit == 'LookupTutor':
          fillers['tutor_id'] = fs['tutor_id'].value
          fillers['Tutor List'] = tutortrek_utils.allTutor(fillers['tutor_id'])
          message = tutortrek_admin.lookUpTutor(fillers)

        if 'cid' in fs and submit == 'LookupClass':
          fillers['class_id'] = fs['cid'].value
          fillers['Class List'] = tutortrek_utils.allClass(fillers['class_id'])
          message = tutortrek_admin.lookUpClass(fillers)

        if submit == 'StoreInfo':
          tutor_list = [False, False, False] # keep track of how many tutors are entered
          for i in range(3):
            tid = 'tid'+str(i)
            cid = 'cid'+str(i)
            cname = 'cname'+str(i)
            if tid in fs:
              fillers[tid] = cgi.escape(fs[tid].value)
              tutor_list[i] = True
              if cid in fs and cname in fs:
                fillers[tid] = cgi.escape(fs[tid].value)
                fillers[cid] = cgi.escape(fs[cid].value)
                fillers[cname] = cgi.escape(fs[cname].value)
          message = tutortrek_admin.addTutor(fillers, tutor_list)

      fillers['No messages'] = message
      tmpl = cgi_utils_sda.file_contents('tutortrek_admin.html')
      page = tmpl.format(**fillers)

      if 'submit' in fs and submit == 'Log Out':
          sess_data['success'] = False
          fillers['No messages'] = "You have successfully logged out. Bye bye!"
          tmpl = cgi_utils_sda.file_contents('tutortrek_main.html')
          page = tmpl.format(**fillers)

    else:
      fillers['No messages'] = 'Sorry, you did not have the authorization to use admin page. Please log in as an admin.'
      tmpl = cgi_utils_sda.file_contents('tutortrek_main.html')
      page = tmpl.format(**fillers)

  print page
  tutortrek_utils.save_session(PY_CGI_SESS_ID, my_sess_dir,sess_data)

if __name__ == '__main__':
  main()