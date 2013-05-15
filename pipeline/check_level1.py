#!/usr/bin/env python
"""
check all level1 models
"""


import glob
import os,sys
from featdir import Featdir

if len(sys.argv)>1:
    modelnum=int(sys.argv[1])
else:
    modelnum=1
    
exclude_warnings=['at least one EV is (close to) a linear combination ','VIF over threshold']
featdirs=glob.glob('sub*/model/model%03d/*.feat'%modelnum)

good_data={}
subs=[]
for f in featdirs:
    subcode=f.split('/')[0]
    if not subcode in subs:
        subs.append(subcode)
        print 'processing',subcode
    print 'checking %s'%f
    taskname,runname=os.path.basename(f).replace('.feat','').split('_')
    tasknum=int(taskname.replace('task',''))
    runnum=int(runname.replace('run',''))
    #print f,tasknum,runnum
    try:
        featdir=Featdir(f)
    except:
        print 'LOAD ERROR: %s'%f
        continue
    featdir.run_all_checks()
    warnings=[]
    for w in featdir.warnings:
        keep_warning=True
        for e in exclude_warnings:
            if w.find(e)>-1:
                keep_warning=False
        if keep_warning:
            warnings.append(w)
    if not len(warnings)==0:
        print 'PROBLEM: with %s'%f
#        for w in warnings:
#                 print w
    else:
        if not good_data.has_key(tasknum):
            good_data[tasknum]={}
        if not good_data[tasknum].has_key(runnum):
            good_data[tasknum][runnum]=0
        good_data[tasknum][runnum]+=1

print ''
print len(subs),' subs found (model %d)'%modelnum
for task in good_data.keys():
    for run in good_data[task].keys():
        print 'task%03d_run%03d: %d good featdirs'%(task,run,good_data[task][run])
#print good_data
