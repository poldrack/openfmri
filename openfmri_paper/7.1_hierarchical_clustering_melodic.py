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

X=N.loadtxt('/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_Dec2012/ICA_smoothed_6mm/datarun1_icarun1_20comp.txt')

taskinfo=N.loadtxt('/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_Dec2012/data_prep/data_key_run1.txt')

dataprepdir='/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_Dec2012/data_prep'
datadir='/corral-repl/utexas/poldracklab/openfmri/shared2/mean_zstat'
outdir='/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_Dec2012/clustering'

conds=N.unique(taskinfo[:,0])
nconds=len(conds)
f=open(os.path.join(dataprepdir,'task_contrasts.pkl'),'rb')
contrasts=pickle.load(f)
f.close()

contrasts_to_use=get_contrasts_to_use()
contrast_labels=[]
contrast_labels_short=[]

ctr=0
for ds in contrasts_to_use.iterkeys():
    for task in contrasts_to_use[ds].iterkeys():
        for contrast in contrasts_to_use[ds][task]:
            contrast_labels.append(ds+'_task%d:%s'%(task,contrasts[ds]['task%03d'%task]['contrasts'][contrast]))
            contrast_labels_short.append(ds+'_t%d_z%d'%(task,contrast))
            
            ctr+=1
            


              
data=N.zeros((nconds,X.shape[1]))

for c in range(len(conds)):
    condidx=taskinfo[:,0]==conds[c]
    data[c,:]=N.mean(X[condidx,:],0)

l=fastcluster.linkage(data,method=clustering_type,metric='euclidean')

plot_data=True
if plot_data:
    plt.figure(figsize=(16,10))
    plt.hold(True)
    dendrogram(l,labels=contrast_labels,orientation='right')
    #plt.show()
    plt.savefig(os.path.join(outdir,'ICA_cluster_figure_%s.pdf'%clustering_type),format='pdf')
