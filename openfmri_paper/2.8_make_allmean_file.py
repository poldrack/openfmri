"""
make alist of all contrasts/tasks
"""

import pickle
from get_contrasts_to_use import *

c=get_contrasts_to_use()

outdir='/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_Dec2012/data_prep'
infodir='/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_Dec2012/data_prep'

f=open(os.path.join(infodir,'task_keys.pkl'),'rb')
task_keys=pickle.load(f)
f.close()

f=open(os.path.join(infodir,'task_contrasts.pkl'),'rb')
contrasts=pickle.load(f)
f.close()

f=open(os.path.join(infodir,'task_conditions.pkl'),'rb')
condition_keys=pickle.load(f)
f.close()

taskctr={'ds001': {1: 1},
 'ds002': {1: 2, 2: 3, 3: 4},
 'ds003': {1: 5},
 'ds005': {1: 6},
 'ds006A': {1: 7},
 'ds007': {1: 8, 2: 9, 3: 10},
 'ds008': {1: 11, 2: 12},
 'ds011': {1: 13, 2: 14, 3: 15, 4: 16},
 'ds017': {2: 17},
 'ds051': {1: 18},
 'ds052': {1: 19, 2: 20},
 'ds101': {1: 21},
 'ds102': {1: 22},
 'ds107': {1: 23}}

taskdict={}
for ds in taskctr.iterkeys():
    for t in taskctr[ds].iterkeys():
        taskdict[taskctr[ds][t]]=[ds,t,task_keys[ds]['task%03d'%t],c[ds][t][0],contrasts[ds]['task%03d'%t]['contrasts'][c[ds][t][0]]]

meanzstatdir='/corral-repl/utexas/poldracklab/openfmri/shared2/mean_zstat/'
outdir='/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_Dec2012/data_prep'

cmd='fslmerge -t %s/all_mean_zstat.nii.gz'%outdir
for t in range(1,24):
    cmd += ' %s/mean_%s_task%03d_zstat%d_run1.nii.gz'%(meanzstatdir,taskdict[t][0],taskdict[t][1],taskdict[t][3])

print cmd
    
