outdir='/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_April2013/classifier/'

from run_shell_cmd import *
from scipy.stats import scoreatpercentile
import numpy as N
import os

cmd='cat %s/randlabel/*SVM*.txt > %s/all_svm_randlabel.txt'%(outdir,outdir)
run_shell_cmd(cmd)

data=N.loadtxt(os.path.join(outdir,'all_svm_randlabel.txt'))
print 'mean: ',N.mean(data)
print '95 pct: ',scoreatpercentile(data,95)
