#!/bin/sh

fsl_glm -i /corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_Dec2012/data_prep/all_mean_zstat.nii.gz -d /corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_Dec2012/ICA_smoothed_6mm/ica_run1_20comp/melodic_IC.nii.gz -o /corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_Dec2012/ICA_smoothed_6mm/all_mean_run1_proj_20comp.txt --demean -m /corral-repl/utexas/poldracklab/software_lonestar/fsl-5.0.1/data/standard/MNI152_T1_2mm_brain_mask.nii.gz

