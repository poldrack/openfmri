#!/usr/bin/env python

from tsne import *
import numpy as N
import matplotlib.pyplot as plt

basedir='/Users/poldrack/data/openfmri/melodic/'

infodir='/Users/poldrack/data/openfmri/shared/'

X=N.genfromtxt(basedir+'melodic_mix')
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
for i in range(len(t)):
    x,y=t[i,:]
    plt.text(x,y,'%d'%dstask[copedata[i,0]][copedata[i,1]]) #,color=colors[i])

# print legend:
plt.savefig(basedir+'tsne_fig.pdf',format='pdf')
