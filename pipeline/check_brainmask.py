#!/usr/bin/env python
""" check_brainmask.py - check skull stripping for all subs in a study
"""


## Copyright 2011, Russell Poldrack. All rights reserved.

## Redistribution and use in source and binary forms, with or without modification, are
## permitted provided that the following conditions are met:

##    1. Redistributions of source code must retain the above copyright notice, this list of
##       conditions and the following disclaimer.

##    2. Redistributions in binary form must reproduce the above copyright notice, this list
##       of conditions and the following disclaimer in the documentation and/or other materials
##       provided with the distribution.

## THIS SOFTWARE IS PROVIDED BY RUSSELL POLDRACK ``AS IS'' AND ANY EXPRESS OR IMPLIED
## WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
## FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL RUSSELL POLDRACK OR
## CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
## CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
## SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
## ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
## NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
## ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import os,sys
from run_shell_cmd import *

dataset=sys.argv[1]
if len(sys.argv)>2:
  basedir=sys.argv[2]
else:
  basedir='/scratch/01329/poldrack/openfmri/staged/'

if not os.path.exists(basedir+dataset):
  print '%s/%s does not exist'%(basedir,dataset)
  sys.exit(2)

if os.path.exists(basedir+dataset+'/brainmask_report'):
    print 'report exists - delete it first'
    sys.exit(0)
else:
    os.mkdir(basedir+dataset+'/brainmask_report')
    
ctr=1

report=open(basedir+dataset+'/brainmask_report/report.html','w')
report.write('<html>\n<body>\n<h1>Brainmask report: %s/%s</h1>'%(basedir,dataset))



for root,dirs,files in os.walk(basedir+dataset):
  if root.find(dataset)>-1:
    for f in files:
        if f.rfind('highres001_brain.nii.gz')>-1:
            cmd='slicer %s/%s -S 4 3200 %s/%s/brainmask_report/tmp_%d.png'%(root,f,basedir,dataset,ctr)
            run_shell_cmd(cmd)
            report.write('<h2>%s/%s\n'%(root,f))
            report.write('<br>\n<img border=0 src=%s/%s/brainmask_report/tmp_%d.png width=100%%>\n<br>\n'%(basedir,dataset,ctr))
            ctr+=1

report.write('</body>\n</html>\n')
report.close()
