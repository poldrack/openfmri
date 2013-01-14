#!/usr/bin/env python
""" deface an image using FSL
USAGE:  deface <filename to deface> <optional: outfilename>
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



import nibabel 
import os,sys
import numpy as N
import tempfile

import subprocess

def run_shell_cmd(cmd,cwd=[]):
    """ run a command in the shell using Popen
    """
    if cwd:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,cwd=cwd)
    else:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    for line in process.stdout:
             print line.strip()
    process.wait()
    
def usage():
    """ print the docstring and exit"""
    sys.stdout.write(__doc__)
    sys.exit(2)


template='mean_reg2mean.nii.gz'
facemask='facemask.nii.gz'

if len(sys.argv)<2:
    usage()
    sys.exit(2)
#    infile='mprage.nii.gz'
else:
    infile=sys.argv[1]

if len(sys.argv)>2:
    outfile=sys.argv[2]
else:
    outfile=infile.replace('.nii.gz','_defaced.nii.gz')
    
if os.environ.has_key('FSLDIR'):
    FSLDIR=os.environ['FSLDIR']
else:
    print 'FSLDIR environment variable must be defined'
    sys.exit(2)
    

foo,tmpmat=tempfile.mkstemp()
foo,tmpfile=tempfile.mkstemp()

print tmpmat
print tmpfile

cmd='flirt -in %s -ref %s -omat %s'%(template,infile,tmpmat)
print 'Running: '+cmd
run_shell_cmd(cmd)

cmd='flirt -in %s -out %s -ref %s -applyxfm -init %s'%(facemask,tmpfile,infile,tmpmat)
print 'Running: '+cmd
run_shell_cmd(cmd)


cmd='fslmaths %s -mul %s %s'%(infile,tmpfile,outfile)
print 'Running: '+cmd
run_shell_cmd(cmd)

os.remove(tmpfile)
os.remove(tmpmat)
