#!/usr/bin/env python
"""
make the readme file for each study
"""

import argparse
import os,sys


def parse_command_line():
    parser = argparse.ArgumentParser(description='setup_subject')

    parser.add_argument('--taskid', dest='taskid',
        required=True,help='Task ID')
    parser.add_argument('-r', dest='releasenote',
        required=True,help='Release note')
    parser.add_argument('--basedir', dest='basedir',
        default='/corral-repl/utexas/poldracklab/openfmri/shared2',
        help='Base directory (above taskid directory)')
    parser.add_argument('-o', dest='overwrite', action='store_true',
        default=False,help='overwrite existing files')
   
    args = parser.parse_args()
    return args


args=parse_command_line()

dsdir=os.path.join(args.basedir,args.taskid)

if not os.path.exists(dsdir):
    print '%s does not exist'%dsdir
    sys.exit(0)

readmefile=os.path.join(dsdir,'README')
if os.path.exists(readmefile) and not args.overwrite:
    print 'README already exists, use -o to overwrite'
    sys.exit(0)

f=open(readmefile,'w')
f.write('This dataset was obtained from the OpenfMRI project (http://www.openfmri.org).\n')

try:
    task_descrip=open(os.path.join(dsdir,'study_key.txt')).readline().strip()
except:
    task_descrip=''
    
f.write('Accession #: %s\nDescription: %s\n'%(args.taskid,task_descrip))

references=[]
try:
    references=open(os.path.join(dsdir,'references.txt')).readlines()
    f.write('\nPlease cite the following references if you use these data:\n\n')
    for r in references:
        if len(r)>0:
            f.write('%s\n'%r)
except:
    print 'no references.txt file found'

try:
    history=open(os.path.join(dsdir,'release_history.txt')).readlines()
    f.write('\nRelease history:\n')
    for h in history:
        if len(h)>0:
            f.write(h)
except:
    pass

if args.releasenote:
    f.write('%s\n'%args.releasenote)

f.write('\n')
license=open(os.path.join(dsdir,'license.txt')).readlines()
for l in license:
    if len(l)>0:
        f.write(l)
    
f.close()
