#!/usr/bin/env python
"""
create multi-task multi-sub dataset
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
import nibabel
import os
from get_contrasts_to_use import *

basedir='/corral-repl/utexas/poldracklab/openfmri/shared2/'
zstatdir=os.path.join(basedir,'zstats')
outdir='/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_April2013/data_prep'


contrasts_to_use=get_contrasts_to_use()

zstats=os.listdir(zstatdir)

file_ds=[]
file_subctr=[]
file_task=[]
file_run=[]
file_zstat=[]

for z in zstats:
    z_split=z.split('_')
    file_ds.append(z_split[0])
    file_subctr.append(z_split[1].replace('subctr',''))
    file_task.append(z_split[2])
    file_run.append(z_split[3])
    file_zstat.append(z_split[4])
    
subnums={}
for ds in contrasts_to_use.iterkeys():
     subnums[ds]=[int(file_subctr[i]) for i,x in enumerate(file_ds) if x.find(ds)>-1 and file_task[i].find('task001')>-1 and file_run[i].find('run001')>-1 and file_zstat[i].find('zstat001')>-1]


taskctr={'ds001': {1: 1},
 'ds002': {1: 2, 2: 3, 3: 4},
 'ds003': {1: 5},
 'ds005': {1: 6},
 'ds006A': {1: 7},
 'ds007': {1: 8, 2: 9, 3: 10},
 'ds008': {1: 11, 2: 12},
 'ds011': {1: 13, 2: 14, 3: 15, 4: 16},
 'ds017A': {2: 17},
 'ds051': {1: 18},
 'ds052': {1: 19, 2: 20},
 'ds101': {1: 21},
 'ds102': {1: 22},
 'ds107': {1: 23},
 'ds108': {1: 24},
 'ds109': {1: 25},
 'ds110': {1: 26}}

zstat_files={1:[],2:[]}  # index across runs

taskinfo={}

for ds in contrasts_to_use.iterkeys():
    taskinfo[ds]={}
    for t in contrasts_to_use[ds].iterkeys():
      for s in subnums[ds]:
        for cope in contrasts_to_use[ds][t]:
          for run in [1,2]:
            cf='%s_subctr%03d_task%03d_run%03d_zstat%03d.nii.gz'%(ds,s,t,run,cope)
            if os.path.exists(os.path.join(zstatdir,cf)):
                zstat_files[run].append(cf)
                #print copefiles[-1]
            else:
                print 'problem with %s'%cf
        

for run in [1,2]:
    npts=len(zstat_files[run])
    ctr=0
    infofile=open(os.path.join(outdir,'data_key_run%d.txt'%run),'w')

    alldata=N.zeros((91,109,91,npts))
    for z in zstat_files[run]:
                    #print 'processing ', z
                    i=nibabel.load(os.path.join(zstatdir,z))
                    ds,subctr,task,runctr,zstatctr=z.replace('.nii.gz','').split('_')
                    alldata[:,:,:,ctr]=i.get_data()
                    infofile.write('%d\t%d\t%d\t%d\t%d\t%d\n'%(taskctr[ds][int(task.replace('task',''))],int(subctr.replace('subctr','')),int(ds.replace('ds','').replace('A','')),int(task.replace('task','')),int(runctr.replace('run','')),int(zstatctr.replace('zstat',''))))
                    ctr=ctr+1

    infofile.close()


    d=nibabel.Nifti1Image(alldata,i.get_affine())
    d.to_filename(os.path.join(outdir,'zstat_run%d.nii.gz'%run))
