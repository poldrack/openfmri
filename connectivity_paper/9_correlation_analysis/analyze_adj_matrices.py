#!/usr/bin/env python
""" compare connectivity matrices across methods
"""

import numpy as N
from mk_gifti_vector import *
from sklearn import metrics

target_adj=500
basedir='/scratch/01329/poldrack/openfmri/analyses/connectivity_paper/'

bs_count=N.load(basedir+'9_correlation_analysis/bs_count_%dadj.npy'%target_adj)
resid_count=N.load(basedir+'9_correlation_analysis/resid_count_%dadj.npy'%target_adj)
dti_adjmtx_thresh=N.load(basedir+'9_correlation_analysis/dti_adjmtx_thresh_%dadj.npy'%target_adj)
neurosynth_adjmtx_thresh=N.load(basedir+'9_correlation_analysis/ns_adjmtx_thresh_%dadj.npy'%target_adj)
resting_adjmtx_thresh=N.load(basedir+'9_correlation_analysis/resting_adjmtx_thresh_%dadj.npy'%target_adj)

tridx=N.triu_indices(296,1)

# get upper triangles and binarize counts

bs=(bs_count[tridx]>0).astype('int')
resid=(resid_count[tridx]>0).astype('int')
dti=dti_adjmtx_thresh[tridx]
ns=neurosynth_adjmtx_thresh[tridx]
resting=resting_adjmtx_thresh[tridx]

all_triu=bs+resid+dti+ns+resting
sum_adjmtx=N.zeros((296,296))
sum_adjmtx[tridx]=all_triu

conj_triu=(all_triu==5).astype('int')

conj_adjmtx=N.zeros((296,296))
conj_adjmtx[tridx]=conj_triu

mk_gifti_vector_from_adjmtx(conj_adjmtx,basedir+'11_gifti_renderings/conj_%dadj.vector.gii'%target_adj,0)
N.save(basedir+'9_correlation_analysis/conj_%dadj.npy'%target_adj,conj_adjmtx)

mk_gifti_vector_from_adjmtx(sum_adjmtx,basedir+'11_gifti_renderings/sum_%dadj.vector.gii'%target_adj,0)
N.save(basedir+'9_correlation_analysis/sum_%dadj.npy'%target_adj,sum_adjmtx)

# get some stats
rand_bs_resid=metrics.adjusted_rand_score(bs,resid)
rand_resting_resid=metrics.adjusted_rand_score(resting,resid)
rand_resting_bs=metrics.adjusted_rand_score(resting,bs)
rand_resting_dti=metrics.adjusted_rand_score(resting,dti)
rand_resting_ns=metrics.adjusted_rand_score(resting,ns)
rand_resid_ns=metrics.adjusted_rand_score(resid,ns)
rand_bs_ns=metrics.adjusted_rand_score(bs,ns)
