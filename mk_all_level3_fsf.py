#!/usr/bin/env python
"""mk_all_level3_fsf.py - make level 3 fsf files
USAGE: python mk_all_level3_fsf.py <name of dataset> <nsubs>  <basedir - default is staged>
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
from openfmri_utils import *

from mk_level3_fsf import *

import sys

def usage():
    """Print the docstring and exit with error."""
    sys.stdout.write(__doc__)
    sys.exit(2)

def main():

    if len(sys.argv)>2:
        taskid=sys.argv[1]
        numsub=int(sys.argv[2])
    else:
        usage()


    if len(sys.argv)>3:
        basedir=sys.argv[3]
        if not os.path.exists(basedir):
            print 'basedir %s does not exist!'%basedir
            sys.exit(1)
    else:
        basedir='/corral/utexas/poldracklab/openfmri/staged/'




    featdirs=[]
    subdirs={}


 
 
    nsubs={taskid:numsub}
    taskid_list=nsubs.keys()


    for taskid in taskid_list:
      cond_key=load_condkey(basedir+taskid+'/condition_key.txt')
      ntasks=len(cond_key)


      for t in range(ntasks):
        mk_level3_fsf(taskid,t+1,nsubs[taskid],basedir)

if __name__ == '__main__':
    main()
