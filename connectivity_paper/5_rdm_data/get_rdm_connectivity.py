#!/usr/bin/env python
""" get connectivity matrices for rdm files
"""

import pickle
import os
import numpy as N
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
import rpy2.robjects.numpy2ri

rdmdir='/scratch/01329/poldrack/openfmri/analyses/rdm/'
colfile='/scratch/01329/poldrack/openfmri/shared2/scatlas_goodcols.npy'
goodcols=N.load(colfile)[0]
ncols=len(goodcols)
rdmfiles=[i for i in os.listdir(rdmdir) if i.find('pkl')>1]

corpcor=importr('corpcor')

for rdmfile in rdmfiles:
    print rdmfile
    f=open(rdmdir+rdmfile,'rb')
    rdm=pickle.load(f)
    f.close()
    ctr=0
    rdmdata=N.zeros((ncols,len(rdm[rdm.keys()[0]])))
    bad_data=0
    for fk in goodcols:
        if not rdm.has_key(float(fk)+1):
            bad_data=1
            print 'bad data'
            continue
        else:
            rdmdata[ctr,:]=rdm[float(fk)+1]
            ctr=ctr+1
    # get rid of NaNs
    goodvox=N.where(N.sum(~N.isnan(rdmdata),0))[0]
    rdmdata=rdmdata[:,goodvox]
    if bad_data==0:
        rdmcorr=N.corrcoef(rdmdata)
        N.save(rdmdir+rdmfile.replace('rdm.pkl','rdmcorr.npy'),rdmcorr)
        pcor_shrink=corpcor.pcor_shrink(rpy2.robjects.numpy2ri.numpy2ri(rdmdata.T))
        partialcorr_shrink=rpy2.robjects.numpy2ri.ri2numpy(pcor_shrink)
        N.save(rdmdir+rdmfile.replace('rdm.pkl','rdm_regpcorr.npy'),partialcorr_shrink)

    
