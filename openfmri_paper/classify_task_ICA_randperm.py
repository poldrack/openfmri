#!/usr/bin/env python
""" classify_task_ICA_randlabel.py - classify task in openfmri data
- shuffle the labels in order to estimate null distribution
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

# params identified from run 2 data 
params={}
params['svm']={'C':3.162278}
params['lr']={'penalty':31.62277}
params['rbf']={'C':10,'gamma':1.0}

# load data

def load_labels(infile):
    f=open(infile,'r')
    textlabels=[i.strip() for i in f.readlines()]
    return textlabels

load_data=True
trainsvm=True
testsvm=True
melodic_dir='/scratch/01329/poldrack/openfmri/analyses/paper_analysis/1_melodic/'
if load_data:
    train_labels_txt=load_labels('../wholebrain/tasklabels_run1.txt')
    labelset=list(set(train_labels_txt))
    labeldict={}
    for idx,val in enumerate(labelset):
        labeldict[val]=idx+1
    train_labels=[labeldict[x] for x in train_labels_txt]

ncomp=[2,10,20,50,100,200]

loo = LeaveOneOut(len(train_labels))

labels=N.array(train_labels)
N.random.shuffle(labels)

acc={}
acc['svm']=N.zeros(len(ncomp))
acc['rbf']=N.zeros(len(ncomp))
acc['lr']=N.zeros(len(ncomp))
pred={}
for c in range(len(ncomp)):
    pred['svm']=N.zeros(len(train_labels))
    pred['rbf']=N.zeros(len(train_labels))
    pred['lr']=N.zeros(len(train_labels))
    data=N.genfromtxt(melodic_dir+'datarun1_icarun2_%dcomp.txt'%ncomp[c])
    for train,test in loo:
        clf=LinearSVC(C=params['svm']['C'])
        clf.fit(data[train],labels[train])
        pred['svm'][test]=clf.predict(data[test])
        clf=SVC(C=params['rbf']['C'],gamma=params['rbf']['gamma'])
        clf.fit(data[train],labels[train])
        pred['rbf'][test]=clf.predict(data[test])
        clf=LogisticRegression(C=params['lr']['penalty'],penalty='l2')
        clf.fit(data[train],labels[train])
        pred['lr'][test]=clf.predict(data[test])
        
    acc['svm'][c]=N.mean(pred['svm']==labels)
    acc['rbf'][c]=N.mean(pred['rbf']==labels)
    acc['lr'][c]=N.mean(pred['lr']==labels)


fname_rand=N.random.randint(0,10**8)
f=open('classifier_accuracy_randperm_%d.pkl'%fname_rand,'wb')
pickle.dump(acc,f)
f.close()


