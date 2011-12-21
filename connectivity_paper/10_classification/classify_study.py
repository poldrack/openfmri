#!/usr/bin/env python
""" classify each dataset by study using partial correlation matrices
"""

from sklearn import svm
import numpy as N
from sklearn.cross_validation import StratifiedKFold

import pickle
datatype='resid'

# load raw data and prepare for classification
prep_data=0
if prep_data==1:
    f=open('all_z_%s_regpcorr.pkl'%datatype,'rb')
    all_z=pickle.load(f)
    f.close()

    taskid=0
    taskkey={}

    data_id=N.zeros(0)
    dataset=N.zeros((0,43660))

    for ds in all_z.keys():
        for task in all_z[ds].keys():
            taskid+=1
            taskkey[taskid]='%s_%d'%(ds,task)
            dataset=N.vstack((dataset,all_z[ds][task]))
            for sub in range(all_z[ds][task].shape[0]):
                data_id=N.hstack((data_id,taskid))

    N.save('%s_data_for_classification.npy'%datatype,dataset)
    N.save('%s_data_labels.npy'%datatype,data_id)
    f=open('%s_taskkey.pkl'%datatype,'wb')
    pickle.dump(taskkey,f)
    f.close()
else:
    dataset=N.load('%s_data_for_classification.npy'%datatype)
    data_id=N.load('%s_data_labels.npy'%datatype)
    f=open('%s_taskkey.pkl'%datatype,'rb')
    taskkey=pickle.load(f)
    f.close()
    
# do classification

            
        
# run classifier
# used balanced cross-validation
run_classifier=0
if run_classifier==1:
    skf=StratifiedKFold(data_id,8)

    predclass=N.zeros(data_id.shape)
    foldctr=1
    for train,test in skf:
        print 'fold %d'%foldctr
        foldctr+=1
        X_train,X_test,Y_train,Y_test=dataset[train,:],dataset[test,:],data_id[train],data_id[test]
        clf=svm.LinearSVC()
        clf.fit(X_train,Y_train)
        predclass[test]=clf.predict(X_test)
    accuracy=N.mean(predclass==data_id)

    N.save('%s_predclass.npy'%datatype,predclass)
