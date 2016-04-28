#!/usr/local/bin/python2.7

# CS304 Final Project TutorTrek(Emma Hower & Wanyi Li)
# Author: Wanyi Li

import sys
import os
import cgi
import cgitb; cgitb.enable()
import cgi_utils_sda
import tutortrek_admin

def main():
  fillers = {}
  fillers['scriptname'] = os.environ['SCRIPT_NAME'] if 'SCRIPT_NAME' in os.environ else ''
  fs = cgi.FieldStorage()
  submit = fs['submit'].value
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
  if 'tutor_id' in fs:
    fillers['tutor_id'] = cgi.escape(fs['tutor_id'].value)
  if 'class_id' in fs:
    fillers['class_id'] = cgi.escape(fs['class_id'].value)


  tutortrek_admin.main(submit, fillers, tutor_list)
  page = cgi_utils_sda.file_contents('tutortrek_admin.html')
  #page = tmpl.format(**fillers)
  return page

if __name__ == '__main__':
  print 'Content-type: text/html\n'
  print main()