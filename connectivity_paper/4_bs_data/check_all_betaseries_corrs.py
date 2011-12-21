#!/usr/bin/env python
""" check all datasets for proper size of extracted atlas data

"""

import os,sys
from run_shell_cmd import *
import numpy as N
import pickle

def usage():
    """Print the docstring and exit with error."""
    sys.stdout.write(__doc__)
    sys.exit(2)

basedir='/scratch/01329/poldrack/openfmri/analyses/correlation/'

colfile='/scratch/01329/poldrack/openfmri/shared2/scatlas_goodcols.npy'
bsdir='/scratch/01329/poldrack/openfmri/analyses/betaseries/'

outdir='/scratch/01329/poldrack/openfmri/analyses/correlation/'
flist=[s for s in os.listdir(bsdir) if s.find('_corr.npy')>1]

goodcols=N.load(colfile)


corrtypes=['corr.npy','pcorr.npy','regpcorr.npy']

for ct in corrtypes:
    corrdata={}
    nbadrois={}
    roidata={}

    for f in flist:
        f=f.replace('_corr.npy','_'+ct)
        print f
        f_s=f.split('_')
        ds=f_s[0]
        if not roidata.has_key(ds):
            roidata[ds]={}
        sub=int(f_s[1][3:6])
        if not roidata[ds].has_key(sub):
            roidata[ds][sub]={}
        model=1
        if not roidata[ds][sub].has_key(model):
            roidata[ds][sub][model]={}
        task=int(f_s[2][4:7])
        if not roidata[ds][sub][model].has_key(task):
            roidata[ds][sub][model][task]={}
        run=int(f_s[3][3:6])
        if not roidata[ds][sub][model][task].has_key(run):
            roidata[ds][sub][model][task][run]={}

        data=N.load(bsdir+f)
        roidata[ds][sub][model][task][run]['data']=data[N.triu_indices(296,1)]
        s=N.sum(N.isnan(data))
        roidata[ds][sub][model][task][run]['nbadrois']=s
    f=open(basedir+'roidata_bs_%s.pkl'%ct.replace('.npy',''),'wb')
    pickle.dump(roidata,f)
    f.close()

    ## goodcols=N.where(missingcount<10)
    ## N.save('scatlas_goodcols.npy',goodcols)
