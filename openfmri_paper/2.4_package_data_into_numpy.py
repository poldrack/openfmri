#!/usr/bin/env python
""" prepare_for_wholebrain.py - get data into npy packages for
whole brain classification on openfmri data

"""

import numpy as N
import nibabel as nib
import os

datadir='/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_May2013/data_prep'
datafile=[os.path.join(datadir,'zstat_run1.nii.gz'),os.path.join(datadir,'zstat_run2.nii.gz')]
infofile=[os.path.join(datadir,'data_key_run1.nii.gz'),os.path.join(datadir,'data_key_run2.nii.gz')]




mask=os.path.join(datadir,'goodvoxmask.nii.gz')


maskimg=nib.load(mask)
maskdata=maskimg.get_data()
maskvox=N.where(maskdata)

for d in range(len(datafile)):
    dataimg=nib.load(datafile[d])
    data=dataimg.get_data()[maskvox]
    
    N.save(os.path.join(datadir,'zstat_run%d.npy'%int(d+1)),data)
    
    
