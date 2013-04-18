#!/usr/bin/env python
""" create classifier accuracy figure for openfmri paper
"""

import pickle
import numpy as N

import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt
from get_randperm_data import *

basedir='/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_April2013/classifier'

f=open(os.path.join(basedir,'ICA_classifier_accuracy.pkl'),'rb')
acc=pickle.load(f)
f.close()

randacc,randcut=get_randperm_data()

ncomp=['2','10','20','50','100','200']

plt.clf()
a=plt.axis([-0.5,6,0,0.7])
plt.plot(acc['svm'],'k-',label='Linear SVM',linewidth=2)
plt.hold(True)
plt.plot(acc['rbf'],'k--',label='RBF SVM',linewidth=2)
plt.plot(acc['lr'],'k:',label='Logistic regression',linewidth=2)


cltypes=['lr','svm','rbf']


plt.legend(loc='center right')

plt.plot(randcut['svm'],'k-')
plt.plot(randcut['rbf'],'k--')
plt.plot(randcut['lr'],'k:')

plt.ylabel('Classification accuracy')
plt.xlabel('# of ICA components')

plt.savefig(os.path.join(basedir,'classification_accuracy.pdf'))
