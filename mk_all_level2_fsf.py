basedir='/corral/utexas/poldracklab/openfmri/staged/'
outfile=open('mk_all_level2_fsf.sh','w')

featdirs=[]
subdirs={}

taskid_list=['ds006']

for taskid in taskid_list:
  for root,dirs,files in os.walk(basedir):
#    for f in files:
        if root.split('/')[-1].rfind('.feat')>-1 and root.find(taskid)>-1:
            featdirs.append(root)
            fs=featdirs[-1].split('/')
            subnum=int(fs[7].replace('sub',''))
            if not subdirs.has_key(subnum):
                subdirs[subnum]={}
            runnum=int(fs[9].split('_')[1].split('.')[0].replace('run',''))
            tasknum=int(fs[9].split('_')[0].replace('task',''))
            if not subdirs[subnum].has_key(tasknum):
                subdirs[subnum][tasknum]=[]
            subdirs[subnum][tasknum].append(runnum)

  for s in subdirs.iterkeys():
    for t in subdirs[s].iterkeys():
        mk_level2_fsf(taskid,s,t,subdirs[s][t],basedir)
