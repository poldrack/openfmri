import os

basedir='/corral/utexas/poldracklab/openfmri/shared/'
outfile=open('run_copy_stripped.sh','w')
#subdir=basedir+'subdir'
subdir='/scratch/01329/poldrack/openfmri/shared/subdir'


for root,dirs,files in os.walk(basedir):
    for f in files:
        if f.rfind('highres.nii.gz')>-1 and root.find('ds011')>-1:
            f_split=root.split('/')
            outfile.write('mri_convert --out_orientation LAS %s/%s_%s/mri/brainmask.mgz --reslice_like %s/highres.nii.gz  %s/highres_brain.nii\n'%(subdir,f_split[6],f_split[7],root,root))
            outfile.write('gzip %s/highres_brain.nii\n'%root)
            outfile.write('fslmaths %s/highres_brain.nii.gz -thr 1 -bin %s/highres_brain_mask.nii.gz\n'%(root,root))

outfile.close()

            
print 'now launch using:'
print 'launch -s run_copy_stripped.sh -n copy_skullstrip -r 02:00:00'



