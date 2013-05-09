#!/usr/bin/env python
""" project image data into ICs
"""

import os
from basedir import *

ncomps=[2,10,20,50,100,200]
datadir=os.path.join(BASEDIR,'data_prep/')
icadir=os.path.join(BASEDIR,'ICA')


f=open('3.1.1_project_data_across_runs.sh','w')

for icarun in range(1,3):
  for datarun in range(1,3):
    for c in ncomps:
            
        cmd='fsl_glm -i %s/zstat_run%d_add10000.nii.gz -d %s/ica_run%d_%dcomp/melodic_IC.nii.gz -o %s/datarun%d_icarun%d_%dcomp.txt --demean -m /corral-repl/utexas/poldracklab/software_lonestar/fsl-5.0.1/data/standard/MNI152_T1_2mm_brain_mask.nii.gz'%(datadir,datarun,icadir,icarun,c,icadir,datarun,icarun,c)
        f.write(cmd+'\n')
f.close()
