
from sklearn.svm import LinearSVC,SVC
import pickle
import numpy as N
import sys,os
import os
from sklearn.multiclass import OneVsRestClassifier
from basedir import *

try:
    run=int(sys.argv[1])
except:
    run=1

basedir=BASEDIR


outdir=os.path.join(basedir,'classifier/subject_classifier')

labels1=N.loadtxt(os.path.join(basedir,'data_prep/data_key_run1.txt'))[:,1]
labels2=N.loadtxt(os.path.join(basedir,'data_prep/data_key_run2.txt'))[:,1]
N.random.shuffle(labels1)

print 'loading data...'
data1=N.load(os.path.join(basedir,'data_prep/zstat_run1_allgood.npy')).T


print 'training...'
clf=OneVsRestClassifier(LinearSVC()).fit(data1,labels1)

del data1

print 'loading test data...'
data2=N.load(os.path.join(basedir,'data_prep/zstat_run2_allgood.npy')).T

print 'predicting...'
pred=clf.predict(data2)
print 'Mean accuracy:',N.mean(pred==labels2)

#acc=N.mean(pred==labels2)
#N.savetxt(os.path.join(outdir,'subclass_rand_%03d.txt'%run),[acc])
