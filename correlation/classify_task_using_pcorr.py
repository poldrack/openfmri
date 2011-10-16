#!/usr/bin/env python
""" classify_task_using_pcorr.py - classify task in openfmri data using partial correlation of ROI regions
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



from sklearn import svm
from sklearn.linear_model import LogisticRegression
import numpy as N
import scipy.stats

from sklearn.cross_validation import LeaveOneOut
from sklearn.cross_validation import StratifiedKFold


basedir='/scratch/01329/poldrack/openfmri/shared/correlations/'

datastem='resid_sc_corr_run001'
X=N.load(basedir+datastem+'.npy')
f=open(basedir+datastem+'_labels.txt','r')
labels=[x.strip() for x in f.readlines()]
f.close()

# number the labels

labelset=set(labels)
labeldict={}
for idx,val in enumerate(labelset):
        labeldict[val]=idx+1
Y=N.array([labeldict[x] for x in labels])


print 'running classifier...'

#loo = LeaveOneOut(len(Y))
skf=StratifiedKFold(Y,10)

predclass=N.zeros(len(Y))

foldctr=1
for train, test in skf:
    print 'fold %d'%foldctr
    X_train, X_test, y_train, y_test = X[train], X[test], Y[train], Y[test]
 #   clf=svm.LinearSVC(C=1)
    clf=LogisticRegression()
    clf.fit(X_train,y_train)
    predclass[test]=clf.predict(X_test)
    foldctr=foldctr+1

print 'Mean accuracy=%0.3f'%N.mean(predclass==Y)

kjahsdf

# randomize labels 1000 times and store accuracy
nruns=500
randacc=N.zeros(nruns)

for r in range(nruns):
    N.random.shuffle(Y)
    for train, test in loo:
        X_train, X_test, y_train, y_test = X[train], X[test], Y[train], Y[test]
#        clf=LogisticRegression(C=1,penalty='l2')
        clf=svm.LinearSVC()
        clf.fit(X_train,y_train)
        predclass[test]=clf.predict(X_test)
    randacc[r]=N.mean(predclass==Y)
    
print 'Mean accuracy with shuffled labels=%0.3f'%N.mean(randacc)
print 'Max accuracy with shuffled labels=%0.3f'%N.max(randacc)
print '95 pct accuracy with shuffled labels=%0.3f'%scipy.stats.scoreatpercentile(randacc,95)
