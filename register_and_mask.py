#!/usr/bin/env python
""" register image to whole-head MNI template and apply mask,
then register again to brain-only template
"""

import os,sys
from run_shell_cmd import *

ANTSPATH=os.environ['ANTSPATH']
FSLDIR=os.environ['FSLDIR']
test=False

#subdir='/corral/utexas/poldracklab/openfmri/shared/ds002/sub001/anatomy/'

def main():
    # first run N4 bias correction
    imgfile=sys.argv[1]
    subdir=imgfile.rstrip('highres001.nii.gz')
    if not os.path.exists(subdir):
        print '%s does not exist!'%subdir
        sys.exit(0)
        
    cmd='%sN4BiasFieldCorrection -i %s/highres001.nii.gz -d 3 -o %s/highres001_bfc.nii.gz  -c [50,0.0001]'%(ANTSPATH,subdir,subdir)

    print cmd
    if not test:
        run_shell_cmd(cmd,cwd=subdir)

    # then align bias-corrected whole-head image to template

    PARAMS="-r Gauss[3,0] -t SyN[0.25] -i 30x90x20 --use-Histogram-Matching --number-of-affine-iterations 10000x10000x10000x10000x10000 --rigid-affine false"

    template_wholehead='%s/data/standard/MNI152_T1_2mm.nii.gz'%FSLDIR
    template_brain='%s/data/standard/MNI152_T1_2mm_brain.nii.gz'%FSLDIR
    template_mask='%s/data/standard/MNI152_T1_2mm_brain_mask.nii.gz'%FSLDIR


    cmd='%sANTS 3 -m CC[%s,%shighres001_bfc.nii.gz,1,4] -o highres001_ANTS.nii.gz %s'%(ANTSPATH,template_wholehead,subdir,PARAMS)
    print cmd
    if not test:
        run_shell_cmd(cmd,cwd=subdir)


    # create a version of the MNI mask aligned to subject space

    cmd='WarpImageMultiTransform 3 %s %shighres001_brain_mask.nii.gz -R %shighres001.nii.gz -i %shighres001_ANTSAffine.txt %shighres001_ANTSInverseWarp.nii.gz --use-NN'%(template_mask,subdir,subdir,subdir,subdir)
    print cmd
    if not test:
        run_shell_cmd(cmd,cwd=subdir)

    cmd='fslmaths %shighres001.nii.gz -mul %shighres001_brain_mask.nii.gz %shighres001_brain.nii.gz'%(subdir,subdir,subdir)
    print cmd
    if not test:
        run_shell_cmd(cmd,cwd=subdir)

    # rerun warp from stripped highres to stripped template

    cmd='%sANTS 3 -m CC[%s,%shighres001_brain.nii.gz,1,4] -o highres001_ANTSstd.nii.gz %s'%(ANTSPATH,template_brain,subdir,PARAMS)
    print cmd
    if not test:
        run_shell_cmd(cmd,cwd=subdir)

    cmd='WarpImageMultiTransform 3 %shighres001_brain.nii.gz %shighres001_reg2std_ANTS.nii.gz -R %s %shighres001_ANTSWarp.nii.gz %shighres001_ANTSAffine.txt'%(subdir,subdir,template_brain,subdir,subdir)

    print cmd
    if not test:
        run_shell_cmd(cmd,cwd=subdir)

if __name__ == '__main__':
    main()
