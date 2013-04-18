"""
do some qa on the data files
"""

import nibabel
import os
import numpy as N
import matplotlib.pyplot as plt

outdir='/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_Dec2012/data_prep'
s={}
zmax={}
zmin={}

mask='/corral-repl/utexas/poldracklab/software_lonestar/fsl-5.0.1/data/standard/MNI152_T1_2mm_brain_mask.nii.gz'

m=nibabel.load(mask)
maskdata=m.get_data()

for run in [1]:
    print 'processing run ',run
    i=nibabel.load(os.path.join(outdir,'zstat_run%d.nii.gz'%run))
    d=i.get_data()

    data_inmask=d[maskdata>0]
    s[run]=N.std(data_inmask,0)
    zmax[run]=N.max(data_inmask,0)
    zmin[run]=N.min(data_inmask,0)
    

