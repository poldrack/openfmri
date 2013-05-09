
import nibabel
import os
import numpy as N

outdir='/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_May2013/data_prep'

mask='/corral-repl/utexas/poldracklab/software_lonestar/fsl-5.0.1/data/standard/MNI152_T1_2mm_brain_mask.nii.gz'

m=nibabel.load(mask)
maskdata=m.get_data()
maskvox=N.where(maskdata>0)

badsubthresh=3
run=2
if 1:
    print 'processing run ',run
    goodvox=N.zeros(maskdata.shape)
    missing_count=N.zeros(maskdata.shape)
    if 1:
        i=nibabel.load(os.path.join(outdir,'zstat_run%d.nii.gz'%run))
        d=i.get_data()
    for v in range(len(maskvox[0])):
        x=maskvox[0][v]
        y=maskvox[1][v]
        z=maskvox[2][v]
        if not N.sum(d[x,y,z,:]==0.0)>badsubthresh:
            goodvox[x,y,z]=1
        missing_count[x,y,z]= N.sum(d[x,y,z,:]==0.0)
    newimg=nibabel.Nifti1Image(goodvox,m.get_affine())
    newimg.to_filename(os.path.join(outdir,'zstat_run%d_goodvoxmask.nii.gz'%run))
    newimg=nibabel.Nifti1Image(missing_count,m.get_affine())
    newimg.to_filename(os.path.join(outdir,'zstat_run%d_missingcount.nii.gz'%run))
