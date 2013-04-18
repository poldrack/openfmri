"""
run hierarchical clustering on dataset

"""

import nibabel as nib
import numpy as N
import os
from get_contrasts_to_use import *
from sklearn.cluster import Ward
import fastcluster
import matplotlib.pyplot as plt
from hcluster import dendrogram
import pickle

clustering_type='ward'

X=N.loadtxt('/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_April2013/ICA/datarun1_icarun1_20comp.txt')

taskinfo=N.loadtxt('/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_April2013/data_prep/data_key_run1.txt')

dataprepdir='/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_April2013/data_prep'
#datadir='/corral-repl/utexas/poldracklab/openfmri/shared2/mean_zstat'
outdir='/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_April2013/clustering'

    
conds=N.unique(taskinfo[:,0])
nconds=len(conds)
f=open(os.path.join(dataprepdir,'task_contrasts.pkl'),'rb')
contrasts=pickle.load(f)
f.close()

contrasts_to_use=get_contrasts_to_use()
contrast_labels=[]
contrast_labels_short=[]

data=N.zeros((nconds,X.shape[1]))

for c in range(len(conds)):
    condidx=taskinfo[:,0]==conds[c]
    data[c,:]=N.mean(X[condidx,:],0)

l=fastcluster.linkage(data,method=clustering_type,metric='euclidean')

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

tasknums={}
for k in taskctr.iterkeys():
    for t in taskctr[k].iterkeys():
        tasknums[taskctr[k][t]]=k+' (%d): '%t+contrasts[k]['task%03d'%t][contrasts_to_use[k][t][0]]

for r in range(1,len(tasknums)+1):
    contrast_labels.append(tasknums[r])
    
plot_data=True
if plot_data:
    plt.figure(figsize=(10,10))
    plt.hold(True)
    d=dendrogram(l,labels=contrast_labels,orientation='right')
    #plt.show()
    plt.savefig(os.path.join(outdir,'ICA_cluster_figure_%s.pdf'%clustering_type),format='pdf')
