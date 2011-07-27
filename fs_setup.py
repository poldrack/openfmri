import os

basedir='/corral/utexas/poldracklab/openfmri/shared/'
subdir='/scratch/01329/poldrack/openfmri/shared/subdir'
outfile=open('fs_setup.sh','w')
#subdir=basedir+'subdir'

for root,dirs,files in os.walk(basedir):
  if root.find('ds011')>-1:
    for f in files:
        if f.rfind('highres.nii.gz')>-1:
            f_split=root.split('/')
            outfile.write('recon-all -i %s/%s -subjid %s_%s -sd %s\n'%(root,f,f_split[6],f_split[7],subdir))

outfile.close()

            
print 'now launch using: sh fs_setup.sh'


