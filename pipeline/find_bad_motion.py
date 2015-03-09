"""
look at length of scrubvols and find
images that have too many bad vols
"""

import os,sys,glob
import numpy

thresh=0.33
verbose=False

cf=glob.glob('sub*/BOLD/*/QA/confound.txt')
for c in cf:
    data=numpy.loadtxt(c)
    nbadvols=data.shape[1]-14
    nvols=data.shape[0]
    pctbadvols=float(nbadvols)/float(nvols)
    if verbose:
        print pctbadvols,nbadvols,c
    if pctbadvols>thresh:
        print '# REJECT: ',pctbadvols,c
        runcode=c.split('/')[2]
        subcode=c.split('/')[0]
        print 'rm -rf %s/model/model001/%s.feat'%(subcode,runcode)
