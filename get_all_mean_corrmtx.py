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
from openfmri_utils import *

basedir='/corral/utexas/poldracklab/openfmri/shared'
outputdir='/corral/utexas/poldracklab/openfmri/analyses/betaseries_corrmtrx_scatlas/'

# note: these are changed a bit from the tsne example, because I could not use overall contrasts

#all_trials_cope={2:{1:1,2:1,3:1},3:{1:1},5:{1:1},6:{1:1},7:{1:1,2:1,3:1},8:{1:1,2:1},11:{1:1,2:1,3:1,4:1},101:{1:1},102:{1:3}}

#all_trials_cope={2:{1:1},3:{1:1},5:{1:1},6:{1:1},7:{1:1},8:{1:1},11:{1:1},101:{1:1},102:{1:3}}

nsubs={'ds002':17,'ds003':13, 'ds005':16,'ds006':14,'ds007':21,'ds008':15,'ds011':14,'ds101':21,'ds102':26}

#dataset='ds007'
maxruns=10

for dataset in nsubs.iterkeys():
    condkey=load_condkey('%s/%s/condition_key.txt'%(basedir,dataset))
    datatype='corr'

    runs={}
    # first out runs
    for sub in range(nsubs[dataset]):
        runs[sub+1]={}
        for task in condkey.iterkeys():
            modeldir='%s/%s/sub%03d/model/'%(basedir,dataset,sub+1)
            # find runs:
            runs[sub+1][task]=[]
            for run in range(1,maxruns):
                if os.path.exists('%s/task%03d_run%03d.feat'%(modeldir,task,run)):
                    runs[sub+1][task].append(run)


    for task in condkey.iterkeys():
        for cond in condkey[task].iterkeys():
            meandata=N.zeros((309,309))
            subdatactr=0
            for sub in range(nsubs[dataset]):
                for run in runs[sub+1][task]:
                    datafile='%s/task%03d_run%03d.feat/betaseries/ev%d_lsone_scatlas__%s.npy'%(modeldir,task,run,cond,datatype)
                    if not os.path.exists(datafile):
                        print 'missing: %s'%datafile
                    else:
                        subdata=N.load(datafile)
                        if data.shape[0]!=309:
                            print 'problem with %s'%datafile

                        else:
                            meandata=subdata+meandata
                            subdatactr+=1

            meandata=meandata/subdatactr
            N.save('%s/%s_task%03d_cond%03d_%s.npy'%(outputdir,dataset,task,cond,datatype),meandata)

