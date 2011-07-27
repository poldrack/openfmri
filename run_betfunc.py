""" run_betfunc.py - run bet on functional images

USAGE: python run_betfnc.py <name of dataset> <basedir - default is staged>

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
        basedir='/corral/utexas/poldracklab/openfmri/staged/'
        
    outfile=open('run_mcflirt.sh','w')


    outfile=open('run_betfunc.sh','w')

    for root,dirs,files in os.walk(basedir+ds):
        for f in files:
            if f.rfind('bold_mcf.nii.gz')>-1  and root.find(ds)>-1:
                outfile.write('bet %s/%s %s/%s -F\n'%(root,f,root,f.replace('mcf','mcf_brain')))

    outfile.close()


    print 'now launch using:'
    print 'launch -s run_betfunc.sh -n betfunc -r 00:10:00'

if __name__ == '__main__':
    main()
