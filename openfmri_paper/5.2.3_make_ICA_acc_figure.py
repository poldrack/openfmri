#!/usr/bin/env python
""" create classifier accuracy figure for openfmri paper
"""

import pickle
import numpy as N

import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt

f=open('classifier_accuracy.pkl','rb')
acc=pickle.load(f)
f.close()
f=open('randperm_empirical_null_acc.pkl','rb')
randacc=pickle.load(f)
f.close()

ncomp=['2','10','20','50','100','200']

plt.clf()
a=plt.axis([-0.5,6,0,0.7])
plt.plot(acc['svm'],'k-',label='Linear SVM',linewidth=2)
plt.hold(True)
plt.plot(acc['rbf'],'k--',label='RBF SVM',linewidth=2)
plt.plot(acc['lr'],'k:',label='Logistic regression',linewidth=2)

f=open('randperm_empirical_null_acc.pkl','rb')
pickle.load(f)
f.close()
cltypes=['lr','svm','rbf']

ci={}

for c in cltypes:
    ci[c]=randacc[c][95,:]

plt.legend(loc='center right')

plt.plot(ci['svm'],'k-')
plt.plot(ci['rbf'],'k--')
plt.plot(ci['lr'],'k:')

plt.ylabel('Classification accuracy')
plt.xlabel('# of ICA components')

plt.savefig('classification_accuracy.pdf')
