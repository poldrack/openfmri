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



from scikits.learn import svm
from scikits.learn.linear_model import LogisticRegression
import numpy as N
import scipy.stats

from scikits.learn.cross_val import LeaveOneOut
from scikits.learn.cross_val import StratifiedKFold
from scikits.learn import svm

basedir='/corral/utexas/poldracklab/openfmri/shared'

# note: these are changed a bit from the tsne example, because I could not use overall contrasts

all_trials_cope={2:{1:1,2:1,3:1},3:{1:1},5:{1:1},6:{1:1},7:{1:1,2:1,3:1},8:{1:1,2:1},11:{1:1,2:1,3:1,4:1},101:{1:1},102:{1:3}}

nsubs={'ds002':17,'ds003':13, 'ds005':16,'ds006':14,'ds007':21,'ds008':15,'ds011':14,'ds101':21,'ds102':26}
labelctr=0
subctr=0
datafile=[]
labels=[]

triu=N.triu_indices(309,1)  # this is for the new scatlas
nfeatures=triu[0].shape[0]

tasksperstudy=[len(a) for a in all_trials_cope.itervalues()]
nexamples=N.sum(N.asarray(tasksperstudy)*N.asarray(nsubs.values()))
X=N.zeros((nexamples,nfeatures))
print 'loading data...'

for ds in all_trials_cope.iterkeys():
    dscode='ds%03d'%ds
    for task in all_trials_cope[ds].iterkeys():
        copenum=all_trials_cope[ds][task]
        labelctr=labelctr+1
        for sub in range(1,nsubs[dscode]+1):
            df='%s/%s/sub%03d/model/task%03d_run001.feat/betaseries/ev%d_lsone_scatlas__corr.npy'%(basedir,dscode,sub,task,copenum)
            try:
                subdata=N.load(df)
            except:
                print 'problem loading %s'%df
                continue
            print subdata.shape
            if not subdata.shape:
                print 'problem with %s'%df
                continue
            if subdata.shape[0]!=309:
                print 'problem with %s'%df
            else:
                datafile.append(df)
                labels.append(labelctr)
                X[subctr,:]=subdata[triu]
                subctr=subctr+1

# fix data size to account for bad examples
X=X[:subctr,:]

Y=N.asarray(labels)

print 'running classifier...'

#loo = LeaveOneOut(len(Y))
skf=StratifiedKFold(Y,10)

predclass=N.zeros(len(Y))

foldctr=1
for train, test in skf:
    print 'fold %d'%foldctr
    X_train, X_test, y_train, y_test = X[train], X[test], Y[train], Y[test]
    clf=LogisticRegression(C=0.1,penalty='l1')
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
