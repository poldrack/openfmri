""" read individual corr data files and put into a single numpy matrix
and arrange labels for classification
"""

from copy import deepcopy
import os
import numpy as N
import pickle

basedir='/scratch/01329/poldrack/openfmri/shared/correlations/'
bsdir=basedir+'betaseries/'
resdir=basedir+'resid/'
roisets=['tomtom','sc']
corrtypes=['corr','pcorr','regpcorr']

f=open(basedir+'resid_tasks_to_use.txt','r')
taskinfo={}
for l in f.readlines():
    l_s=l.strip().split(' ')
    if not taskinfo.has_key(l_s[0]):
        taskinfo[l_s[0]]={}
    if not taskinfo[l_s[0]].has_key(l_s[1]):
         taskinfo[l_s[0]][l_s[1]]={}
    if not taskinfo[l_s[0]][l_s[1]].has_key(l_s[2]) and int(l_s[2][5])<3:
         taskinfo[l_s[0]][l_s[1]][l_s[2]]=[]
    
       
f.close()

# first clean up to get rid of tasks without two good runs

taskinfo_good=deepcopy(taskinfo)

for ds in taskinfo.iterkeys():
    for task in taskinfo[ds].iterkeys():
        if len(taskinfo[ds][task])<2:
            taskinfo_good[ds].pop(task)
taskinfo=deepcopy(taskinfo_good)

for ds in taskinfo_good.iterkeys():
    if len(taskinfo_good[ds])<1:
        taskinfo.pop(ds)

# now load all data
ls=os.listdir(resdir)

residfiles={}
data={}
labels={}
for roi in roisets:
    residfiles[roi]=[]
    data[roi]={}
    labels[roi]={}
    for ct in corrtypes:
        data[roi][ct]={}
        labels[roi][ct]={}
        for runs in ['run001','run002']:
            labels[roi][ct][runs]=[]
            data[roi][ct][runs]=[]
    

# I will assume that each one has all three corr types
# so I just need to look at one of them to get the list
for f in ls:
    if f.find('_corr.npy')>0:
        f_s=f.strip().replace('sc_HO','sc').split('_')
        try:
            if taskinfo[f_s[0]][f_s[2]].has_key(f_s[3]):
                residfiles[f_s[5]].append(f.strip().replace('_corr.npy',''))
        except:
            pass


for roi in roisets:
    for f in residfiles[roi]:
        for ct in corrtypes:
            tmp=N.load(resdir+'%s_%s.npy'%(f,ct))
            f_s=f.split('_')
            data[roi][ct][f_s[3]].append(tmp[N.triu_indices(tmp.shape[0],1)])
            labels[roi][ct][f_s[3]].append('_'.join([f_s[0],f_s[2]]))
            
f=open('all_data_resid.pkl','wb')
pickle.dump(data,f)
f.close()

f=open('all_labels_resid.pkl','wb')
pickle.dump(labels,f)
f.close()

for roi in roisets:
    for ct in corrtypes:
        for run in ['run001','run002']:
            f=open(basedir+'resid_%s_%s_%s_labels.txt'%(roi,ct,run),'w')
            for i in labels[roi][ct][run]:
                f.write(i+'\n')
            f.close()
            tmp=N.zeros((len(data[roi][ct][run]),len(data[roi][ct][run][0])))
            for x in range(len(data[roi][ct][run])):
                tmp[x,:]=data[roi][ct][run][x]
            N.save(basedir+'resid_%s_%s_%s.npy'%(roi,ct,run),tmp)
