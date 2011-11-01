#!/usr/bin/env python
"""
run1 classification

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
from classifier_run import *
import pickle
f=open('bestparams_run2.pkl','rb')
params=pickle.load(f)
f.close()

basedir='/scratch/01329/poldrack/openfmri/shared/correlations/'
outputdir=basedir+'/resid_classifier/'


models=['sc_corr','sc_pcorr','sc_regpcorr','tomtom_corr','tomtom_pcorr','tomtom_regpcorr']

for m in models:
    datastem='resid_%s_run001'%m
    datafile=datastem+'.npy'
    labelfile=datastem+'_labels.txt'
    outputfile=outputdir+datastem+'_svm.pkl'
    cmd='/work/01329/poldrack/code/poldrack/python/classifier_run.py -t LinearSVC -d %s -l %s -o %s -c %f --cv 8'%(datafile,labelfile,outputfile,params[m]['svm'])
    print cmd

    outputfile=outputdir+datastem+'_rbf.pkl'
    cmd='/work/01329/poldrack/code/poldrack/python/classifier_run.py -t SVC -d %s -l %s -o %s -c %f --cv 8 -g %f'%(datafile,labelfile,outputfile,params[m]['rbf']['C'],params[m]['rbf']['gamma'])
    print cmd

    outputfile=outputdir+datastem+'_lr.pkl'
    cmd='/work/01329/poldrack/code/poldrack/python/classifier_run.py -t LogisticRegression -d %s -l %s -o %s -c %f --cv 8'%(datafile,labelfile,outputfile,params[m]['lr'])
    print cmd



