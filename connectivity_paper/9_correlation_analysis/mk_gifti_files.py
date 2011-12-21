#!/usr/bin/env python
""" create gifti files for connectivity matrices
"""

import numpy as N
from mk_gifti_vector import *

basedir='/scratch/01329/poldrack/openfmri/analyses/connectivity_paper/'

# read in task descriptors
f=open(basedir+'9_correlation_analysis/tasknames-desc.txt','r')
taskdesc={}
for i in f.readlines():
    i_s=i.strip().split('\t')
    taskdesc[i_s[0]]=i_s[1]
f.close()


f=open(basedir+'9_correlation_analysis/tasknames_regpcorr.txt','r')

tasknames_pcorr=[]
for i in f.readlines():
    i_s=i.strip().split('_')
    type='other'
    tn=i.strip()
    if i_s[0].find('resid')==0:
        type='res'
        tn=i.strip().replace('resid_','')
    elif i_s[0].find('bs')==0:
        type='bs'
        tn=i.strip().replace('bs_','')

    if taskdesc.has_key(tn):
        tasknames_pcorr.append(taskdesc[tn]+'_'+type)
    else:
        tasknames_pcorr.append(tn)
                                      
f.close()

# load data
data_pcorr=N.load(basedir+'8_mean_corrmtx/corrdata_regpcorr.npy')
tridx=N.triu_indices(296,1)
adjmtx=N.zeros((data_pcorr.shape[0],296,296))

# reconstruct full adjacency matrices

for i in range(data_pcorr.shape[0]):
    tmp=N.zeros((296,296))
    tmp[tridx]=data_pcorr[i,:]
    adjmtx[i,:,:]=tmp
    
dti_adjmtx=adjmtx[0,:,:]
neurosynth_adjmtx=adjmtx[1,:,:]
resting_adjmtx=adjmtx[2,:,:]

resid_adjmtx=adjmtx[3:32,:,:]
bs_adjmtx=adjmtx[32:,:,:]



# find thresholds for each dataset that give a target # of adjacencies

target_adj=500

resting_thresh=N.max(resting_adjmtx)
nadj_resting=1
while nadj_resting<target_adj:
    resting_thresh-=0.001
    nadj_resting=N.where(resting_adjmtx>resting_thresh)[0].shape[0]

resting_adjmtx_thresh=(resting_adjmtx>resting_thresh).astype('int')


dti_thresh=N.max(dti_adjmtx)
nadj_dti=1
while nadj_dti<target_adj:
    dti_thresh-=0.001
    nadj_dti=N.where(dti_adjmtx>dti_thresh)[0].shape[0]

dti_adjmtx_thresh=(dti_adjmtx>dti_thresh).astype('int')
# get threshold for neurosynth

ns_thresh=N.max(neurosynth_adjmtx)
nadj_ns=1
while nadj_ns<target_adj:
    ns_thresh-=0.001
    nadj_ns=N.where(neurosynth_adjmtx>ns_thresh)[0].shape[0]

neurosynth_adjmtx_thresh=(neurosynth_adjmtx>ns_thresh).astype('int')

res_thresh=0.1*N.ones(resid_adjmtx.shape[0])
resid_adjmtx_thresh=N.zeros(resid_adjmtx.shape)
for res_ds in range(resid_adjmtx.shape[0]):
    nadj_res=0
    while nadj_res<target_adj:
        res_thresh[res_ds]-=0.001
        nadj_res=N.where(resid_adjmtx[res_ds,:,:]>res_thresh[res_ds])[0].shape[0]
    resid_adjmtx_thresh[res_ds,:,:]=(resid_adjmtx[res_ds,:,:]>res_thresh[res_ds]).astype('int')

bs_thresh=0.1*N.ones(bs_adjmtx.shape[0])
bs_adjmtx_thresh=N.zeros(bs_adjmtx.shape)

for bs_ds in range(bs_adjmtx.shape[0]):
    nadj_bs=0
    while nadj_bs<target_adj:
        bs_thresh[bs_ds]-=0.001
        nadj_bs=N.where(bs_adjmtx[bs_ds,:,:]>bs_thresh[bs_ds])[0].shape[0]
    bs_adjmtx_thresh[bs_ds,:,:]=(bs_adjmtx[bs_ds,:,:]>bs_thresh[bs_ds]).astype('int')

bs_count=N.sum(bs_adjmtx_thresh,0)
resid_count=N.sum(resid_adjmtx_thresh,0)

mk_gifti_vector_from_adjmtx(dti_adjmtx,basedir+'11_gifti_renderings/dti_%dadj.vector.gii'%target_adj,dti_thresh)
mk_gifti_vector_from_adjmtx(neurosynth_adjmtx,basedir+'11_gifti_renderings/neurosynth_%dadj.vector.gii'%target_adj,ns_thresh)
mk_gifti_vector_from_adjmtx(bs_count,basedir+'11_gifti_renderings/bs_%dadj.vector.gii'%target_adj,0)
mk_gifti_vector_from_adjmtx(resid_count,basedir+'11_gifti_renderings/resid_%dadj.vector.gii'%target_adj,0)

N.save(basedir+'9_correlation_analysis/bs_count_%dadj.npy'%target_adj,bs_count)
N.save(basedir+'9_correlation_analysis/resid_count_%dadj.npy'%target_adj,resid_count)
N.save(basedir+'9_correlation_analysis/dti_adjmtx_thresh_%dadj.npy'%target_adj,dti_adjmtx_thresh)
N.save(basedir+'9_correlation_analysis/ns_adjmtx_thresh_%dadj.npy'%target_adj,neurosynth_adjmtx_thresh)
N.save(basedir+'9_correlation_analysis/resting_adjmtx_thresh_%dadj.npy'%target_adj,resting_adjmtx_thresh)
