#!/usr/bin/env python
""" run_betfunc.py - run bet on functional images

USAGE: python run_betfnc.py <name of dataset> <basedir - default is staged> <mcf process to wait on - default is none>

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


import os,glob
import sys
import launch_qsub

def main():

    if len(sys.argv)>1:
        ds=sys.argv[1]
    else:
        usage()

    if len(sys.argv)>2:
        basedir=sys.argv[2]
        if not os.path.exists(basedir):
            print 'basedir %s does not exist!'%basedir
            sys.exit(1)
    else:

        basedir='/scratch/01329/poldrack/openfmri/staged/'
    if len(sys.argv)>3:
        wait_process=int(sys.argv[3])
    else:
        wait_process=[]
    
    outfile=open('run_betfunc_%s.sh'%ds,'w')
    found_files=0
    dsdir=os.path.join(basedir,ds)
    for d in glob.glob(os.path.join(dsdir,'sub*/BOLD/*/bold.nii.gz')):
                    outfile.write('bet %s %s -F\n'%(d.replace('.nii','_mcf.nii'),d.replace('.nii','_mcf_brain.nii')))
                    found_files=1
    outfile.close()

    if found_files>0:
        print 'now launching using:'
        print 'launch -s run_betfunc_%s.sh -n betfunc -r 00:10:00'%ds

        launch_qsub.launch_qsub(script_name='run_betfunc_%s.sh'%ds,runtime='00:10:00',jobname='%sbf'%ds,email=False,hold=wait_process)
    else:
        print 'no files found to process'


if __name__ == '__main__':
    main()
