#!/usr/local/bin/python2.7

# CS304 Final Project TutorTrek(Emma Howey & Wanyi Li)
# Author: Wanyi Li

import sys
import os
import cgi
import cgitb; cgitb.enable()
import cgi_utils_sda
import tutortrek_tutee

def main():
  fillers = {}
  fillers['scriptname'] = os.environ['SCRIPT_NAME'] if 'SCRIPT_NAME' in os.environ else ''
  #fillers['message section'] = "AHHHHHHHHHH"
  fs = cgi.FieldStorage()
  attendance_list = [False, False, False] # keep track of how many work sessions are entered
  if "uid" not in fs or "name" not in fs: 
    print "Message: Please fill in the following fields if you want to add info into the database."
  else:
    fillers['uid'] = cgi.escape(fs["uid"].value)
    fillers['name'] = cgi.escape(fs["name"].value)
    for i in range(3):
      cid = 'cid'+str(i)
      date = 'date'+str(i)
      time = 'time'+str(i)
      tutor = 'tutor'+str(i)
      rating = 'rating'+str(i)
      if cid in fs:
        fillers[cid] = cgi.escape(fs[cid].value)
        attendance_list[i] = True
        if date in fs and time in fs and tutor in fsand rating in fs:
          fillers[date] = cgi.escape(fs[date].value)
          fillers[time] = cgi.escape(fs[time].value)
          fillers[tutor] = cgi.escape(fs[tutor].value)
          fillers[rating] = cgi.escape(fs[rating].value)
    tutortrek.main(fillers, attendance_list)
  tmpl = cgi_utils_sda.file_contents('tutortrek.html')
  page = tmpl.format(**fillers)
  return page

if __name__ == '__main__':
  print_headers(None)
  print 'Content-type: text/html\n'
  print main()