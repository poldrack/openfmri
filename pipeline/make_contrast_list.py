""" create list of all contrasts for shared datasets"""

import os,sys
from openfmri_utils import *

#basedir='/corral/utexas/poldracklab/openfmri/shared/'
if len(sys.argv)>1:
    basedir=sys.argv[1]
else:
    basedir='./'
    
l=os.listdir(basedir)

studydirs=[x for x in l if x.find('ds')==0]

o=open(basedir+'all_study_conditions.txt','w')
for s in studydirs:
    condkey=load_condkey(basedir+s+'/condition_key.txt')
    custom_contrasts=[]
    if os.path.exists(basedir+s+'/task_contrasts.txt'):
        c=open(basedir+s+'/task_contrasts.txt','r')
        custom_contrasts=[i.split(' ')[0] for i in c.readlines()]
        c.close()
    for task in range(1,len(condkey)+1):
        nconds_orig=len(condkey[task])
        condkey[task][len(condkey[task])+1]='all_conds'
        for cc in custom_contrasts:
            condkey[task][len(condkey[task])+1]=cc.strip()
            
        for cond in range(1,len(condkey[task])+1):
            if cond<=nconds_orig:
                print '%s task%03d cond%03d cond:%s'%(s,task,cond,condkey[task][cond])
                o.write('%s task%03d cond%03d cond:%s\n'%(s,task,cond,condkey[task][cond]))
            elif cond==(nconds_orig+1):
                print '%s task%03d cond%03d %s'%(s,task,cond,condkey[task][cond])
                o.write('%s task%03d cond%03d %s\n'%(s,task,cond,condkey[task][cond]))
            else:
                print '%s task%03d cond%03d custom%03d:%s'%(s,task,cond,cond-nconds_orig-1,condkey[task][cond])
                o.write('%s task%03d cond%03d custom%03d:%s\n'%(s,task,cond,cond-nconds_orig-1,condkey[task][cond]))
o.close()
