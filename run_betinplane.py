import os

basedir='/corral/utexas/poldracklab/openfmri/shared/'
outfile=open('run_betinplane.sh','w')

for root,dirs,files in os.walk(basedir):
    for f in files:
        if f.rfind('inplane.nii.gz')>-1 and root.find('ds011')>-1:
            outfile.write('bet %s/%s %s/%s\n'%(root,f,root,f.replace('inplane','inplane_brain')))

outfile.close()

            
print 'now launch using:'
print 'launch -s run_betinplane.sh -n betinplane -r 00:30:00'
