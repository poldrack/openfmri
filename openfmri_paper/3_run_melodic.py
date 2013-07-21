#!/usr/bin/env python
"""  
run ICA on run 1 with varying dimensionalities

"""

from openfmri_utils import *
from run_shell_cmd import *

import os
import re



datadir='/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_May2013/data_prep'

outdir='/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_May2013/ICA'


# melodic command:
# melodic -i 9tasks_add1000.nii.gz -o ica_9tasks_120comp -v --report --Oall -d 120 --nobet -m /scratch/01329/poldrack/fsl-4.1.7/data/standard/MNI152_T1_2mm_brain_mask.nii.gz

ncomps=[2,10,20,50,100,200]

f=open('run_melodic_smoothed.sh','w')

for run in [1,2]:
  for c in ncomps:
    cmd='melodic -i %s/zstat_run%d_add10000_smoothed.nii.gz -o %s/ica_run%d_%dcomp -v --report --Oall -d %d --nobet -m /corral-repl/utexas/poldracklab/software_lonestar/fsl-5.0.1/data/standard/MNI152_T1_2mm_brain_mask.nii.gz --bgimage=/corral-repl/utexas/poldracklab/software_lonestar/fsl-5.0.1/data/standard/MNI152_T1_2mm_brain.nii.gz'%(datadir,run,outdir,run,c,c)
    f.write(cmd+'\n')
f.close()


print "now run: launch -s run_melodic_smoothed.sh -r 08:00:00 -n melodic -e 1way -p 72"
