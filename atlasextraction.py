""" atlasextraction.py: extract data for each ROI in an atlas image
"""
import nibabel as nib
import numpy as N
import os,sys
from run_shell_cmd import *

def main():
    
    atlasfile='/corral/utexas/poldracklab/data/roi_atlas/new_atlas.nii.gz'

    datafile=sys.argv[1]
    featdir=sys.argv[2]
    outfile=sys.argv[3]
    
#    datafile='/corral/utexas/poldracklab/openfmri/shared/ds002/sub002/model/task001_run001.feat/betaseries/ev1_lsone.nii.gz'
#    featdir='/corral/utexas/poldracklab/openfmri/shared/ds002/sub002/model/task001_run001.feat/'
#    outfile='/corral/utexas/poldracklab/openfmri/shared/ds002/sub002/model/task001_run001.feat/betaseries/ev1_scatlas_roidata.txt'


    # first make the atlas in native space if it doesn't exist
    # just use linear reg, as fnirt does goofy stuff
    nativeatlas=featdir+'/scatlas_native.nii.gz'
    cmd='flirt -in %s -out %s -ref %s -applyxfm -init %s/reg/standard2example_func.mat -interp nearestneighbour'%(atlasfile,nativeatlas,featdir+'/example_func.nii.gz',featdir)
    run_shell_cmd(cmd)

    atlas=nib.load(nativeatlas)
    atlasdata=atlas.get_data()

    atlasrois=N.unique(atlasdata[atlasdata>0])
    nroi=N.max(atlasrois)+1


    img=nib.load(datafile)
    data=img.get_data()
    ntp=data.shape[3]

    roidata=N.zeros((nroi,ntp))
    for r in atlasrois:
        roivox=(atlasdata==r)
        roidata[r,:]=N.mean(data[roivox,:],0)

    N.savetxt(outfile,roidata[1:,:],delimiter='\t')


if __name__=='__main__':
    main()

