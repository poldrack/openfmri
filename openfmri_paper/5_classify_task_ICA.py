#!/usr/bin/env python
""" classify_task_ICA.py - classify task in openfmri data

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
from sklearn.cross_validation import LeaveOneOut
from sklearn.linear_model import LogisticRegression
import pickle
import numpy as N
import sys,os
from get_best_params import *
import os

# params identified from run 2 data 
#params={}
#params['svm']={'C':3.162278}
#params['lr']={'penalty':31.62277}
#params['rbf']={'C':10,'gamma':1.0}


# load data

load_data=True
trainsvm=True
testsvm=True
basedir='/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_Dec2012/'
melodic_dir='/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_Dec2012/ICA_smoothed_6mm/'
outdir=os.path.join(basedir,'classifier')
labels=N.loadtxt(os.path.join(basedir,'data_prep/data_key_run1.txt'))[:,0]

f=open(os.path.join(outdir,'ICA_classifier_accdata_paramest_run2.pkl'))
param_opt=pickle.load(f)
f.close()

linsvm,rbfsvm,logreg=get_best_params()

ncomp=[2,10,20,50,100,200]

loo = LeaveOneOut(len(labels))
svmparams=10.0**param_opt['svmparams']
lrparams=10.0**param_opt['lrparams']
rbfparams=10.0**param_opt['rbfparams']


acc={}
acc['svm']=N.zeros(len(ncomp))
acc['rbf']=N.zeros(len(ncomp))
acc['lr']=N.zeros(len(ncomp))
pred={}
for c in range(len(ncomp)):
    pred['svm']=N.zeros(len(labels))
    pred['rbf']=N.zeros(len(labels))
    pred['lr']=N.zeros(len(labels))
    data=N.genfromtxt(melodic_dir+'datarun1_icarun1_%dcomp.txt'%ncomp[c])
    for train,test in loo:
        svm_c=linsvm[c]
        print 'SVM: ',svm_c
        clf=LinearSVC(C=svm_c)
        clf.fit(data[train],labels[train])
        pred['svm'][test]=clf.predict(data[test])
        svm_c=rbfsvm[c,0]
        svm_gamma=rbfsvm[c,1]
        print 'SVM-RBF: ',svm_c,svm_gamma
        clf=SVC(C=svm_c,gamma=svm_gamma)
        clf.fit(data[train],labels[train])
        pred['rbf'][test]=clf.predict(data[test])
        lrpen=logreg[c]
        print 'logistic: ',lrpen
        clf=LogisticRegression(C=lrpen,penalty='l2')
        clf.fit(data[train],labels[train])
        pred['lr'][test]=clf.predict(data[test])
        
    acc['svm'][c]=N.mean(pred['svm']==labels)
    acc['rbf'][c]=N.mean(pred['rbf']==labels)
    acc['lr'][c]=N.mean(pred['lr']==labels)


f=open(os.path.join(outdir,'ICA_classifier_accuracy.pkl'),'wb')
pickle.dump(acc,f)
f.close()


