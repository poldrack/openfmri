#!/usr/bin/env python
""" get checksums for all images
USAGE: get_image_checksums.py <dsdir>
"""
from run_shell_cmd import *

def usage():
    """Print the docstring and exit with error."""
    sys.stdout.write(__doc__)
    sys.exit(2)

import sys
if len(sys.argv)>1:
        taskid=sys.argv[1]
else:
    taskid='ds001'
 #   usage()

o=run_shell_cmd('find %s/sub*/{BOLD,anatomy} -name "*.nii.gz"'%taskid)

checksums=[]
outfile=open('checksums_%s.txt'%taskid,'w')

for f in o:
    outfile.write(run_shell_cmd('md5sum %s'%f)[0]+'\n')
outfile.close()
