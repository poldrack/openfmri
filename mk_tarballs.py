#!/usr/bin/env python

tbdir='/corral/utexas/poldracklab/openfmri/tarballs'

import sys
from run_shell_cmd import *

#dataset=sys.argv[1]
dataset='ds107'

sublist='sublist_%s'%dataset

tarcmd='tar zcvf %s/%s.tgz '%(tbdir,dataset)

f=open(sublist,'r')
for l in f.readlines():
    l=l.strip().lstrip('./')
    l_s=l.split('/')
    subcode='%s_%s'%(l_s[0],l_s[1])
    cmd='cp %s/*_key.txt %s'%(l_s[0],l)
    print cmd
    run_shell_cmd(cmd)
    cmd='cp %s/README* %s'%(l_s[0],l)
    print cmd
    run_shell_cmd(cmd)
    tarcmd=tarcmd+'%s/behav %s/BOLD/*/bold.nii.gz %s/anatomy/highres*.nii.gz %s/anatomy/inplane*.nii.gz %s/README* %s/*key.txt '%(l,l,l,l,l,l)
f.close()
print cmd
run_shell_cmd(tarcmd)

