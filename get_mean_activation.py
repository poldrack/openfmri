#!/usr/bin/env python
"""
load the SCatlas and check how much of each ROI is activated for each study
in the openfmri database
"""

import nibabel as nib
import numpy as N
import openfmri_utils as ofu
import os

def get_atlas_activation(imgdata,atlasdata):
    atlasvals=[x for x in N.unique(atlasdata) if x > 0]
    proportion_active=N.zeros(len(atlasvals)+1)
    for roi in atlasvals:
        roivox=atlasdata==roi
        proportion_active[roi]=N.mean(imgdata[roivox]>0)
    return proportion_active
        
        
outbase='/scratch/01329/poldrack/openfmri/analyses/roi_activation/'
basedir='/scratch/01329/poldrack/openfmri/shared2/'
studies=['ds001','ds002','ds003','ds005','ds006','ds007','ds008','ds011','ds017A','ds051','ds052','ds101','ds102','ds105','ds107']
#studies=['ds001','ds002']
# load the atlas
atlasfile='/work/01329/poldrack/software_lonestar/atlases/sc_HO_atlas.nii.gz'
atlasimg=nib.load(atlasfile)
atlasdata=atlasimg.get_data()
try:
    activation_data.has_key('foo')
except:
  activation_data={}

  taskctr=0
  tasklabels=[]
  for s in studies:
    activation_data[s]={}
    print s
    condkey=ofu.load_condkey(basedir+s+'/models/model001/condition_key.txt')
    for task in condkey.keys():
        taskctr+=1
        tasklabels.append(s+'_%d'%task)
        activation_data[s][task]={}
        groupbase=os.path.join(basedir,s,'group/model001/task%03d'%task)
        groupbase_list=os.listdir(groupbase)
        gfeat_list=[x for x in groupbase_list if x.find('.gfeat')>0]
        for gfeat in gfeat_list:
            gfeatdir=os.path.join(groupbase,gfeat)
            featnum=int(gfeat[4:7])
#            print gfeatdir
            thresh_zstat_file=os.path.join(gfeatdir,'cope1.feat/thresh_zstat1.nii.gz')
            zstatimg=nib.load(thresh_zstat_file)
            zstatdata=zstatimg.get_data()
            activation_data[s][task][featnum]=get_atlas_activation(zstatdata,atlasdata)



roi_act=N.zeros(306)
ctr=0
tasklabels=[]
data=N.zeros((136,306))
for s in studies:
    condkey=ofu.load_condkey(basedir+s+'/models/model001/condition_key.txt')
    for task in condkey.keys():
        for c in activation_data[s][task].iterkeys():
            condlabel=s+'_%d_con%d'%(task,c)
            tasklabels.append(condlabel)
            data[ctr,:]=activation_data[s][task][c]
            ctr+=1
#            nrois=N.sum(data>0)
#            roi_act[N.where(data>0)]+=1
#            roimean=N.mean(data[data>0])
#            print '%s %d %d: %d rois, %f mean acc'%(s,t,c,nrois,roimean)

