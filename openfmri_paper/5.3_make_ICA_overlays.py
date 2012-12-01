#!/usr/bin/env python

import os

icadir='/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_Dec2012/ICA/ica_run2_20comp/'
anatimg='/corral-repl/utexas/poldracklab/software_lonestar/fsl-5.0.1/data/standard/MNI152_T1_2mm_brain.nii.gz'

basedir='/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_Dec2012/'

outdir=os.path.join(basedir,'ICA/ICA_components_figure/')


for v in range(1,21):
    cmd='overlay 0 0 %s -a  %s/stats/thresh_zstat%d.nii.gz 2 6 %s/rend%04d'%(anatimg,icadir,v,outdir,v)
    print cmd
    cmd='slicer %s/rend%04d -S 5 100 %s/comp%04d.png'%(outdir,v,outdir,v)
    print cmd

cmd='pngappend '
for v in range(1,21):
    cmd=cmd+' %s/comp%04d.png +'%(outdir,v)
cmd=cmd.rstrip('+')
cmd=cmd + ' %s/all_comps.png'%outdir
print cmd
