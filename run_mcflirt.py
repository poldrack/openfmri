import os

basedir='/corral/utexas/poldracklab/openfmri/shared/'
outfile=open('run_mcflirt.sh','w')

for root,dirs,files in os.walk(basedir):
    for f in files:
        if f.rfind('bold.nii.gz')>-1:
            outfile.write('mcflirt -in %s/%s -sinc_final -plots\n'%(root,f))

outfile.close()

            
print 'now launch using:'
print 'launch -s run_mcflirt.sh -n mcflirt -r 00:30:00'
