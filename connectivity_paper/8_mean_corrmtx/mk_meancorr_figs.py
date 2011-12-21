#!/usr/bin/env python
"""
make mean corrmtx figures
"""

import numpy as N
import pickle
import matplotlib.pyplot as plt
from openfmri_utils import *

def get_symm_mean(m):
    """ get mean of upper and lower triangles
    """
    tmp=N.zeros(m.shape)
    for i in range(m.shape[0]):
        for j in range(m.shape[0]):
            if i==j:
                tmp[i,j]=tmp[j,i]=0
            else:
                tmp[i,j]=tmp[j,i]=N.mean([m[i,j],m[j,i]])
    return tmp
    



#ctypes=['corr','regpcorr']


triu=N.triu_indices(296,1)
ncorr=triu[0].shape[0]

ucla_dti=N.genfromtxt('UCLA305_avg.txt')
ucla_dti=get_symm_mean(ucla_dti)
ucla_dti_triu=ucla_dti[triu]


for ctype in ['regpcorr']:
#for ctype in ['corr','regpcorr']:

    tasknames=[]
    tasknames.append('dti_ucla_triu')
    corrdata=ucla_dti_triu/N.max(ucla_dti_triu)

    tasknames.append('neurosynth')
    corrdata=N.vstack((corrdata,N.load('sc_HO_neurosynth_%s.npy'%ctype)[triu]))

    datafile=open('mean_resid_%s.pkl'%ctype,'r')
    meancorr=pickle.load(datafile)
    datafile.close()

    # find all tasks

    for k in meancorr.iterkeys():
        for t in meancorr[k].iterkeys():
            corrdata=N.vstack((corrdata,meancorr[k][t]))
            tasknames.append('resid_%s_task%03d'%(k,t))

            
    # now get betaseries
    datafile=open('mean_bs_%s.pkl'%ctype,'r')
    meancorr=pickle.load(datafile)
    datafile.close()

    for k in meancorr.iterkeys():
        for t in meancorr[k].iterkeys():
            corrdata=N.vstack((corrdata,meancorr[k][t]))
            tasknames.append('bs_%s_task%03d'%(k,t))


    N.save('corrdata_%s.npy'%ctype,corrdata)
    f=open('tasknames_%s.txt'%ctype,'w')
    for t in tasknames:
        f.write(t+'\n')
    f.close()
    
    cc=N.corrcoef(corrdata)
    mean_corrdata=z2r(N.mean(r2z(corrdata),0))
    cc[N.diag_indices(corrdata.shape[0])]=0
    mean_corrmtx=N.zeros((296,296))
    mean_corrmtx[triu]=mean_corrdata
    
    plt.clf()
    plt.imshow(mean_corrmtx,interpolation='nearest')
    plt.colorbar()
    plt.title('mean %s matrix'%ctype)
    plt.savefig('meancorr_%s_fig.pdf'%ctype,format='pdf')

    plt.clf()
    plt.imshow(cc,interpolation='nearest')
    plt.colorbar()
    plt.title('studycorr - %s'%ctype)
    plt.savefig('studycorr_%s_fig.pdf'%ctype,format='pdf')


