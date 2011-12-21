#!/usr/bin/env python
""" classify each dataset vs resting
using partial correlation matrices
"""

from sklearn import svm,linear_model
import numpy as N
from sklearn.cross_validation import StratifiedKFold
import pickle

datatype='resid'
outfile='classify_vs_resting.out'

load_data=1
if load_data==1:
    dataset=N.load('%s_data_for_classification.npy'%datatype)
    data_id=N.load('%s_data_labels.npy'%datatype)
    f=open('%s_taskkey.pkl'%datatype,'rb')
    taskkey=pickle.load(f)
    f.close()
    f=open('tasknames-desc.txt','r')
    taskdesc={}
    for i in f.readlines():
        i_s=i.strip().split('\t')
        taskdesc[i_s[0].replace('task00','')]=i_s[1]
    f.close()

rest_ds=N.where(data_id==1)[0]

f=open(outfile,'w')

accuracy={}
coefs=N.zeros((31,43660))
for ds in range(2,31):
    task_ds=N.where(data_id==ds)[0]
    X=dataset[N.hstack((rest_ds[0:len(task_ds)],task_ds)),:]
    Y=data_id[N.hstack((rest_ds[0:len(task_ds)],task_ds))]
    skf=StratifiedKFold(Y,6)

    predclass=N.zeros(Y.shape)
    cf=N.zeros((1,43660))
    for train,test in skf:
        X_train,X_test,Y_train,Y_test=X[train,:],X[test,:],Y[train],Y[test]
#        clf=svm.LinearSVC()
        clf=linear_model.LogisticRegression(penalty='l1',C=10.0)
        clf.fit(X_train,Y_train)
        cf=cf+clf.coef_
        predclass[test]=clf.predict(X_test)
    coefs[ds,:]=cf/4.0
    accuracy[ds]=N.mean(predclass==Y)
    print '%s (%s): %0.3f'%(taskkey[ds],taskdesc[taskkey[ds]],accuracy[ds])
    f.write('%s (%s): %0.3f\n'%(taskkey[ds],taskdesc[taskkey[ds]],accuracy[ds]))
            
f.close()

f=open('classify_vs_rest_accuracy.pkl','wb')
pickle.dump(accuracy,f)
f.close()

N.save('lr_coefs.npy',coefs)
