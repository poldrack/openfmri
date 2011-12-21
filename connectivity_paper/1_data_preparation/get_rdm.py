#!/usr/bin/env python
""" get_rdm.py: extract rdm for each ROI in an atlas image
USAGE: get_rdm.py <featdir> <descriptor> <atlasimage>
"""
import nibabel as nib
import numpy as N
import os,sys
from run_shell_cmd import *
#from mvpa.misc.fsl.base import read_fsl_design
import pickle


def extract_rdm(datafile,atlasdata):

## if 1==1:
##     datafile='/scratch/01329/poldrack/openfmri/shared/ds018/sub004/model/task002_run002+.feat/betaseries/ev1_lsone.nii.gz'
##     atlasfile='/scratch/01329/poldrack/openfmri/shared/ds018/sub004/model/task002_run002+.feat/tomtom_native.nii.gz'

##     atlas=nib.load(atlasfile)
##     atlasdata=atlas.get_data()
    
    atlasrois=N.unique(atlasdata[atlasdata>0])
    nroi=N.max(atlasrois)+1

    img=nib.load(datafile)
    data=img.get_data()
    rdmsize=data.shape[3]*(data.shape[3]-1)/2

    rdm={}
    roisize={}
    for r in atlasrois:
        if r==0:
            continue
        roivox=(atlasdata==r)
        roidata=data[roivox,:]
        roisize[r]=roidata.shape[0]
        if roidata.shape[0]>1:
            cc=N.corrcoef(roidata.T)
            rdm[r]=cc[N.triu_indices(cc.shape[0],1)]

    return rdm



def main():
#if 1==0:
    
    atlas_descriptor='sc'
    bsmethod='lsone'
    featdir=sys.argv[1]
    outdir='/scratch/01329/poldrack/openfmri/analyses/rdm/'
    nativeatlas=featdir+'/%s_native.nii.gz'%atlas_descriptor
    atlas=nib.load(nativeatlas)
    atlasdata=atlas.get_data()

    # extract roi data from betaseries
    
    if not os.path.exists(featdir+'/all_lsone.nii.gz'):
        print 'missing all_lsone for %s'%featdir
    else:

        bsf=featdir+'/all_lsone.nii.gz'

        rdm=extract_rdm(bsf,atlasdata)
        fd_s=featdir.split('/')
        outfname='%s_%s_%s_rdm.pkl'%(fd_s[1],fd_s[2],fd_s[5].replace('.feat',''))
        of=open(outdir+outfname,'wb')
        pickle.dump(rdm,of)
##         for x in rdm.iterkeys():
##             of.write('%d\t'%x)
##             for i in range(rdm[x].shape[0]):
##                 of.write('%f\t'%rdm[x][i])
##             of.write('\n')
        of.close()


if __name__=='__main__':
    main()

