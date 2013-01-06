#!/usr/bin/env python
""" mk_all_level1_fsf.py - make fsf files for all subjects

USAGE: python mk_all_level1_fsf.py <name of dataset> <modelnum> <basedir - default is staged> <nonlinear - default=1> <smoothing - default=0> <tasknum - default to all>

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
import glob
from mk_level1_fsf import *
import launch_qsub

import sys

def usage():
    """Print the docstring and exit with error."""
    sys.stdout.write(__doc__)
    sys.exit(2)

def main():

    if len(sys.argv)>2:
        dataset=sys.argv[1]
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

    if not basedir[-1]=='/':
        basedir=basedir+'/'
        
    nonlinear=1
    if len(sys.argv)>4:
        nonlinear=int(sys.argv[4])
        if nonlinear==0:
            print 'using linear registration'


    outfile=open('mk_all_level1_%s.sh'%dataset,'w')

    smoothing=0
    if len(sys.argv)>5:
        smoothing=int(sys.argv[5])
 
    tasknum_spec='task*'
    if len(sys.argv)>6:
        tasknum_spec='task%03d*'%int(sys.argv[6])
 


    use_inplane=1
    dsdir=os.path.join(basedir,dataset)
    
    for root in glob.glob(os.path.join(dsdir,'sub*/BOLD/%s'%tasknum_spec)):
 
        for m in glob.glob(os.path.join(root,'bold_mcf_brain.nii.gz')):
            #print m
            f_split=root.split('/')
            scankey='/'+'/'.join(f_split[1:7])+'/scan_key.txt'
            taskid=f_split[6]
            subnum=int(f_split[7].lstrip('sub'))
            taskinfo=f_split[9].split('_')
            tasknum=int(taskinfo[0].lstrip('task'))

            runnum=int(taskinfo[1].lstrip('run'))
            tr=float(load_scankey(scankey)['TR'])
            # check for inplane
            inplane='/'+'/'.join(f_split[1:8])+'/anatomy/inplane001_brain.nii.gz'
            if os.path.exists(inplane):
                use_inplane=1
            else:
                use_inplane=0
            print 'mk_level1_fsf("%s",%d,%d,%d,%d,%d,"%s",%d)'%(taskid,subnum,tasknum,runnum,smoothing,use_inplane,basedir,modelnum)
            fname=mk_level1_fsf(taskid,subnum,tasknum,runnum,smoothing,use_inplane,basedir,nonlinear,modelnum)
            outfile.write('feat %s\n'%fname)
    outfile.close()

    print 'now launching all feats:'
    print "find %s/sub*/model/*.fsf |sed 's/^/feat /' > run_all_feats.sh; sh run_all_feats.sh"%taskid
    f=open('mk_all_level1_%s.sh'%dataset)
    l=f.readlines()
    f.close()
    njobs=len(l)
    ncores=(njobs/2)*12
    launch_qsub.launch_qsub(script_name='mk_all_level1_%s.sh'%dataset,runtime='04:00:00',jobname='%sl1'%dataset,email=False,parenv='2way',ncores=ncores)


if __name__ == '__main__':
    main()
