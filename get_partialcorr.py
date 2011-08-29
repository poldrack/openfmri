import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
import rpy2.robjects.numpy2ri
import numpy as N

import os,sys


def main():
    datafile=sys.argv[1]
    outfilestem=sys.argv[2]
    get_partialcorr(datafile,outfilestem)
    
def get_partialcorr(datafile,outfilestem):

    data=N.genfromtxt(datafile)
    
    c=N.cov(data)
    corr=N.corrcoef(data)
    
    corpcor=importr('corpcor')
##     glasso=importr('glasso')

##     g=glasso.glassopath(rpy2.robjects.numpy2ri.numpy2ri(c),approx=1,rholist=rpy2.robjects.numpy2ri.numpy2ri(N.arange(0,1.1,0.1)))

##     wi=rpy2.robjects.numpy2ri.ri2numpy(g.rx2('wi'))
    
##     N.save(outfilestem+'_glassopath.npy',wi)

    pcor_shrink=corpcor.pcor_shrink(rpy2.robjects.numpy2ri.numpy2ri(data.T))
    partialcorr_shrink=rpy2.robjects.numpy2ri.ri2numpy(pcor_shrink)
    N.save(outfilestem+'_regpcorr.npy',partialcorr_shrink)

    pcor=corpcor.pcor_shrink(rpy2.robjects.numpy2ri.numpy2ri(data.T),0)
    partialcorr=rpy2.robjects.numpy2ri.ri2numpy(pcor)
    N.save(outfilestem+'_pcorr.npy',partialcorr)

    N.save(outfilestem+'_corr.npy',corr)


if __name__ == '__main__':
    main()
