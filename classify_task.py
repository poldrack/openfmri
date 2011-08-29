#!/usr/bin/env python
""" classify_task.py - classify task in openfmri data
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

basedir='/corral/utexas/poldracklab/openfmri/melodic/'
icadir='ica_9tasks_120comp/'

melodic_mix=N.genfromtxt(basedir+icadir+'melodic_mix')
copedata=N.genfromtxt(basedir+'/copedata.txt')

cope1_data=(copedata[:,1]==1)
task1_data=(copedata[:,2]==1)

usedata=N.zeros(len(copedata))

s=set(copedata[:,0])
# find max cope (all-trials) for each task
maxcope={}
for t in list(s):
    maxcope[t]=N.max(copedata[copedata[:,0]==t,2])

all_trials_cope={2:{1:1,2:1,3:3},3:{1:3},5:{1:1},6:{1:6},7:{1:1,2:1,3:1},8:{1:1,2:1},11:{1:1,2:1,3:1,4:5},101:{1:5},102:{1:5}}

for x in range(len(copedata)):
    if copedata[x,2]==all_trials_cope[copedata[x,0]][copedata[x,1]]:
#    if copedata[x,1]==1:
        usedata[x]=1



## for x in range(len(copedata)):
## #    if copedata[x,1]==1 and copedata[x,2]==1:
##      if copedata[x,2]==1:
##         usedata[x]=1

copedata=copedata[usedata==1,:]

# get class labels
ctr=1
dstask={}

s=set(copedata[:,0])
for ds in list(s):
    dstask[ds]={}
    sdata=copedata[:,0]==ds
    stasks=set(copedata[sdata,1])
    for t in stasks:
        dstask[ds][t]=ctr
        ctr=ctr+1

Y=N.zeros(len(copedata))
for x in range(len(copedata)):
    Y[x]=dstask[copedata[x,0]][copedata[x,1]]


X=melodic_mix[usedata==1,:]

loo = LeaveOneOut(len(Y))

predclass=N.zeros(len(Y))

for train, test in loo:
    X_train, X_test, y_train, y_test = X[train], X[test], Y[train], Y[test]
    clf=LogisticRegression(C=0.1,penalty='l1')
    clf.fit(X_train,y_train)
    predclass[test]=clf.predict(X_test)

print 'Mean accuracy=%0.3f'%N.mean(predclass==Y)

# randomize labels 1000 times and store accuracy
nruns=500
randacc=N.zeros(nruns)

for r in range(nruns):
    N.random.shuffle(Y)
    for train, test in loo:
        X_train, X_test, y_train, y_test = X[train], X[test], Y[train], Y[test]
        clf=LogisticRegression(C=1,penalty='l2')
        clf.fit(X_train,y_train)
        predclass[test]=clf.predict(X_test)
    randacc[r]=N.mean(predclass==Y)
    
print 'Mean accuracy with shuffled labels=%0.3f'%N.mean(randacc)
print 'Max accuracy with shuffled labels=%0.3f'%N.max(randacc)
print '95 pct accuracy with shuffled labels=%0.3f'%scipy.stats.scoreatpercentile(randacc,95)
