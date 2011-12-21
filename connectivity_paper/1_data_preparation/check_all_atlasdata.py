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

basedir=os.path.abspath(os.curdir)

flist=run_shell_cmd('find . -name "res4d_sc.txt"')

roidata={}
nbadrois={}
missingcount=N.zeros(305)

for f in flist:
    f_s=f.split('/')
    ds=f_s[1]
    if not roidata.has_key(ds):
        roidata[ds]={}
    sub=int(f_s[2][3:6])
    if not roidata[ds].has_key(sub):
        roidata[ds][sub]={}
    model=int(f_s[4][5:8])
    if not roidata[ds][sub].has_key(model):
        roidata[ds][sub][model]={}
    task=int(f_s[5][4:7])
    if not roidata[ds][sub][model].has_key(task):
        roidata[ds][sub][model][task]={}
    run=int(f_s[5][11:14])
    if not roidata[ds][sub][model][task].has_key(run):
        roidata[ds][sub][model][task][run]={}
    
    data=N.genfromtxt(f)
    roidata[ds][sub][model][task][run]['data']=data
    roidata[ds][sub][model][task][run]['shape']=data.shape
    s=N.sum(data,0)
    roidata[ds][sub][model][task][run]['badrois']=N.where(s==0)[0]
    if not nbadrois.has_key(len(N.where(s==0)[0])):
        nbadrois[len(N.where(s==0)[0])]=1
    else:
        nbadrois[len(N.where(s==0)[0])]+=1
    for i in N.where(s==0)[0]:
        missingcount[i]+=1


goodcols=N.where(missingcount<10)
N.save('scatlas_goodcols.npy',goodcols)
