#!/usr/bin/env python
""" classify_task_wholebrain.py - classify task in openfmri data
- train on run 1, test on run 2
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

# load data

def load_labels(infile):
    f=open(infile,'r')
    textlabels=[i.strip() for i in f.readlines()]
    return textlabels

load_data=True
trainsvm=True

if load_data:
    train_labels_txt=load_labels('tasklabels_run1.txt')
    labelset=list(set(train_labels_txt))
    labeldict={}
    for idx,val in enumerate(labelset):
        labeldict[val]=idx+1
    train_labels=[labeldict[x] for x in train_labels_txt]
#    test_labels_txt=load_labels('tasklabels_run2.txt')
#    test_labels=[labeldict[x] for x in test_labels_txt]

    train_data=N.load('zstat_run1.npy')
#    test_data=N.load('zstat_run2.npy')

labels=N.array(train_labels)
skf=StratifiedKFold(labels,8)
#loo=LeaveOneOut(len(labels))

# get of voxels with zeros
goodvox=[]
for x in range(train_data.shape[0]):
    if len(N.nonzero(train_data[x,:])[0])==379:
        goodvox.append(x)

data=train_data[goodvox,:]
print 'found %d good voxels'%len(goodvox)



if trainsvm:
    pred=N.zeros(len(labels))
    for train,test in skf:
        clf=LinearSVC()
        clf.fit(data[train],labels[train])
        pred[test]=clf.predict(data[test])


    
print 'test accuracy = %f'%N.mean(pred==labels)
