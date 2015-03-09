#!/usr/bin/env python
"""
create a report of all registrations
"""

import os,sys
import glob


try:
    run=int(sys.argv[1])
except:
    run=1

try:
    task=int(sys.argv[2])
except:
    task=1

regpngs=glob.glob('sub*/model/model001/task%03d_run00%d.feat/reg/example_func2standard.png'%(task,run))

f=open('reg_report_run%d.html'%run,'w')
f.write("""<HTML>
  <HEAD>
      <TITLE>Clean markup</TITLE>
        </HEAD>
          <BODY>
          """)
          
for p in regpngs:
    f.write('<h3>%s</h3>\n'%p)
    f.write('<img src="%s" width=800>\n'%p)


f.write("""
  </BODY>
  </HTML>
  """)
f.close()
