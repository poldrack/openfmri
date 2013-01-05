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
import matplotlib.font_manager as mplfont
import pickle,os

X=N.loadtxt('/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_Dec2012/ICA/datarun1_icarun1_20comp.txt')

if os.path.exists('/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_Dec2012/tsne_ICA_20comps.pkl'):
    f=open('/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_Dec2012/tsne_ICA_20comps.pkl','rb')
    t=pickle.load(f)
    f.close()
else:
    t=tsne(X,no_dims=2, initial_dims=30,perplexity=10.0, max_iter=1000)
    f=open('/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_Dec2012/tsne_ICA_20comps.pkl','wb')
    pickle.dump(t,f)
    f.close()

taskinfo=N.loadtxt('/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_Dec2012/data_prep/data_key_run1.txt')

tasknums=N.unique(taskinfo[:,0])


# compute scatter for each task
t_eucdist={}
mean_t_obs={}
for k in tasknums:
    obs=N.where(taskinfo[:,0]==k)[0]
    t_obs=t[obs,:]
    mean_t_obs[k]=N.mean(t_obs,0)
    t_eucdist[k]=N.mean(N.sqrt((t_obs[:,0]-mean_t_obs[k][0])**2 + (t_obs[:,1]-mean_t_obs[k][1])**2 ))

plt.clf()
plt.axis([-90,125,-110,110])
plt.scatter(t[:,0],t[:,1],s=0)  # create axes
#f=open('tasklabels.txt','w')


for i in range(len(t)):
    x,y=t[i,:]
    plt.text(x,y,'%d'%taskinfo[i,0],fontsize=8,color='0.5') #,color=colors[i])
#    f.write('%d\n'%dstask[copedata[i,0]][copedata[i,1]])

for i in tasknums:
    plt.text(mean_t_obs[i][0],mean_t_obs[i][1],'%d'%i,fontsize=5 + t_eucdist[i]**0.8)
#f.close()
# print legend:
plt.savefig('/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_Dec2012/tsne/tsne_fig_ICA.pdf',format='pdf')
