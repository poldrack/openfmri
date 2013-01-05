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

clustering_type='average'

dataprepdir='/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_Dec2012/data_prep'
datadir='/corral-repl/utexas/poldracklab/openfmri/shared2/mean_zstat'
outdir='/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_Dec2012/clustering'
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
            
nconds=ctr

mask=nib.load(os.path.join(dataprepdir,'goodvoxmask.nii.gz'))
maskvox=N.where(mask.get_data()>0)
              
data=N.zeros((nconds,len(maskvox[0])))

ctr=0
for ds in contrasts_to_use.iterkeys():
    for task in contrasts_to_use[ds].iterkeys():
        for contrast in contrasts_to_use[ds][task]:
            tmp=nib.load(os.path.join(datadir,'mean_%s_task%03d_zstat%d_run1.nii.gz'%(ds,task,contrast))).get_data()
            data[ctr,:]=tmp[maskvox]
            ctr+=1

l=fastcluster.linkage(data,method=clustering_type,metric='euclidean')

plot_data=True
if plot_data:
    plt.figure(figsize=(16,10))
    plt.hold(True)
    dendrogram(l,labels=contrast_labels,orientation='right')
    #plt.show()
    plt.savefig(os.path.join(outdir,'cluster_figure_%s.pdf'%clustering_type),format='pdf')
