"""
load searchlights from randomized image and
get max across entire brain
"""

import numpy as N
import nibabel as nib
import os
import scipy.stats

nruns=500

datadir='/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_Dec2012/classifier/searchlight_rand'

mask='/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_Dec2012/data_prep/goodvoxmask.nii.gz'
maskimg=nib.load(mask)
maskdata=maskimg.get_data()
maskvox=maskdata>0

max_stats=N.zeros(nruns)

for i in range(nruns):
    imgfile=os.path.join(datadir,'searchlight_randlabel_radius5_%d.nii.gz'%i)
    img=nib.load(imgfile)
    data=img.get_data()*-1.0 + 1.0
    max_stats[i]=N.max(data[maskvox])
    
print '95% max :',scipy.stats.scoreatpercentile(max_stats,95)
