"""
find all reg_standard/zstat images for the specified datasets and move
them into a common directory
- after running this script, need to launch get_all_zstats.sh
"""

import os
import numpy as N
from mvpa2.misc.fsl import read_fsl_design
from openfmri_utils import *
import pickle

studies=['ds001',
'ds002',
'ds003',
'ds005',
'ds006A',
'ds007',
'ds008',
'ds011',
'ds017A',
'ds051',
'ds052',
'ds101',
'ds102',
'ds107',
'ds108',
'ds109',
'ds110']


basedir='/corral-repl/utexas/poldracklab/openfmri/shared2'
outdir='/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_May2013/data_prep'

subctr=0
outfile=open('get_all_zstats.sh','w')
task_keys={}
condition_keys={}
contrasts={}

for study in studies:
    studydir='%s/%s/'%(basedir,study)
    task_keys[study]=load_taskkey(os.path.join(studydir,'task_key.txt'))
    condition_keys[study]=load_condkey(os.path.join(studydir,'models/model001/condition_key.txt'))
    contrasts[study]={}
    for t in task_keys[study].iterkeys():
        contrasts[study][t]=load_fsl_design_con(os.path.join(studydir,'sub001/model/model001/%s_run001.feat/design.con'%t))
    stdrs=os.listdir(studydir)
    subdirs=[x for x in stdrs if x.find('sub')==0]
    #if 0:
    for sd in subdirs:
        subctr+=1
        featdirs=[x for x in os.listdir(studydir+sd+'/model/model001') if x.find('.feat')>0]
        for f in featdirs:
            fd=studydir+sd+'/model/model001/'+f
            if os.path.exists(fd+'/design.fsf'):
                design=read_fsl_design(fd+'/design.fsf')
                ncontrasts=design['fmri(ncon_real)']
                for c in range(1,ncontrasts+1):
                    cmd='mv %s/reg_standard/stats/zstat%d.nii.gz %s/zstats/%s_subctr%03d_%s_zstat%03d.nii.gz'%(fd,c,basedir,study,subctr,f.replace('.feat',''),c)
                    #print cmd
                    outfile.write(cmd+'\n')
                    
outfile.close()

f=open(os.path.join(outdir,'task_keys.pkl'),'wb')
pickle.dump(task_keys,f)
f.close()

f=open(os.path.join(outdir,'task_contrasts.pkl'),'wb')
pickle.dump(contrasts,f)
f.close()

f=open(os.path.join(outdir,'task_conditions.pkl'),'wb')
pickle.dump(condition_keys,f)
f.close()

