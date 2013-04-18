import numpy as N
import os
import pickle

def get_best_params():
    basedir='/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_April2013/'
    melodic_dir='/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_April2013/ICA/'
    outdir=os.path.join(basedir,'classifier')

    f=open(os.path.join(outdir,'ICA_classifier_accdata_paramest_run2.pkl'))
    param_opt=pickle.load(f)
    f.close()

    ncomp=[2, 10, 20, 50, 100, 200]
    svmparams=10.0**param_opt['svmparams']
    lrparams=10.0**param_opt['lrparams']
    rbfparams=10.0**param_opt['rbfparams']

    linsvm=N.zeros(len(ncomp))
    logreg=N.zeros(len(ncomp))
    rbfsvm=N.zeros((len(ncomp),2))

    for c in range(len(ncomp)):
        linsvm[c]=svmparams[N.argmax(param_opt['svm'][c,:])]
        logreg[c]=lrparams[N.argmax(param_opt['lr'][c,:])]
        rbfacc=param_opt['rbf'][c,:,:]
        rbfsvm[c,0]=svmparams[N.where(rbfacc==N.max(rbfacc))[0][0]]
        rbfsvm[c,1]=rbfparams[N.where(rbfacc==N.max(rbfacc))[1][0]]

    return linsvm,rbfsvm,logreg
