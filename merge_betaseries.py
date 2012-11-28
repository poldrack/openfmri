#!/usr/bin/env python
""" merge a set of betaseries into a single file
"""


import os
import sys


basedir='/scratch/01329/poldrack/openfmri/shared/ds006/'
nsubs=14
goodevs=[1,2,3,4]

for s in range(nsubs):
    runs=os.listdir('%ssub%03d/model'%(basedir,s+1))
    for r in runs:
        if r.find('.feat')>-1:
            bsdir='%ssub%03d/model/%s/'%(basedir,s+1,r)
            #print 'processing %s'%bsdir
            bsfiles=[]
            for ev in goodevs:
                bsfiles.append('%s/betaseries/ev%d_lsone.nii.gz'%(bsdir,ev))
            cmd='fslmerge -t %s/betaseries/all_goodevs_lsone.nii.gz %s'%(bsdir,' '.join(bsfiles))
            print cmd
