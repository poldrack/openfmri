import os
from openfmri_utils import *

from mk_level3_fsf import *

basedir='/corral/utexas/poldracklab/openfmri/shared/'

featdirs=[]
subdirs={}

taskid_list=['ds002','ds003','ds005','ds006','ds007','ds008','ds011','ds101','ds102']
nsubs={'ds002':17, 'ds003':13,'ds005':16,'ds006':14,'ds007':21,'ds008':15,'ds011':14,'ds101':21,'ds102':26}

 
for taskid in taskid_list:
  cond_key=load_condkey(basedir+taskid+'/condition_key.txt')
  ntasks=len(cond_key)

  
  for t in range(ntasks):
    mk_level3_fsf(taskid,t+1,nsubs[taskid],basedir)

