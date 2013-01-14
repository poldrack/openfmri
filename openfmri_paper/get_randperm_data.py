import numpy as N
import pickle
import os
from scipy.stats import scoreatpercentile

basedir='/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_Dec2012/'
melodic_dir='/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_Dec2012/ICA/'
outdir=os.path.join(basedir,'classifier/')

def get_randperm_data():
    allacc={'svm':N.zeros((1000,6)),'lr':N.zeros((1000,6)),'rbf':N.zeros((1000,6))}

    for run in range(1000):
        f=open(os.path.join(outdir,'randlabel/ICA_classifier_accuracy_run%05d.pkl'%run),'rb')
        acc=pickle.load(f)
        for k in allacc.keys():
            allacc[k][run,:]=acc[k]
        f.close()

    meanacc={}
    cutoff={}
    for k in allacc.keys():
        cutoff[k]=N.zeros(6)
        meanacc[k]=N.mean(allacc[k],0)
        for c in range(6):
            cutoff[k][c]=scoreatpercentile(allacc[k][:,c],95)
    return meanacc,cutoff
