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
        basedir='/corral/utexas/poldracklab/openfmri/staged/'



 #   outfile=open('mk_all_level2_fsf.sh','w')

    featdirs=[]
    subdirs={}


    for root,dirs,files in os.walk(basedir+taskid):
    #    for f in files:
            if root.split('/')[-1].rfind('.feat')>-1 and root.find(taskid)>-1:
                featdirs.append(root)
                fs=featdirs[-1].split('/')
                subnum=int(fs[7].replace('sub',''))
                if not subdirs.has_key(subnum):
                    subdirs[subnum]={}
                runnum=int(fs[9].split('_')[1].split('.')[0].replace('run',''))
                tasknum=int(fs[9].split('_')[0].replace('task',''))
                if not subdirs[subnum].has_key(tasknum):
                    subdirs[subnum][tasknum]=[]
                subdirs[subnum][tasknum].append(runnum)

    for s in subdirs.iterkeys():
              for t in subdirs[s].iterkeys():
                mk_level2_fsf(taskid,s,t,subdirs[s][t],basedir)

if __name__ == '__main__':
    main()
