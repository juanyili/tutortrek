#!/usr/local/bin/python2.7

# CS304 Final Project TutorTrek(Emma Hower & Wanyi Li)
# Author: Wanyi Li

import sys
import os
import cgi
import cgitb; cgitb.enable()
import cgi_utils_sda
import tutortrek_admin

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
    #print dir+sessid
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
  submit = fs['submit'].value

  if 'username' not in sess_data:
    fillers['No messages'] = 'Sorry, you are not logged in.'
    tmpl = cgi_utils_sda.file_contents('tutortrek_main.html')
    page = tmpl.format(**fillers)
    print page
  else:
    if sess_data['success'] == True and sess_data['role'] == 'Admin':
      fillers['username'] = sess_data['username'] #this is the admin's username
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

      if 'tutor_id' in fs and submit == 'LookupTutor':
        fillers['tutor_id'] = cgi.escape(fs['tutor_id'].value)
        message = tutortrek_admin.searchTutor(fillers)

      if 'class_id' in fs and submit == 'LookupClass':
        fillers['class_id'] = cgi.escape(fs['class_id'].value)
        message = tutortrek_admin.searchClass(fillers)

      fillers['No messages'] = message
      tmpl = cgi_utils_sda.file_contents('tutortrek_admin.html')
      page = tmpl.format(**fillers)
      print page

    else:
      fillers['No messages'] = 'Sorry, you did not have the authorization to use admin page. Please log in as an admin.'
      tmpl = cgi_utils_sda.file_contents('tutortrek_main.html')
      page = tmpl.format(**fillers)
      print page

  save_session(my_sess_dir,sess_data)


if __name__ == '__main__':
  main()