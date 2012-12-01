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
from sklearn.metrics import confusion_matrix

import os

# load data

datadir='/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_Dec2012/data_prep/'
outdir='/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_Dec2012/classifier/'

load_data=True
trainsvm=True

if load_data:
    datakeyfile=os.path.join(datadir,'data_key_run1.txt')
    datakey=N.loadtxt(datakeyfile)
    labels=datakey[:,0]
#    test_labels_txt=load_labels('tasklabels_run2.txt')
#    test_labels=[labeldict[x] for x in test_labels_txt]

    data=N.load(os.path.join(datadir,'zstat_run1.npy'))
#    test_data=N.load('zstat_run2.npy')


skf=StratifiedKFold(labels,8)
#loo=LeaveOneOut(len(labels))


if trainsvm:
    pred=N.zeros(len(labels))
    for train,test in skf:
        clf=LinearSVC()
        clf.fit(data[train],labels[train])
        pred[test]=clf.predict(data[test])


testacc=N.mean(pred==labels)
print 'test accuracy = %f'%N.mean(pred==labels)
cm=confusion_matrix(labels,pred)
print cm

N.savez(os.path.join(outdir,'classifier_results_SVM'),pred,labels,cm)
