#!/usr/bin/env python
""" run clustering on connectivity matrices
"""

import numpy as N
from sklearn import decomposition
from sklearn.decomposition import FastICA
from sklearn.cluster import AffinityPropagation
import matplotlib.pyplot as plt
from hcluster import pdist, linkage, dendrogram
from sklearn.cluster import DBSCAN
from scipy.spatial import distance

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

cc_pcorr=N.corrcoef(data_pcorr)
cc_pcorr[N.diag_indices(50)]=0
meancorr=N.mean(cc_pcorr,0)

if 1==1:
    fig = plt.figure(figsize=(16,10))
    ax = fig.add_subplot(111)
    ax.set_yticks(range(50))
    labels = ax.set_yticklabels(tasknames_pcorr)
    plt.imshow(cc_pcorr)
    for x in range(50):
        plt.text(50,x,'%.2f'%meancorr[x],size=6)
        for y in range(50):
            if not x==y:  # skip diagonal
                plt.text(x-0.3,y,'%.2f'%cc_pcorr[x,y],size=6,color='red')

    plt.savefig(basedir+'9_correlation_analysis/pcorr_corrcoefs.pdf',format='pdf')


#do clustering

if 1==1:
    dst=pdist(data_pcorr[2:,:])
    Z=linkage(dst,method='complete')
    plt.figure(figsize=(14,12))
    dendrogram(Z,labels=tasknames_pcorr)
    plt.savefig(basedir+'9_correlation_analysis/pcorr_task_cluster.pdf',format='pdf')

# decompose connections using ICA and save adjacency matrices

data_pcorr_fmri=data_pcorr[2:,:]

if 1==0:
    ica = FastICA(n_components=20)
    S_ = ica.fit(data_pcorr_fmri.T).transform(data_pcorr_fmri.T)  # Get the estimated sources
    A_ = ica.get_mixing_matrix()  # Get estimated mixing matrix


                                  #ncomps=20
                                  #nmf=decomposition.ProjectedGradientNMF(n_components=ncomps,sparseness='components',init='nndsvd')
                                  #nmf.fit(data_pcorr_fmri+100)
#comps=nmf.components_

