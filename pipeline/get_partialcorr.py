#!/usr/bin/env python
""" compute partial correlation
"""

import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
import rpy2.robjects.numpy2ri
import numpy as N

import os,sys


def main():
    datafile=sys.argv[1]
    outfilestem=sys.argv[2]
    colstouse=sys.argv[3]
    get_partialcorr(datafile,outfilestem,colstouse)

    
def get_partialcorr(datafile,outfilestem,colsfile):

##     datafile='/scratch/01329/poldrack/openfmri/shared2/ds001/sub001/model/model001/task001_run001.feat/stats/res4d_sc.txt'
##     outfilestem='/scratch/01329/poldrack/openfmri/shared2/ds001/sub001/model/model001/task001_run001.feat/stats/res4d_sc'
##     colsfile='/work/01329/poldrack/software_lonestar/atlases/sc_HO_atlas_goodcols.npy'

    data=N.genfromtxt(datafile)
    colstouse=N.load(colsfile)[0]
    data=data[:,colstouse]
#    print data.shape
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
