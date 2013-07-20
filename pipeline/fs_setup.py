#!/usr/bin/env python
""" fs_setup.py - set up directories for freesurfer analysis
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


import os,sys

dataset=sys.argv[1]
if len(sys.argv)>2:
  basedir=sys.argv[2]
else:
  basedir=os.path.abspath(os.curdir)
if len(sys.argv)>3:
  subdir=sys.argv[3]
else:
  subdir='/corral-repl/utexas/poldracklab/openfmri/subdir'
  
outfile=open('fs_setup.sh','w')
#subdir=basedir+'subdir'
if not basedir[-1]=='/':
  basedir=basedir+'/'
  
if not os.path.exists(basedir+dataset):
  print '%s/%s does not exist'%(basedir,dataset)
  sys.exit(2)
  
#for d in os.listdir(basedir+ds):
#  if d[0:3]=='sub':
for root,dirs,files in os.walk(basedir+dataset):
  if root.find(dataset)>-1:
    for f in files:
        if f.rfind('highres001.nii.gz')>-1:
            f_split=root.split('/')
            outfile.write('recon-all -i %s/%s -subjid %s_%s -sd %s\n'%(root,f,f_split[-3],f_split[-2],subdir))

outfile.close()

            
print 'now launch using: sh fs_setup.sh'


