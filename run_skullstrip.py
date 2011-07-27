import os

basedir='/corral/utexas/poldracklab/openfmri/shared/'
outfile=open('run_skullstrip.sh','w')
#subdir=basedir+'subdir'
subdir='/scratch/01329/poldrack/openfmri/shared/subdir'

for root,dirs,files in os.walk(basedir):
    for f in files:
        if f.rfind('highres.nii.gz')>-1 and root.find('ds011')>-1:
            f_split=root.split('/')
            outfile.write('recon-all -autorecon1 -subjid %s_%s -sd %s\n'%(f_split[6],f_split[7],subdir))

outfile.close()

            
print 'now launch using:'
print 'launch -s run_skullstrip.sh -n skullstrip -r 02:00:00'
print 'NB: requires intel compiler (use "module swap gcc intel")'


