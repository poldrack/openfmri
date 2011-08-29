import os,sys
from run_shell_cmd import *

featdir='/corral/utexas/poldracklab/openfmri/shared/ds002/sub001/model/task001_run001.feat/'

ANTSPATH=os.environ['ANTSPATH']
FSLDIR=os.environ['FSLDIR']
test=False
template_brain='%s/data/standard/MNI152_T1_2mm_brain.nii.gz'%FSLDIR

antsdir=featdir+'reg_ANTS'
if not os.path.exists(antsdir):
    os.mkdir(antsdir)

anatdir='/'.join(featdir.split('/')[:-3])+'/anatomy'

cmd='c3d_affine_tool -ref %s/reg/highres.nii.gz -src %s/example_func.nii.gz %s/reg/example_func2highres.mat -fsl2ras -oitk %s/func2highresAffine.txt'%(featdir,featdir,featdir,antsdir)
#print cmd

cmd='WarpImageMultiTransform 3 %s/example_func.nii.gz %s/example_func2std.nii.gz -R %s %s/highres001_ANTSstdWarp.nii.gz %s/highres001_ANTSstdAffine.txt %s/func2highresAffine.txt'%(featdir,antsdir,template_brain,anatdir,anatdir,antsdir)
print cmd
