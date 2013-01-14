import numpy as N
import os

# ds002
nsubs={'ds002':17,'ds003':13, 'ds005':16,'ds007':21,'ds008':15}


basedir='/corral/utexas/poldracklab/openfmri/shared/'

for task in nsubs.iterkeys():
    
    f=open(basedir+task+'/condition_key.txt')
    cond_info={}
    for l in f.readlines():
        l_s=l.strip().split(' ')
        t=int(l_s[0].replace('task',''))
        cond=int(l_s[1].replace('cond',''))
        condname=l_s[2]
        if not cond_info.has_key(t):
            cond_info[t]={}
        cond_info[t][cond]=condname
    f.close()


    for s in range(nsubs[task]):
        maxrun={}
        behavdir=basedir+task+'/sub%03d/behav'%int(s+1)
        # figure out the # of runs
        for root,dirs,files in os.walk(behavdir):
                for file in files:
                  if file.find('ons.txt')>-1:
                    f_s=file.split('_')
                    t=int(f_s[0].replace('task',''))
                    r=int(f_s[1].replace('run',''))
                    if not maxrun.has_key(t):
                        maxrun[t]=r
                    elif maxrun[t]<r:
                        maxrun[t]=r
            #print maxrun
        for tasknum in maxrun.iterkeys():
            for r in range(maxrun[tasknum]):
                bdir='%s/%s/sub%03d/behav/task%003d_run%03d'%(basedir,task,s+1,tasknum,r+1)
                print 'mkdir %s'%bdir
                print 'mv %s/task%03d_run%03d_behav.txt %s/behavdata.txt'%(behavdir,tasknum,r+1,bdir)
                for c in cond_info[tasknum].iterkeys():
                    print 'mv %s/task%03d_run%03d_%s_ons.txt %s/cond%03d.txt'%(behavdir,tasknum,r+1,cond_info[tasknum][c],bdir,c)
                print 'mv %s/task%03d_run%03d_behav.txt %s/behavdata.txt'%(behavdir,tasknum,r+1,bdir)
