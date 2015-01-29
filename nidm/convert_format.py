# -*- coding: utf-8 -*-
"""
convert_format.py - convert to new openfmri fmri

Created on Wed Jan 28 15:42:54 2015

@author: poldrack
"""

import os,sys,glob
from run_shell_cmd import run_shell_cmd
import datetime
import shutil
import numpy
from openfmri_utils import load_condkey

def logmsg(msg,logfile='conversion_log.txt'):
    f=open(logfile,'a')
    stamp=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    f.write("%s: %s\n"%(stamp,msg))
    f.close()

def run_and_log(cmd,logfile='conversion_log.txt'):
    run_shell_cmd(cmd)
    logmsg(cmd,logfile)

def convert_behavdata(infile,outfile):
    assert os.path.exists(infile)
    assert os.path.exists(os.path.dirname(outfile))
    behav=numpy.loadtxt(infile,skiprows=1)
    varnames=[i for i in open(infile).readline().strip().split()]
    print varnames

newdirnames=['functional','anatomy','behav','model']
# fieldnamp and diffusion do not exist for ds007 so don't generate them

basedir='/Users/poldrack/Dropbox/code/openfmri/nidm/ds007'
newdir=basedir+'_new'
if not os.path.exists(newdir):
    os.mkdir(newdir)
    logmsg('mkdir %s'%newdir)
    
condkey=load_condkey(os.path.join(basedir,'models/model001/condition_key.txt'))

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
                
    t1files=glob.glob(os.path.join(subdir,'anatomy/highres001*.nii.gz'))
    for t1file in t1files:
        newt1file=os.path.basename(t1file).replace('highres','%s_T1w_'%subcode)
        shutil.copy(t1file,os.path.join(newsubdir,'anatomy',newt1file))        
        logmsg('cp %s %s'%(t1file,os.path.join(newsubdir,'anatomy',newt1file)))

    # NB: for ds007, we don't have the task order available.  
    # so we will just use the existing ordering and mark timing as NA in
    # session key file
    # ultimately we want to use the order to determine rn number

    funcdirs=glob.glob(os.path.join(subdir,'BOLD/*'))
    funcdirs.sort()
    runctr=1
    
    for funcdir in funcdirs:
        try:
            assert os.path.exists(os.path.join(funcdir,'bold.nii.gz'))
        except:
            print funcdir,'has no bold file'
            continue
        tasknum=int(funcdir.split('/')[-1].split('_')[0].replace('task',''))
        origtaskcode=os.path.basename(funcdir)
        newfuncdirname=os.path.join(newsubdir,'functional/%s'%origtaskcode.replace('task','protocol'))
        runctr+=1
        if not os.path.exists(newfuncdirname):
            os.mkdir(newfuncdirname)
            logmsg('mkdir %s'%newfuncdirname)
        for file_to_copy in glob.glob(os.path.join(funcdir,'*')):
            shutil.copy(file_to_copy,'%s/%s_%s_bold.nii.gz'%(newfuncdirname,
                                                               subcode,origtaskcode.replace('task','protocol')))
            logmsg('cp %s %s/%s_%s_bold.nii.gz'%(file_to_copy,newfuncdirname,
                                                               subcode,origtaskcode.replace('task','protocol')))
    
        
        newbehavdatafile=os.path.join(newfuncdirname,'events.tsv')
        onsetdir=os.path.join(subdir,'model/model001/onsets',origtaskcode)
        onsfiles=glob.glob(os.path.join(onsetdir,'cond*.txt'))

        fullonsdata=None
        try:
            assert len(onsfiles)>0
        except:
            print 'no onset file for',subdir,origtaskcode
        condition=[]
        header=['onset','duration','condition']
        for onsfile in onsfiles:
            condnum=int(os.path.basename(onsfile)[4:7])
            condname=condkey[tasknum][condnum].replace(' ','_')
            header.append(condname)
            onsdata=numpy.loadtxt(onsfile)
            if len(onsdata.shape)>1:
                onsdata[:,2]=condnum
            else:
                onsdata[2]=condnum
                
            try:
                fullonsdata=numpy.vstack((fullonsdata,onsdata))
            except:
                fullonsdata=onsdata
        fullonsdata_idx=numpy.argsort(fullonsdata[:,0])
        fullonsdata=fullonsdata[fullonsdata_idx,:]
        for cond in range(4):
                condmatch=fullonsdata[:,2]==(cond+1)
                fullonsdata=numpy.hstack((fullonsdata,condmatch[:,numpy.newaxis]))

        numpy.savetxt(newbehavdatafile,fullonsdata,header='\t'.join(header),delimiter='\t',comments='')
    