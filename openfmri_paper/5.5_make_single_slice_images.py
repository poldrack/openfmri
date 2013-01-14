#!/usr/bin/env python

import os

icadir='/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_Dec2012/ICA_smoothed_6mm/ica_run1_20comp/'
anatimg='/corral-repl/utexas/poldracklab/software_lonestar/fsl-5.0.1/data/standard/MNI152_T1_2mm_brain.nii.gz'

basedir='/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_Dec2012/'

outdir=os.path.join(basedir,'ICA_smoothed_6mm/ICA_components_figure/')


for v in range(1,21):

    cmd='slicer %s/rend%04d -a %s/comp%04d_3axis.png'%(outdir,v,outdir,v)
    print cmd


