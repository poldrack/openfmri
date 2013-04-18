#!/usr/bin/env python
""" classify_task_searchlight.py - classify task in openfmri data

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




import numpy as N
from sklearn.svm import LinearSVC,SVC
from sklearn.cross_validation import LeaveOneOut,StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from mvpa2.suite import *

import os,sys

run=int(sys.argv[1])

# load data

datadir='/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_April2013/data_prep/'
outdir='/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_April2013/classifier/searchlight'

load_data=True
trainsvm=True

if load_data:
    datakeyfile=os.path.join(datadir,'data_key_run1.txt')
    datakey=N.loadtxt(datakeyfile)
    labels=datakey[:,0]
    subjects=datakey[:,1]
    
#    test_labels_txt=load_labels('tasklabels_run2.txt')
#    test_labels=[labeldict[x] for x in test_labels_txt]

#    data=N.load(os.path.join(datadir,'zstat_run1.npy'))
#    test_data=N.load('zstat_run2.npy')


if 1:
  dataset = fmri_dataset(
                    samples=os.path.join(datadir, 'zstat_run1.nii.gz'),
                          targets=labels,
                          chunks=range(len(labels)),
                          mask=os.path.join(datadir, 'goodvoxmask.nii.gz'))

# enable debug output for searchlight call
#if __debug__:
#        debug.active += ["SLC"]

        
clf=LinearCSVMC()
part=NGroupPartitioner(ngroups=8)
cv = CrossValidation(clf, part)
radius=5
print 'starting searchlight...'

sl = sphere_searchlight(cv, radius=radius, space='voxel_indices',
                          postproc=mean_sample(),nproc=12)


ds = dataset.copy(deep=False,
                sa=['targets','chunks'],
                fa=['voxel_indices'],
                a=['mapper'])

# randomly reorder data and labels so that crossvalidation works
randidx=range(ds.samples.shape[0])
N.random.shuffle(randidx)
ds.samples=ds.samples[randidx,:]
ds.targets=ds.targets[randidx,:]

sl_map=sl(ds)
sl_map.samples *= -1
sl_map.samples += 1
     
niftiresults = map2nifti(sl_map, imghdr=dataset.a.imghdr)
niftiresults.to_filename(os.path.join(outdir,'searchlight_radius%d_run%d.nii.gz'%(radius,run)))

