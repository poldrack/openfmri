""" run_betaseries_atlas_extraction.py


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

def usage():
    """Print the docstring and exit with error."""
    sys.stdout.write(__doc__)
    sys.exit(2)

#def main():
if 1==1:
    
##     if len(sys.argv)>1:
##         dataset=sys.argv[1]
##     else:
##         usage()


##     if len(sys.argv)>2:
##         basedir=sys.argv[2]
##         if not os.path.exists(basedir):
##             print 'basedir %s does not exist!'%basedir
##             sys.exit(1)
##     else:
##         basedir='/corral/utexas/poldracklab/openfmri/staged/'

    basedir='/corral/utexas/poldracklab/openfmri/shared/'



    outfile=open('run_betaseries_atlas_extraction.sh','w')

 
    for root,dirs,files in os.walk(basedir):
        for f in files:
            if f.rfind('_lsone.nii.gz')>-1:  # and root.find(dataset)>-1:
                f_split=root.split('/')
                featdir='/'.join(root.split('/')[:-1])
                cmd='python atlasextraction.py %s/%s %s %s/%s'%(root,f,featdir,root,f.replace('.nii.gz','_scatlas_roi.txt'))
                #print cmd
                outfile.write(cmd+'\n')
 
    outfile.close()

    print 'now run  using:'
    print 'launch run_betaseries_atlas_extraction.sh'
    


#if __name__ == '__main__':
#    main()
