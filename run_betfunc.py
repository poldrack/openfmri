import os

basedir='/corral/utexas/poldracklab/openfmri/shared/'
outfile=open('run_betfunc.sh','w')

for root,dirs,files in os.walk(basedir):
    for f in files:
        if f.rfind('bold_mcf.nii.gz')>-1:
            outfile.write('bet %s/%s %s/%s -F\n'%(root,f,root,f.replace('mcf','mcf_brain')))

outfile.close()

            
print 'now launch using:'
print 'launch -s run_betfunc.sh -n betfunc -r 00:30:00'
