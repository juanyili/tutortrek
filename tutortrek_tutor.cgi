#!/usr/local/bin/python2.7

# CS304 Final Project TutorTrek(Emma Hower & Wanyi Li)
# Author: Wanyi Li

import sys
import os
import cgi
import cgitb; cgitb.enable()
import cgi_utils_sda
import tutortrek_tutor

def main():
  fillers = {}
  fillers['scriptname'] = os.environ['SCRIPT_NAME'] if 'SCRIPT_NAME' in os.environ else ''
  fillers['Message'] = 'You have no new message right now'
  fs = cgi.FieldStorage()
  work_list = [False, False, False] # keep track of how many work sessions are entered
  if "uid" not in fs or "name" not in fs: 
    print "Message: Please fill in the following fields if you want to add info into the database."
  else:
    fillers['uid'] = cgi.escape(fs["uid"].value)
    fillers['name'] = cgi.escape(fs["name"].value)
    for i in range(3):
      cid = 'cid'+str(i)
      date = 'date'+str(i)
      time = 'time'+str(i)
      duration = 'duration'+str(i)
      if cid in fs:
        fillers[cid] = cgi.escape(fs[cid].value)
        work_list[i] = True
        if date in fs and time in fs and duration in fs:
          fillers[date] = cgi.escape(fs[date].value)
          fillers[time] = cgi.escape(fs[time].value)
          fillers[duration] = cgi.escape(fs[duration].value)
    message = tutortrek_tutor.main(fillers, work_list)
    fillers['No messages'] = message
  tmpl = cgi_utils_sda.file_contents('tutortrek_tutor.html')
  page = tmpl.format(**fillers)
  return page

if __name__ == '__main__':
  #print_headers(None)
  print 'Content-type: text/html\n'
  print main()