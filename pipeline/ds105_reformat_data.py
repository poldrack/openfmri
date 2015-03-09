# reformat data from pymvpa shared dataset to openfmri format

import os
import nibabel
import shutil
from run_shell_cmd import *

s=4  # subject number

basedir='/corral/utexas/poldracklab/openfmri/inprocess/haxby/sub%03d/'%s


# set up directories
datadirs=['anatomy','behav','BOLD','model']
for d in datadirs:
    if not os.path.exists(basedir+d):
        os.mkdir(basedir+d)

# break BOLD data into separate runs
nruns=12
runlength=121

process_bold=1
if process_bold:
    bold=nibabel.load(basedir+'bold.nii.gz')
    bolddata=bold.get_data()
 
    for run in range(nruns):
        if not os.path.exists(basedir+'BOLD/task001_run%03d'%int(run+1)):
            os.mkdir(basedir+'BOLD/task001_run%03d'%int(run+1))

        start=run*runlength
        end=run*runlength + runlength+1
        rundata=bolddata[:,:,:,start:end]
        newimg=nibabel.Nifti1Image(rundata,bold.get_affine())
        newimg.to_filename(basedir+'BOLD/task001_run%03d/bold.nii.gz'%int(run+1))

# deface and move anatomy
process_anatomy=1
if process_anatomy:
    run_shell_cmd('deface.py %s/anat.nii.gz'%basedir)
    shutil.move('%s/anat_defaced.nii.gz'%basedir,'%s/anatomy/highres001.nii.gz'%basedir)


# create onset files
## from the original paper:
## Each time series began and ended with 12 s of rest and contained
## eight stimulus blocks of 24-s duration, one for each category,
## sep- arated by 12-s intervals of rest. Stimuli were present- ed
## for 500 ms with an interstimulus interval of 1500 ms. Repetitions
## of meaningful stimuli were pictures of the same face or object
## photographed from dif- ferent angles.

process_behav=1
stimdur=0.5
SOA=2

f=open(basedir+'labels.txt','r')
cond=[]
condrun=[]
foo=f.readline() # get rid of first line
for l in f.readlines():
    cond.append(l.strip().split(' ')[0])
    condrun.append(int(l.strip().split(' ')[1]))
f.close()

conditions_dict={'house':0,'scrambledpix':1,'cat':2,'shoe':3,'bottle':4,'scissors':5,'chair':6,'face':7}
block_onsets=range(12,433,36)
ntrialsperblock=12
if process_behav==1:
    for run in range(nruns):
        if not os.path.exists(basedir+'behav/task001_run%03d'%int(run+1)):
            os.mkdir(basedir+'behav/task001_run%03d'%int(run+1))

        # get the condition order
        start=run*runlength
        end=run*runlength + runlength+1
        runcond=cond[start:end]
        runcondorder=[]
        for r in runcond:
            if r=='rest':
                continue
            elif not runcondorder:
                 runcondorder.append(conditions_dict[r])               
            elif conditions_dict[r]==runcondorder[-1]:
                continue
            else:
                runcondorder.append(conditions_dict[r])
##         if run==8:
##             continue
        
        for c in range(8):
            f=open(basedir+'behav/task001_run%03d/cond%03d.txt'%(run+1,runcondorder[c]+1),'w')
            for t in range(ntrialsperblock):
                ons=block_onsets[c]+t*2.0
                f.write('%0.3f\t0.5\t1\n'%ons)
            f.close()
                   
