#!/usr/bin/env python
"""
get mean correlation matrices
"""

import os,sys,pickle
from openfmri_utils import *
import numpy as N

ctypes=['corr','regpcorr']

datatypes=['resid','bs']

for ctype in ctypes:
  for dt in datatypes:
    datafile=open('roidata_%s_%s.pkl'%(dt,ctype),'r')
    data=pickle.load(datafile)
    datafile.close()
    
    triu=N.triu_indices(296,1)
    ncorr=triu[0].shape[0]
    model=1
    allcorr={}
    meancorr={}
    zctr={}

    for ds in data.iterkeys():
        allcorr[ds]={}
        zctr[ds]={}
        for sub in data[ds].iterkeys():
            for task in data[ds][sub][model].iterkeys():
                for run in data[ds][sub][model][task].iterkeys():
                    if N.sum(N.isnan(data[ds][sub][model][task][run]['data']))>0 or data[ds][sub][model][task][run]['nbadrois']>0:
                        print 'skipping %s sub%03d task%03d run%03d'%(ds,sub,task,run)
                    else:
                        if not allcorr[ds].has_key(task):
                            allcorr[ds][task]=r2z(data[ds][sub][model][task][run]['data'])
                            zctr[ds][task]=1
                        else:
                            allcorr[ds][task]=N.vstack((allcorr[ds][task],r2z(data[ds][sub][model][task][run]['data'])))
                            zctr[ds][task]+=1


        for task in allcorr[ds].iterkeys():
            if not meancorr.has_key(ds):
                meancorr[ds]={}
            meancorr[ds][task]=z2r(N.mean(allcorr[ds][task],0))

    f=open('mean_%s_%s.pkl'%(dt,ctype),'wb')
    pickle.dump(meancorr,f)
    f.close()
    f=open('all_z_%s_%s.pkl'%(dt,ctype),'wb')
    pickle.dump(allcorr,f)
    f.close()
    f=open('zctr_%s_%s.pkl'%(dt,ctype),'wb')
    pickle.dump(zctr,f)
    f.close()

