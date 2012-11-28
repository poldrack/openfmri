#!/usr/bin/env python
"""mk_all_level3_fsf.py - make level 3 fsf files
USAGE: python mk_all_level3_fsf.py <name of dataset> <modelnum>  <basedir - default is pwd> <tasknum -default is all>
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



import os
from openfmri_utils import *
import launch_qsub
from mk_level3_fsf import *

import sys

def usage():
    """Print the docstring and exit with error."""
    sys.stdout.write(__doc__)
    sys.exit(2)

def main():

    if len(sys.argv)>2:
        taskid=sys.argv[1]
        modelnum=int(sys.argv[2])
    else:
        usage()


    if len(sys.argv)>3:
        basedir=sys.argv[3]
        if not os.path.exists(basedir):
            print 'basedir %s does not exist!'%basedir
            sys.exit(1)
    else:
        basedir=os.path.abspath(os.curdir)

    if len(sys.argv)>4:
        tasknum=int(sys.argv[4])
    else:
        tasknum=0


    if not basedir[-1]=='/':
        basedir=basedir+'/'

    if not os.path.exists(os.path.join(basedir,taskid,'group')):
        os.mkdir(os.path.join(basedir,taskid,'group'))
    if not os.path.exists(os.path.join(basedir,taskid,'group/model%03d'%modelnum)):
        os.mkdir(os.path.join(basedir,taskid,'group/model%03d'%modelnum))
        
    featdirs=[]
    subdirs={}


    cond_key=load_condkey(basedir+taskid+'/models/model%03d/condition_key.txt'%modelnum)

    ntasks=len(cond_key)
    print 'found %d tasks'%ntasks

    fsfnames=[]
    if tasknum==0:
        tasks=range(1,ntasks+1)
    else:
        tasks=[tasknum]
        
    for t in tasks:
        f=mk_level3_fsf(taskid,t,modelnum,basedir)
        for i in f:
            fsfnames.append(i)

    outfile=open('run_all_level3_%s.sh'%taskid,'w')
    for f in fsfnames:
          outfile.write('feat %s\n'%f)
    outfile.close()

    print 'now launching using:'
    print 'launch -s run_all_level3_%s.sh -n %sl3 -r 01:00:00'%(taskid,taskid)
    launch_qsub.launch_qsub(script_name='run_all_level3_%s.sh'%taskid,runtime='01:00:00',jobname='%sl3'%taskid,email=False)

      
if __name__ == '__main__':
    main()
