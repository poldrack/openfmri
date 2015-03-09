#!/usr/bin/env python
"""
make a report for a smoothed group analysis

"""

import os,sys
import glob
import numpy
import argparse
from run_shell_cmd import *

def parse_command_line():
    parser = argparse.ArgumentParser(description='run_smoothed_group_stats')
    parser.add_argument('-b','--basedir', dest='basedir',
        help='base directory for data file', default='/corral-repl/utexas/poldracklab/openfmri/shared2')
    parser.add_argument('--taskid', dest='taskid',
        help='name of study/studies to be analyzed')
    parser.add_argument('--modelnum', dest='modelnum',type=int,
        default=1,help='Model number')
    parser.add_argument('-i','--bgimg', dest='bgimg',
        help='bg image for rendering', default='/corral-repl/utexas/poldracklab/software_lonestar/fsl-5.0.1/data/standard/MNI152_T1_2mm_brain.nii.gz')

    args = parser.parse_args()
    return args

args=parse_command_line()

basedir=args.basedir
modelnum=args.modelnum
dataset=args.taskid
#dataset='ds105'

dsdir=os.path.join(basedir,dataset)
if not os.path.exists(dsdir):
    print '%s does not exist'%dsdir
    sys.exit(1)

gsdir=os.path.join(dsdir,'group_smoothed')
if not os.path.exists(gsdir):
    print '%s does not exist'%gsdir
    sys.exit(1)


taskdirs=glob.glob(os.path.join(gsdir,'model%03d/task*'%modelnum))

for td in taskdirs:
    
    print 'checking %s'%td
    tasknum=int(os.path.basename(td).lstrip('task'))
    
    # try to open a design.con file to get contrast names
    dscon=os.path.join(dsdir,'sub001/model/model%03d/task%03d_run001.feat/design.con'%(modelnum,tasknum))
    if os.path.exists(dscon):
        con_info=open(dscon).readlines()
        con_names=[i.strip().split('\t')[1] for i in con_info if i.find('ContrastName')>-1]
    else:
        print 'cannot open %s'%dscon

    outfilename=td+'/group_stats_report.html'
    outfile=open(outfilename,'w')
    outfile.write('<html>\n<body>\n')


    copes=glob.glob(os.path.join(td,'cope[0-9][0-9][0-9].nii.gz'))
    copes.sort()
    for c in copes:
        copenum=int(os.path.basename(c).split('.')[0].lstrip('cope'))
        print '%d: %s'%(copenum,con_names[copenum-1])
        overlay_cmd='overlay 0 0 %s -a %s 2.3 5 %s'%(args.bgimg,c.replace('.nii.gz','_tstat1.nii.gz'),c.replace('.nii.gz','_tstat1_overlay.nii.gz'))
        print overlay_cmd
        run_shell_cmd(overlay_cmd)
        
        slicer_cmd='slicer %s  -S 4  1000 %s'%(c.replace('.nii.gz','_tstat1_overlay.nii.gz'),c.replace('.nii.gz','_tstat1_overlay.png'))
        print slicer_cmd
        run_shell_cmd(slicer_cmd)


        outfile.write('%s cope%03d (%s)<br>\n'%(td,copenum,con_names[copenum-1]))
        outfile.write('<img src="%s" width=100%%/>\n'%c.replace('.nii.gz','_tstat1_overlay.png'))

    outfile.write('</body>\n</html>\n')
    outfile.close()
