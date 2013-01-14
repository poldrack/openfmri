import os
import numpy as N
import pickle
import nibabel as nib

basedir='/corral-repl/utexas/poldracklab/openfmri/shared2'
outdir='/corral-repl/utexas/poldracklab/openfmri/shared2/mean_zstat'
zstatdir=os.path.join(basedir,'zstats')
infodir='/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_Dec2012/data_prep'

all_zstats=os.listdir(zstatdir)
z_task=[]
z_ds=[]
z_run=[]
z_zstat=[]

for z in all_zstats:
    z_s=z.strip().replace('.nii.gz','').split('_')
    z_task.append(z_s[2])
    z_ds.append(z_s[0])
    z_run.append(int(z_s[3].replace('run','')))
    z_zstat.append(int(z_s[4].replace('zstat','')))
                 
    
f=open(os.path.join(infodir,'task_keys.pkl'),'rb')
task_keys=pickle.load(f)
f.close()

f=open(os.path.join(infodir,'task_contrasts.pkl'),'rb')
contrasts=pickle.load(f)
f.close()

f=open(os.path.join(infodir,'task_conditions.pkl'),'rb')
condition_keys=pickle.load(f)
f.close()

data_shape=(91,109,91)
runnum=1

for ds in task_keys.iterkeys():
    for task in task_keys[ds].iterkeys():
        for contrast in contrasts[ds][task]['contrasts']:
            z_task_idx= N.array([1 if a == task else 0 for a in z_task])
            z_run_idx= N.array([1 if a==runnum else 0 for a in z_run])
            
            z_ds_idx=N.array([1 if a == ds else 0 for a in z_ds])
            z_zstat_idx = N.array([1 if a == contrast else 0 for a in z_zstat])
            zslist=[all_zstats[i] for i in N.where(z_task_idx*z_ds_idx*z_zstat_idx*z_run_idx)[0]]
            imgdata=N.zeros(data_shape)
            
            for zfile in zslist:
                img=nib.load(os.path.join(zstatdir,zfile))
                imgdata+=img.get_data()
            imgdata=imgdata/float(len(zslist))
            newimg=nib.Nifti1Image(imgdata,img.get_affine())
            newimg.to_filename(os.path.join(outdir,'mean_%s_%s_zstat%d_run%d.nii.gz'%(ds,task,contrast,runnum)))

                             
