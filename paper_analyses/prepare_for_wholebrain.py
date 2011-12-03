#!/usr/bin/env python
""" prepare_for_wholebrain.py - get data into npy packages for
whole brain classification on openfmri data
"""

import numpy as N
import nibabel as nib

datafile=['/scratch/01329/poldrack/openfmri/analyses/paper_analysis/1_melodic/run1_melodic_zstats.nii.gz','/scratch/01329/poldrack/openfmri/analyses/paper_analysis/1_melodic/run2_melodic_zstats.nii.gz']

infofile=['/scratch/01329/poldrack/openfmri/analyses/paper_analysis/1_melodic/filelist_run1.txt','/scratch/01329/poldrack/openfmri/analyses/paper_analysis/1_melodic/filelist_run2.txt']

def get_info(infofile):
    f=open(infofile,'r')
    info=[]
    for i in f.readlines():
        subinfo=i.strip().replace('.nii.gz','').split('/')[-1].split('_')[0:5]
        info.append(subinfo)
    return info

for run in range(2):
    tasklabelfile=open('tasklabels_run%d.txt'%int(run+1),'w')
    sublabelfile=open('sublabels_run%d.txt'%int(run+1),'w')
    
    info=get_info(infofile[run])
    tasklabel=[]
    sublabel=[]
    for f in info:
        tasklabel.append(f[0]+f[2])
        tasklabelfile.write(f[0]+f[2]+'\n')
        sublabel.append(f[1])
        sublabelfile.write(f[1]+'\n')
    tasklabelfile.close()
    sublabelfile.close()
    
    
# now load the data files and save to numpy arrays

mask='/work/01329/poldrack/software_lonestar/fsl/data/standard/MNI152_T1_2mm_brain_mask.nii.gz'

maskimg=nib.load(mask)
maskdata=maskimg.get_data()
maskvox=N.where(maskdata)

for d in range(len(datafile)):
    dataimg=nib.load(datafile[d])
    data=dataimg.get_data()[maskvox]
    N.save('zstat_run%d.npy'%int(d+1),data)
    
    
