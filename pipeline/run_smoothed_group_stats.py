#!/usr/bin/env python
"""
take filtered func data from stats dirs,
apply spatial smoothing, and run group
model using randomize
"""

import os,sys
import glob
import numpy
import argparse

def parse_command_line():
    parser = argparse.ArgumentParser(description='run_smoothed_group_stats')
    parser.add_argument('-b','--basedir', dest='basedir',
        help='base directory for data file', default='/corral-repl/utexas/poldracklab/data/openfmri/shared2')
    parser.add_argument('input',nargs='+', #dest='studyname',
        help='name of study/studies to be analyzed')
    parser.add_argument('--modelnum', dest='modelnum',type=int,
        default=1,help='Model number')
    parser.add_argument('--smoothing', dest='smoothing',type=float,
        default=6.0,help='Smoothing (mm FWHM)')
    parser.add_argument('-m','--maskimg', dest='maskimg',
        help='mask image for randomise', default='/corral-repl/utexas/poldracklab/software_lonestar/fsl-5.0.1/data/standard/MNI152_T1_2mm_brain_mask.nii.gz')

    args = parser.parse_args()
    return args

args=parse_command_line()

print args
datasets=[]
for i in args.input:
    if not os.path.exists(os.path.join(args.basedir,i)):
        print os.path.join(args.basedir,i),'does not exist, skipping'
    else:
        datasets.append(i)

basedir=args.basedir

#datasets=['ds001','ds002', 'ds003', 'ds005', 'ds006A', 'ds007', 'ds008', 'ds011', 'ds017A', 'ds017B', 'ds051', 'ds052', 'ds101', 'ds102', 'ds105', 'ds107']

modelnum=args.modelnum
fwhm=args.smoothing
maskimg=args.maskimg
#maskimg='/corral-repl/utexas/poldracklab/software_lonestar/fsl-5.0.1/data/standard/MNI152_T1_2mm_brain_mask.nii.gz'

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
    
