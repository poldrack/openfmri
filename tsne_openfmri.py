#!/usr/bin/env python
""" tsne_openfmri.py: code to run t-SNE on results from MELODIC ICA applied to the OpenFMRI dataset

requires:
- tsne.py from http://homepage.tudelft.nl/19j49/t-SNE.html
- Numpy
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


from tsne import *
import numpy as N
import matplotlib.pyplot as plt

basedir='./data/'

X=N.genfromtxt(basedir+'melodic_mix_20comps')
copedata=N.genfromtxt(basedir+'copedata.txt')

usedata=N.zeros(len(copedata))
s=set(copedata[:,0])
# find max cope (all-trials) for each task
maxcope={}
for t in list(s):
    maxcope[t]=N.max(copedata[copedata[:,0]==t,2])

## for x in range(len(copedata)):
## #    if copedata[x,1]==1 and copedata[x,2]==maxcope[copedata[x,0]]:
##     if copedata[x,0]<100:
##         usedata[x]=1

all_trials_cope={2:{1:1,2:1,3:3},3:{1:3},5:{1:1},6:{1:6},7:{1:1,2:1,3:1},8:{1:2,2:2},11:{1:1,2:1,3:1,4:5},101:{1:5},102:{1:5}}

for x in range(len(copedata)):
    if copedata[x,2]==all_trials_cope[copedata[x,0]][copedata[x,1]]:
#    if copedata[x,1]==1:
        usedata[x]=1


copedata=copedata[usedata==1,:]

# get class labels
ctr=1
dstask={}
tasklabel={}
s=set(copedata[:,0])
for ds in list(s):
    dstask[ds]={}
    sdata=copedata[:,0]==ds
    stasks=set(copedata[sdata,1])
    for t in stasks:
        dstask[ds][t]=ctr
        print '%d: ds%03d task%03d'%(ctr,ds,t)
        ctr=ctr+1

# make colormap
cmap={}
ctr=0

for i in list(s):
    cmap[i]=ctr
    ctr+=1

colors=[cmap[i] for i in copedata[:,0]]

X=X[usedata==1,:]

t=tsne(X,no_dims=2, initial_dims=15, perplexity=10.0, max_iter=1000)
plt.clf()
plt.scatter(t[:,0],t[:,1],s=0)  # create axes
f=open(basedir+'tasklabels.txt','w')
for i in range(len(t)):
    x,y=t[i,:]
    plt.text(x,y,'%d'%dstask[copedata[i,0]][copedata[i,1]]) #,color=colors[i])
    f.write('%d\n'%dstask[copedata[i,0]][copedata[i,1]])
    
f.close()
# print legend:
plt.savefig(basedir+'tsne_fig.pdf',format='pdf')
