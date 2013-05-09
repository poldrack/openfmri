DATADIR="/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_May2013/data_prep"

SIGMA="2.94"

fslmaths ${DATADIR}/zstat_run1_add10000.nii.gz -s $SIGMA ${DATADIR}/zstat_run1_add10000_smoothed
fslmaths ${DATADIR}/zstat_run2_add10000.nii.gz -s $SIGMA ${DATADIR}/zstat_run2_add10000_smoothed