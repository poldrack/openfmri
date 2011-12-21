#!/usr/bin/env python
""" atlasextraction_neurosynth.py: extract data for each ROI from neurosynth
"""
import nibabel as nib
import numpy as N
import os,sys
from run_shell_cmd import *




def extract_roi_means(datafile,atlasdata,outfilename,nroi=305):
    
    img=nib.load(datafile)
    data=img.get_data()
    ntp=data.shape[3]

    roidata=N.zeros((nroi,ntp))
    for r in range(nroi):
        roivox=(atlasdata==r+1)
        if N.sum(roivox)>0:
            roidata[r,:]=N.mean(data[roivox,:],0)
    roidata=roidata.T
    
    N.savetxt(outfilename,roidata,delimiter='\t')
    return roidata



if 1==1:
    
    atlasfile='/work/01329/poldrack/software_lonestar/atlases/sc_HO_atlas_3mm.nii.gz'
    colfile='/scratch/01329/poldrack/openfmri/shared2/scatlas_goodcols.npy'
    outfile='/scratch/01329/poldrack/textmining/network_analysis/sc_HO_neurosynth.txt'
    datafile='/scratch/01329/poldrack/textmining/data/all_peakimages.nii.gz'
    
    atlas_descriptor='sc_HO'

    atlas=nib.load(atlasfile)
    atlasdata=atlas.get_data()

    # extract roi data from betaseries
    

    roidata=extract_roi_means(datafile,atlasdata,outfile)


