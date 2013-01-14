"""
take filtered func data from stats dirs,
apply spatial smoothing, and run group
model using randomize
"""

import os
import glob
import numpy

basedir='/corral-repl/utexas/poldracklab/openfmri/shared2'
datasets=['ds002', 'ds003', 'ds005', 'ds006A', 'ds007', 'ds008', 'ds011', 'ds017A', 'ds017B', 'ds051', 'ds052', 'ds101', 'ds102', 'ds105', 'ds107']
modelnum=1
fwhm=6.0
maskimg='/corral-repl/utexas/poldracklab/software_lonestar/fsl-5.0.1/data/standard/MNI152_T1_2mm_brain_mask.nii.gz'
sigma=numpy.sqrt(numpy.log(2.0)*fwhm)


f=open('mk_smooothed_files.sh','w')
frand=open('run_smoothed_randomise.sh','w')

for dataset in datasets:
    origdir=os.path.join(basedir,dataset,'group/model%03d'%modelnum)
    smoothdir=os.path.join(basedir,dataset,'group_smoothed')

    if not os.path.exists(smoothdir):
        os.mkdir(smoothdir)

    smoothdir=os.path.join(smoothdir,'model%03d'%modelnum)
    if not os.path.exists(smoothdir):
        os.mkdir(smoothdir)

    taskdirs=glob.glob(os.path.join(origdir,'task*'))

    tasks=[t.split('/')[-1] for t in taskdirs]


    for taskdir in taskdirs:
        task=taskdir.split('/')[-1]
        newtaskdir=os.path.join(smoothdir,task)
        if not os.path.exists(newtaskdir):
            os.mkdir(newtaskdir)
        gfeat_dirs=glob.glob(os.path.join(taskdir,'cope*.gfeat'))
        for gfeat in gfeat_dirs:
            filtfunc=os.path.join(gfeat,'cope1.feat/filtered_func_data.nii.gz')
            gfeatnum=gfeat.split('/')[-1].replace('.gfeat','')

            newfile=os.path.join(smoothdir,task,'%s.nii.gz'%gfeatnum)
            cmd='fslmaths %s -s %f %s'%(filtfunc,sigma,newfile)
            print cmd
            f.write('%s\n'%cmd)
            cmd='randomise -i %s -o %s/%s -1 -m %s -n 5000 -T -R -v 10'%(newfile,
                      newtaskdir,gfeatnum,maskimg)
            print cmd
            frand.write(cmd+'\n')

frand.close()

f.close()
    
