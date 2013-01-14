
BASEDIR='/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_Dec2012/data_prep/'
MASK='/corral-repl/utexas/poldracklab/software_lonestar/fsl-5.0.1/data/standard/MNI152_T1_2mm_brain_mask.nii.gz'

fslmaths ${BASEDIR}/zstat_run1.nii.gz -add 10000 -mul $MASK ${BASEDIR}/zstat_run1_add10000.nii.gz
fslmaths ${BASEDIR}/zstat_run2.nii.gz -add 10000 -mul $MASK  ${BASEDIR}/zstat_run2_add10000.nii.gz