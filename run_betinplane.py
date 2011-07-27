""" run_betinplane.py - run bet on inplane structural images
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

basedir='/corral/utexas/poldracklab/openfmri/shared/'
outfile=open('run_betinplane.sh','w')

for root,dirs,files in os.walk(basedir):
    for f in files:
        if f.rfind('inplane.nii.gz')>-1 and root.find('ds011')>-1:
            outfile.write('bet %s/%s %s/%s\n'%(root,f,root,f.replace('inplane','inplane_brain')))

outfile.close()

            
print 'now launch using:'
print 'launch -s run_betinplane.sh -n betinplane -r 00:30:00'
