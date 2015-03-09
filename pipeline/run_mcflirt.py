#!/usr/bin/env python
""" run_mcflirt.py - run mcflirt on all data

USAGE: python run_mcflirt.py <name of dataset> <basedir - default is staged>
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

def usage():
    """Print the docstring and exit with error."""
    sys.stdout.write(__doc__)
    sys.exit(2)

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
        basedir='/corral-repl/utexas/poldracklab/openfmri/staged/'
        
    outfile=open('run_mcflirt_%s.sh'%ds,'w')

    boldfiles=glob.glob(os.path.join(basedir,ds,'sub*/BOLD/*/bold.nii.gz'))
    if len(boldfiles)==0:
        print 'no bold files found!'
        return
    
    for d in boldfiles:
        outfile.write('mcflirt -in %s -sinc_final -plots\n'%d)

    outfile.close()


    print 'now launching using:'
    print 'launch -s run_mcflirt_%s.sh -n mcflirt -r 00:30:00'%ds
    #launch_qsub.launch_qsub(script_name='run_mcflirt_%s.sh'%ds,runtime='00:30:00',jobname='%smcf'%ds,projname='Analysis_Lonestar',email=False)
    launch_qsub.launch_qsub(script_name='run_mcflirt_%s.sh'%ds,runtime='00:30:00',jobname='%smcf'%ds,email=False)


if __name__ == '__main__':
    main()
