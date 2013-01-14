#!/usr/bin/env python

tbdir='/corral-repl/utexas/poldracklab/openfmri/tarballs'
basedir='/corral-repl/utexas/poldracklab/openfmri/shared2/'

import sys,os
from run_shell_cmd import *

try:
    datasets=[sys.argv[1]]
except:
    print 'USAGE: mk_tarballs.py <ds code>'
    sys.exit()
    
#datasets=['ds105']
#, 'ds002', 'ds003', 'ds005', 'ds006', 'ds007', 'ds008', 'ds011', 'ds017A', 'ds017B', 'ds018', 'ds051', 'ds052', 'ds101', 'ds102', 'ds105', 'ds107']

tarballs_to_make={'raw':1,'model':0}

for dataset in datasets:

    sublist=[s for s in os.listdir(basedir+dataset) if s.find('sub')==0]

    if tarballs_to_make['raw']==1:
        tarcmd='tar zcvf %s/%s_raw.tgz %s/models %s/*.txt '%(tbdir,dataset,dataset,dataset)

        for s in sublist:
            l=dataset+'/'+s
            tarcmd=tarcmd+'%s/behav %s/model/model*/onsets %s/BOLD/*/bold.nii.gz %s/anatomy/highres*.nii.gz %s/anatomy/inplane*.nii.gz %s/README* '%(l,l,l,l,l,l)

        print tarcmd
        run_shell_cmd(tarcmd)

    if tarballs_to_make['model']==1:
        tarcmd='tar zcvf %s/%s_models.tgz %s/models %s/*.txt '%(tbdir,dataset,dataset,dataset)

        for s in sublist:
            l=dataset+'/'+s
            tarcmd=tarcmd+'%s/model/model* %s/BOLD/*/bold_mcf.par* %s/README* '%(l,l,l)

        print tarcmd
        run_shell_cmd(tarcmd)

