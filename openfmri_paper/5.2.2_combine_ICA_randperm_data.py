import numpy as N
import pickle

basedir='/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_Dec2012/'
melodic_dir='/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_Dec2012/ICA/'
outdir=os.path.join(basedir,'classifier/')

acc={}
for run in range(1000):
    f=open(os.path.join(outdir,'randlabel/ICA_classifier_accuracy_run%05d.pkl'%run),'rb')
    acc[run]=pickle.load(f)
    f.close()

