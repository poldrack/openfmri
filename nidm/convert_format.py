# -*- coding: utf-8 -*-
"""
convert_format.py - convert to new openfmri fmri

Created on Wed Jan 28 15:42:54 2015

@author: poldrack
"""

import os,sys,glob
from run_shell_cmd import run_shell_cmd
import datetime

def logmsg(msg,logfile='conversion_log.txt'):
    f=open(logfile,'a')
    stamp=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    f.write("%s: %s\n"%(stamp,msg))
    f.close()

def run_and_log(cmd,logfile='conversion_log.txt'):
    run_shell_cmd(cmd)
    logmsg(cmd,logfile)

newdirnames=['functional','anatomy','behav','model']

basedir='/Users/poldrack/Dropbox/code/openfmri/nidm/ds007'
newdir='/Users/poldrack/Dropbox/code/openfmri/nidm/ds007_new'
if not os.path.exists(newdir):
    os.mkdir(newdir)
    logmsg('mkdir %s'%newdir)
    
subdirs=glob.glob(os.path.join(basedir,'sub*'))

for subdir in subdirs:
    try:
        assert os.path.exists(os.path.join(subdir,'BOLD'))
        assert os.path.exists(os.path.join(subdir,'anatomy'))
    except:
        print subdir,'does not appear to be a good subject dir'
        continue
    subcode=subdir.split('/')[-1]

    newsubdir=os.path.join(newdir,subcode)
    if not os.path.exists(newsubdir):
        os.mkdir(newsubdir)
        logmsg('mkdir %s'%newsubdir)
    for nd in newdirnames:
        snd=os.path.join(newsubdir,nd)
        if not os.path.exists(snd):
            os.mkdir(snd)
            logmsg('mkdir %s'%snd)
                
    # NB: for ds007, we don't have the task order available.  
    # so we will just use the existing ordering and mark timing as NA in
    # session key file

    funcdirs=glob.glob(os.path.join(subdir,'BOLD/*'))
    for funcdir in funcdirs:
        try:
            assert os.path.exists(os.path.join(funcdir,'bold.nii.gz'))
        except:
            print funcdir,'has no bold file'
    