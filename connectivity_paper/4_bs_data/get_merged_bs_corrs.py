#!/usr/bin/env python
""" compute correlations for merged betaseries files
"""

from get_partialcorr import get_partialcorr
import os,sys


colfile='/scratch/01329/poldrack/openfmri/shared2/scatlas_goodcols.npy'
bsdir='/scratch/01329/poldrack/openfmri/analyses/betaseries/'

bsfiles=[s for s in os.listdir(bsdir) if s.find('bs.txt')>1]

goodcols=N.load(colfile)

for f in bsfiles:
    d=N.genfromtxt(bsdir+f)
    if N.sum(N.mean(d[:,goodcols],0)==0.0)==0:
        get_partialcorr(bsdir+f,bsdir+f.replace('.txt',''),colfile)
