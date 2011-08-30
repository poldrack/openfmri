#!/usr/bin/env python
""" mk_all_level2_fsf.py - make level 2 fsf files for all subjects in a dataset
USAGE: python mk_all_level2_fsf.py <name of dataset>  <basedir - default is staged>

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
from mk_level2_fsf import *

import sys
import launch_qsub

def usage():
    """Print the docstring and exit with error."""
    sys.stdout.write(__doc__)
    sys.exit(2)

def main():

    if len(sys.argv)>1:
        taskid=sys.argv[1]
    else:
        usage()


    if len(sys.argv)>2:
        basedir=sys.argv[2]
        if not os.path.exists(basedir):
            print 'basedir %s does not exist!'%basedir
            sys.exit(1)
    else:
        basedir='/scratch/01329/poldrack/openfmri/staged/'


    outfile=open('run_all_level2_%s.sh'%taskid,'w')

    featdirs=[]
    subdirs={}

    
    for d in os.listdir(basedir+taskid):
        if d[0:3]=='sub':
            for m in os.listdir('%s/%s/model/'%(basedir+taskid,d)):
                if m[-5:]=='.feat':
                    featdirs.append(m)
                    fs=featdirs[-1]
                    subnum=int(d.replace('sub',''))
                    if not subdirs.has_key(subnum):
                        subdirs[subnum]={}
                    runnum=int(fs.split('_')[1].split('.')[0].replace('run',''))
                    tasknum=int(fs.split('_')[0].replace('task',''))
                    if not subdirs[subnum].has_key(tasknum):
                        subdirs[subnum][tasknum]=[]
                    subdirs[subnum][tasknum].append(runnum)

    for s in subdirs.iterkeys():
              for t in subdirs[s].iterkeys():
                fname=mk_level2_fsf(taskid,s,t,subdirs[s][t],basedir)
                outfile.write('feat %s\n'%fname)
                
    outfile.close()

    print 'now launching using:'
    print 'launch -s run_all_level2_%s.sh -n %sl2 -r 02:00:00'%(taskid,taskid)
    launch_qsub.launch_qsub(script_name='run_all_level2_%s.sh'%taskid,runtime='02:00:00',jobname='%sl2'%taskid,email=False)

if __name__ == '__main__':
    main()
