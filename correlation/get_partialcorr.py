import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
import rpy2.robjects.numpy2ri
import numpy as N

import os,sys


def main():
    datafile=sys.argv[1]
    outfilestem=sys.argv[2]
    try:
        colstouse=sys.argv[3]
        st=int(colstouse.split(':')[0])
        fi=int(colstouse.strip().split(':')[1])
        get_partialcorr(datafile,outfilestem,[st,fi])
    except:   
        get_partialcorr(datafile,outfilestem)
    
def get_partialcorr(datafile,outfilestem,colstouse=[]):

    data=N.genfromtxt(datafile)
    if colstouse:
        print 'using cols:'
        print colstouse
        data=data[:,colstouse[0]:colstouse[1]]
         
    corr=N.corrcoef(data.T)
    N.save(outfilestem+'_corr.npy',corr)
   
    corpcor=importr('corpcor')

    pcor_shrink=corpcor.pcor_shrink(rpy2.robjects.numpy2ri.numpy2ri(data))
    partialcorr_shrink=rpy2.robjects.numpy2ri.ri2numpy(pcor_shrink)
    N.save(outfilestem+'_regpcorr.npy',partialcorr_shrink)

    pcor=corpcor.pcor_shrink(rpy2.robjects.numpy2ri.numpy2ri(data),0)
    partialcorr=rpy2.robjects.numpy2ri.ri2numpy(pcor)
    N.save(outfilestem+'_pcorr.npy',partialcorr)



if __name__ == '__main__':
    main()
