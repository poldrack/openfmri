#!/usr/bin/env python
"""  melodic_setup.py - set up data for melodic analysis

1. specify which contrasts to use for each task (should use only run 1 for melodic, then we can run the classifier on run 2)

"""

from openfmri_utils import *
from run_shell_cmd import *

import os
import re

# specify contrasts

datadir='/scratch/01329/poldrack/openfmri/shared/zstats/'
analysisdir='/scratch/01329/poldrack/openfmri/analyses/paper_analysis/1_melodic/'
c=load_contrasts(analysisdir+'task_contrast_list_for_melodic.txt')

filelist=[]

allzstats=os.listdir(datadir)
mf=open('merge_data.sh','w')

for r in range(1,3):
    filelist=[]
    for ds in c.iterkeys():
        for task in c[ds].iterkeys():
            zs=c[ds][task][0].replace('contrast','zstat')
            for f in allzstats:
                if re.match('%s_subctr[0-9]*_%s_run%03d_%s.nii.gz'%(ds,task,r,zs),f):
                    filelist.append(datadir+f)

    cmd='fslmerge -t run%d_melodic_zstats '%r+' '.join(filelist)
    mf.write(cmd+'\n')


    of=open('filelist_run%d.txt'%r,'w')
    for i in filelist:
        of.write('%s\n'%i)
    of.close()
    
mf.close()

run_shell_cmd('sh merge_data.sh')

# run sh merge_run*_data.sh by hand

# need to make all voxels positive for melodic to work correctly

f=open('mk_add1000.sh','w')
for r in range(1,3):
    cmd='fslmaths run%d_melodic_zstats -add 1000 run%d_melodic_zstats_add1000\n'%(r,r)
    f.write(cmd)
f.close()

run_shell_cmd('sh mk_add1000.sh')

# melodic command:
# melodic -i 9tasks_add1000.nii.gz -o ica_9tasks_120comp -v --report --Oall -d 120 --nobet -m /scratch/01329/poldrack/fsl-4.1.7/data/standard/MNI152_T1_2mm_brain_mask.nii.gz

ncomps=[2,10,20,50,100,200]

f=open('run_melodic.sh','w')
for r in range(1,3):
  for c in ncomps:
    cmd='melodic -i run%d_melodic_zstats_add1000.nii.gz -o ica_run%d_%dcomp -v --report --Oall -d %d --nobet -m /work/01329/poldrack/software_lonestar/fsl/data/standard/MNI152_T1_2mm_brain_mask.nii.gz'%(r,r,c,c)
    f.write(cmd+'\n')
f.close()


print "now run: launch -s run_melodic -r 08:00:00 -n melodic -e 1way -p 144"
