#!/usr/bin/env python
""" atlasextraction.py: extract data for each ROI in an atlas image
USAGE: atlasextraction.py <featdir> <descriptor> <atlasimage>
"""
import nibabel as nib
import numpy as N
import os,sys
from run_shell_cmd import *
#from mvpa.misc.fsl.base import read_fsl_design

def mk_native_atlas(featdir,atlasfile,atlas_descriptor):
                    
    # make the atlas in native space if it doesn't exist
    # just use linear reg, as fnirt does goofy stuff
    nativeatlas=featdir+'/%s_native.nii.gz'%atlas_descriptor
    if not os.path.exists(nativeatlas):
        cmd='flirt -in %s -out %s -ref %s -applyxfm -init %s/reg/standard2example_func.mat -interp nearestneighbour'%(atlasfile,nativeatlas,featdir+'/example_func.nii.gz',featdir)
        run_shell_cmd(cmd)
    return nativeatlas



def extract_roi_means(datafile,atlasdata,outfilename):
    
    atlasrois=N.unique(atlasdata[atlasdata>0])
    nroi=N.max(atlasrois)+1

    img=nib.load(datafile)
    data=img.get_data()
    ntp=data.shape[3]

    roidata=N.zeros((nroi,ntp))
    for r in atlasrois:
        roivox=(atlasdata==r)
        roidata[r,:]=N.mean(data[roivox,:],0)
    roidata=roidata[1:,:].T
    
    N.savetxt(outfilename,roidata,delimiter='\t')
    return roidata


def main():
#if 1==1:
    
    #atlasfile='/work/01329/poldrack/code/poldrack/roi_atlas/sc_HO_atlas.nii.gz'
    #atlas_descriptor='sc_HO'
    bsmethod='lsone'
    featdir=sys.argv[1]
    atlas_descriptor=sys.argv[2]
    atlasfile=sys.argv[3]
    
     
    nativeatlas=mk_native_atlas(featdir,atlasfile,atlas_descriptor)
    atlas=nib.load(nativeatlas)
    atlasdata=atlas.get_data()

    # extract roi data from betaseries
    
    if os.path.exists(featdir+'/betaseries'):

        bsfiles_all=os.listdir(featdir+'/betaseries')
        bsfiles=['%s/betaseries/%s'%(featdir,f) for f in bsfiles_all if f.find(bsmethod)>-1 and f.find('nii.gz')>-1]
    #    print "files:"
    #    print bsfiles

        for bsf in bsfiles:
            roidata=extract_roi_means(bsf,atlasdata,bsf.replace('.nii.gz','_%s.txt'%atlas_descriptor))

    # now extract for residual
    residfile=featdir+'/stats/res4d.nii.gz'
    roidata_res4d=extract_roi_means(residfile,atlasdata,residfile.replace('.nii.gz','_%s.txt'%atlas_descriptor))

if __name__=='__main__':
    main()

