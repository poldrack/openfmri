#!/usr/bin/env python
""" estimate_parameters_from_run2.py
- use the run 2 data to estimate the best parameter values
- these will then be applied in the run1 classification
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



from sklearn.svm import LinearSVC,SVC
from sklearn.cross_validation import LeaveOneOut,StratifiedKFold
from sklearn.linear_model import LogisticRegression
import pickle
import numpy as N
import os

# load data

load_data=True
trainsvm=True
testsvm=True
basedir='/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_April2013/'
melodic_dir='/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_April2013/ICA/'
outdir=os.path.join(basedir,'classifier')
train_labels=N.loadtxt(os.path.join(basedir,'data_prep/data_key_run2.txt'))[:,0]

ncomp=[2,10,20,50,100,200]

skf = StratifiedKFold(train_labels, 8)

labels=N.array(train_labels)
svmparams=N.arange(-3,5,0.5)
lrparams=N.arange(-3,5,0.5)
rbfparams=N.arange(-3,5,0.5)
acc={}
acc['svm']=N.zeros((len(ncomp),len(svmparams)))
acc['lr']=N.zeros((len(ncomp),len(lrparams)))
acc['rbf']=N.zeros((len(ncomp),len(svmparams),len(rbfparams)))

acc['svmparams']=svmparams
acc['rbfparams']=rbfparams
acc['lrparams']=lrparams
acc['ncomp']=ncomp

pred={}
for c in range(len(ncomp)):
    pred['svm']=N.zeros((len(train_labels),len(svmparams)))
    pred['rbf']=N.zeros((len(train_labels),len(svmparams),len(rbfparams)))
    pred['lr']=N.zeros((len(train_labels),len(lrparams)))
    data=N.genfromtxt(melodic_dir+'datarun2_icarun2_%dcomp.txt'%ncomp[c])

    for p in range(len(svmparams)):
        for train,test in skf:
            clf=LinearSVC(C=10**svmparams[p])
            clf.fit(data[train],labels[train])
            pred['svm'][test,p]=clf.predict(data[test])
            for r in range(len(rbfparams)):
                clf=SVC(C=10**svmparams[p],gamma=10**rbfparams[r])
                clf.fit(data[train],labels[train])
                pred['rbf'][test,p,r]=clf.predict(data[test])
                
            clf=LogisticRegression(C=10**lrparams[p],penalty='l2')
            clf.fit(data[train],labels[train])
            pred['lr'][test,p]=clf.predict(data[test])
        
        acc['svm'][c,p]=N.mean(pred['svm'][:,p]==labels)
        acc['lr'][c,p]=N.mean(pred['lr'][:,p]==labels)
        for r in range(len(rbfparams)):
            acc['rbf'][c,p,r]=N.mean(pred['rbf'][:,p,r]==labels)




f=open(os.path.join(outdir,'ICA_classifier_accdata_paramest_run2.pkl'),'wb')
pickle.dump(acc,f)
f.close()
