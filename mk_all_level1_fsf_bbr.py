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
from mk_level1_fsf_bbr import *
import launch_qsub
import argparse
import sys

def usage():
    """Print the docstring and exit with error."""
    sys.stdout.write(__doc__)
    sys.exit(2)

def parse_command_line():
    parser = argparse.ArgumentParser(description='setup_subject')
    #parser.add_argument('integers', metavar='N', type=int, nargs='+',help='an integer for the accumulator')
    # set up boolean flags


    parser.add_argument('--taskid', dest='taskid',
        required=True,help='Task ID')
    parser.add_argument('--parenv', dest='parenv',
        default='2way',help='Parallel environment')
    parser.add_argument('--tasknum', dest='tasknum',type=int,
        help='Task number')
    parser.add_argument('--basedir', dest='basedir',
        default=os.getcwd(),help='Base directory (above taskid directory)')
    parser.add_argument('--smoothing', dest='smoothing',type=int,
        default=0,help='Smoothing (mm FWHM)')
    parser.add_argument('--use_inplane', dest='use_inplane', type=int,
        default=0,help='Use inplane image')
    parser.add_argument('--nonlinear', dest='nonlinear', action='store_true',
        default=False,help='Use nonlinear regristration')
    parser.add_argument('--test', dest='test', action='store_true',
        default=False,help='Test mode (do not run job)')
    parser.add_argument('--modelnum', dest='modelnum',type=int,
        default=1,help='Model number')
    parser.add_argument('--ncores', dest='ncores',type=int,
        default=6,help='number of cores (ncores * way = 12)')
    
    args = parser.parse_args()
    return args

def main():

    args=parse_command_line()
    print args
    

    smoothing=args.smoothing
    use_inplane=args.use_inplane
    basedir=args.basedir
    nonlinear=args.nonlinear
    modelnum=args.modelnum


    dataset=args.taskid
    
    if not args.test:
        outfile=open('mk_all_level1_%s.sh'%dataset,'w')

 
    tasknum_spec='task*'
    if not args.tasknum==None:
        tasknum_spec='task%03d*'%args.tasknum
 



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

            print 'mk_level1_fsf_bbr("%s",%d,%d,%d,%d,%d,"%s",%d)'%(taskid,subnum,tasknum,runnum,smoothing,use_inplane,basedir,modelnum)
            if not args.test:
                fname=mk_level1_fsf_bbr(taskid,subnum,tasknum,runnum,smoothing,use_inplane,basedir,nonlinear,modelnum)
                outfile.write('feat %s\n'%fname)
    if not args.test:
        outfile.close()

    if not args.test:
        print 'now launching all feats:'
        print "find %s/sub*/model/*.fsf |sed 's/^/feat /' > run_all_feats.sh; sh run_all_feats.sh"%args.taskid
        f=open('mk_all_level1_%s.sh'%dataset)
        l=f.readlines()
        f.close()
        njobs=len(l)
        ncores=(njobs/2)*12
        launch_qsub.launch_qsub(script_name='mk_all_level1_%s.sh'%dataset,runtime='04:00:00',jobname='%sl1'%dataset,email=False,parenv=args.parenv,ncores=args.ncores)


if __name__ == '__main__':
    main()
