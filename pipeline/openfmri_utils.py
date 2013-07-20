
"""openfmri_utils: utility functions for openfmri project
"""
## Copyright 2011, Russell Poldrack. All rights reserved.

## Redistribution and use in source and binary forms, with or without modification, are
## permitted provided that the following conditions are met:

##    1. Redistributions of source code must retain the above copyright notice, this list of
##       conditions and the following disclaimer.

##    2. Redistributions in binary form must reproduce the above copyright notice, this list
##       of conditions and the following disclaimer in the documentation and/or other materials
##       provided with the distribution.

## THIS SOFTWARE IS PROVIDED BY RUSSELL POLDRACK ``AS IS'' AND ANY EXPRESS OR IMPLIED
## WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
## FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL RUSSELL POLDRACK OR
## CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
## CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
## SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
## ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
## NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
## ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import os
import glob
import numpy as N

r2z = lambda r: 0.5*(N.log(1+r)-N.log(1-r))

z2r = lambda z: (N.exp(2.0*z)-1)/(N.exp(2.0*z)+1)


def load_condkey(condkeyfile):

    f=open(condkeyfile)
    cond_info={}
    for l in f.readlines():
        l_s=l.strip().replace('\t',' ').split(' ')
        if len(l_s)<2:
            continue
        t=int(l_s[0].replace('task',''))
        cond=int(l_s[1].replace('cond',''))
        condname=' '.join(l_s[2:])
        if not cond_info.has_key(t):
            cond_info[t]={}
        cond_info[t][cond]=condname
    f.close()
    return cond_info

def load_scankey(scankeyfile):
    f=open(scankeyfile)
    scankey={}
    for l in f.readlines():
        l_split=l.strip().replace('\t',' ').split(' ')
        scankey[l_split[0]]=l_split[1]
    f.close()
    return scankey

def load_taskkey(taskkeyfile):
    f=open(taskkeyfile)
    taskkey={}
    for l in f.readlines():
        l_split=l.strip().replace('\t',' ').split(' ')
        taskkey[l_split[0]]='_'.join(l_split[1:])
    f.close()
    return taskkey

def load_contrastkey(contrastkeyfile):
    f=open(contrastkeyfile)
    contrastkey={}
    for l in f.readlines():
        l_split=l.strip().replace('\t',' ').split(' ')
        if not contrastkey.has_key(l_split[1]):
            contrastkey[l_split[1]]={}

        contrastkey[l_split[1]][l_split[2]]=l_split[3:]
    f.close()
    return contrastkey

def load_contrasts(contrastfile):
    if not os.path.exists(contrastfile):
        return {}
    f=open(contrastfile)
    contrasts={}
    for l in f.readlines():
        l_split=l.strip().replace('\t',' ').split(' ')
        if not contrasts.has_key(l_split[0]):
            contrasts[l_split[0]]={}
        contrasts[l_split[0]][l_split[1]] = l_split[2:]
    f.close()
    return contrasts

def check_featdir(featdir,verbose=0):
    if verbose==1:
        print 'checking %s'%featdir
    feat_info={}
    feat_info['problem']=0
    feat_info['featdir']=featdir
    feat_info['exists']=1
    if not os.path.exists(featdir):
        print '%s does not exist!'%featdir
        feat_info['exists']=0
        feat_info['problem']=1
        return feat_info

    # does report.log exist?  if so, grab its contents
    if os.path.exists(featdir+'/report.log'):
        f=open(featdir+'/report.log')
        feat_info['report.log']=f.readlines()
        f.close()
        feat_info['problem']=1
        if verbose==1:
            print feat_info['report.log']
            
    # does stats dir exist?
    if not os.path.exists(featdir+'/stats'):
        if verbose==1:
            print 'PROBLEM: stats dir does not exist!'
        feat_info['stats']=0
        feat_info['problem']=1
    else:
        feat_info['stats']=1
        for root,dirs,files in os.walk(featdir+'/stats/'):
            feat_info['zstats']=0
            for f in files:
                if f.find('zstat')>-1:
                    feat_info['zstats']+=1
        if verbose==1:
            print 'found %d zstats'%feat_info['zstats']
        
    if not os.path.exists(featdir+'/reg/'):
        feat_info['reg']=0
    else:
        feat_info['reg']=1
        feat_info['std']=0
        feat_info['fnirt']=0
        if os.path.exists(featdir+'/reg/example_func2standard.nii.gz'):
            feat_info['std']=1
        if os.path.exists(featdir+'/reg/highres2standard_warp.nii.gz'):
            feat_info['fnirt']=1

    if feat_info['problem']==1:
        print 'PROBLEM: %s'%featdir
    return feat_info

def load_fsl_design_con(featdir):
    f=open(featdir+'/design.con','r')
    l=f.readlines()
    dcon={}
    dcon['contrasts']={}
    for line in l:
        l_split=line.strip().split('\t')
        if l_split[0].find('/ContrastName')==0:
            cnum=int(l_split[0].replace('/ContrastName',''))
            dcon['contrasts'][cnum]=l_split[1].replace('"','').replace(' ','')
        if l_split[0].find('/Matrix')<0:
            l_split[0]=l_split[0].lstrip('/')
            dcon[l_split[0]]=l_split[1:]
        else:
            break

    readcons=0
    dcon['contrast_vals']=[]
    for line in l:
        l_split=line.strip().split('\t')
        if l_split[0].find('/Matrix')>-1:
            readcons=1
            continue
        if readcons==1:
            dcon['contrast_vals'].append([float(x) for x in line.strip().split(' ')])

    
    return dcon





def get_openfmri_contrasts(dataset):
    basedir='/corral-repl/utexas/poldracklab/openfmri/shared2'

    contrasts={}
    contrast_files=glob.glob(os.path.join(basedir,dataset,'sub001/model/model001/task*_run001.feat/design.con'))
    for c in contrast_files:
        
        tasknum=int(c.split('task')[1].split('_')[0])
        contrasts[tasknum]=load_fsl_design_con(c)
        
    
    return contrasts


def load_fsl_design_con(infile):

    f=open(infile)
    data=[i for i in f.readlines() if i.find('/ContrastName')==0]
    f.close()

    contrasts={}
    for c in data:
        connum=int(c.split('\t')[0].replace('/ContrastName',''))
        conname=c.strip().split('\t')[1].replace('"','')
       # print connum,conname
        contrasts[connum]=conname
    
    return contrasts
