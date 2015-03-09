#!/usr/bin/env python

tbdir='/corral-repl/utexas/poldracklab/openfmri/tarballs'
basedir='/corral-repl/utexas/poldracklab/openfmri/shared2'

import sys,os,glob
from run_shell_cmd import *

try:
    datasets=[sys.argv[1]]
except:
    print 'USAGE: mk_tarballs.py <ds code>'
    sys.exit()
    
#datasets=['ds105']
#, 'ds002', 'ds003', 'ds005', 'ds006', 'ds007', 'ds008', 'ds011', 'ds017A', 'ds017B', 'ds018', 'ds051', 'ds052', 'ds101', 'ds102', 'ds105', 'ds107']

tarballs_to_make={}
try:
    tarballs_to_make['raw']=int(sys.argv[2])
except:
    tarballs_to_make['raw']=1

try:
    tarballs_to_make['model']=int(sys.argv[3])
except:
    tarballs_to_make['model']=1

print tarballs_to_make

for dataset in datasets:

    sublist=[s for s in os.listdir(os.path.join(basedir,dataset)) if s.find('sub')==0]

    if tarballs_to_make['raw']==1:
        tarcmd='cd %s; tar zcvf %s/%s_raw.tgz '%(basedir,tbdir,dataset)

        for s in sublist:
            l=os.path.join(dataset,s)
            tarcmd=tarcmd+'%s/behav %s/model/model*/onsets  %s/BOLD/*/QA %s/BOLD/*/bold.nii.gz %s/anatomy/highres*.nii.gz %s/anatomy/inplane*.nii.gz %s/README* '%(l,l,l,l,l,l,l)

        print tarcmd
        run_shell_cmd(tarcmd)

    if tarballs_to_make['model']==1:
        tarcmd='tar zcvf %s/%s_models.tgz %s/models %s/*.txt '%(tbdir,dataset,dataset,dataset)

        for s in sublist:
            l=dataset+'/'+s
            tarcmd=tarcmd+'%s/model/model* %s/README* '%(l,l)

        print tarcmd
        run_shell_cmd(tarcmd)


    # now make checksum file
    if tarballs_to_make['raw']==1:
        checksumfile='%s/%s_raw_checksums.txt'%(tbdir,dataset)
        f=open(checksumfile,'w')
        tarcmd='tar ztf %s/%s_raw.tgz'%(tbdir,dataset)
        flist=run_shell_cmd(tarcmd)
        for i in flist:
            cscmd='md5sum %s'%i
            output=run_shell_cmd(cscmd)
            #print cscmd,output
            if len(output)>0:
                f.write(output[0]+'\n')
        f.close()

    if tarballs_to_make['model']==1:
        checksumfile='%s/%s_model_checksums.txt'%(tbdir,dataset)
        f=open(checksumfile,'w')
        tarcmd='tar ztf %s/%s_models.tgz'%(tbdir,dataset)
        flist=run_shell_cmd(tarcmd)
        for i in flist:
            cscmd='md5sum %s'%i
            output=run_shell_cmd(cscmd)
            #print cscmd,output
            if len(output)>0:
                f.write(output[0]+'\n')
        f.close()
