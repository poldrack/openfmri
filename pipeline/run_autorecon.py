#!/usr/bin/env python
""" run_autorecon.py - run freesurfer

USAGE: python run_autorecon.py <taskid> <autorecon level> <basedir> <subdir>

autorecon1: skull stripping
autorecon2/3: full surface reconstruction
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
import sys
import launch_qsub

def usage():
    """Print the docstring and exit with error."""
    sys.stdout.write(__doc__)
    sys.exit(2)

def main():

    artimes=['08:00:00','12:00:00','24:00:00']

    if len(sys.argv)>1:
        dataset=sys.argv[1]
    else:
        usage()
 
    if len(sys.argv)>2:
        arlevel=int(sys.argv[2])
    else:
        arlevel=1
        print 'assuming autorecon 1 (skullstrip)'

    if len(sys.argv)>3:
        basedir=sys.argv[3]
        if not os.path.exists(basedir):
            print 'basedir %s does not exist!'%basedir
            sys.exit(1)
    else:
        basedir='/corral-repl/utexas/poldracklab/openfmri/staged/'

    if len(sys.argv)>4:
        subdir=sys.argv[4]
        if not os.path.exists(basedir):
            print 'basedir %s does not exist!'%basedir
            sys.exit(1)
    else:
        subdir='/corral-repl/utexas/poldracklab/openfmri/subdir/'
        print 'assuming subdir: %s'%subdir
 

    outfile=open('run_autorecon%d_%s.sh'%(arlevel,dataset),'w')
    cmdctr=0
    for d in os.listdir(os.path.join(basedir,dataset)):
        if d[0:3]=='sub':
            for m in os.listdir('%s/%s/anatomy/'%(os.path.join(basedir,dataset),d)):
                if m=='highres001.nii.gz':
                    subnum=int(d.replace('sub',''))
                    outfile.write('recon-all -autorecon%d -subjid %s_sub%03d -sd %s\n'%(arlevel,dataset,subnum,subdir))
                    cmdctr+=1

    outfile.close()


    print 'now launch using:'
    print 'launch -s run_autorecon%d_%s.sh -n %sar%d -r %s'%(arlevel,dataset,dataset,arlevel,artimes[arlevel-1])
    launch_qsub.launch_qsub(script_name='run_autorecon%d_%s.sh'%(arlevel,dataset),runtime=artimes[arlevel-1],jobname='%sar%d'%(dataset,arlevel),email=False,parenv='1way',ncores=cmdctr*12)


if __name__ == '__main__':
    main()
