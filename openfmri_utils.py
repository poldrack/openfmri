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

def load_condkey(condkeyfile):

    f=open(condkeyfile)
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
    return cond_info

def load_scankey(scankeyfile):
    f=open(scankeyfile)
    scankey={}
    for l in f.readlines():
        l_split=l.strip().split(' ')
        scankey[l_split[0]]=l_split[1]
    f.close()
    return scankey

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
