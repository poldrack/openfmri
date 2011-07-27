""" run_copy_stripped.py - copy skull-stripped images from freesurfer dirs
"""

## Copyright 2011, Russell Poldrack. All rights reserved.

## Redistribution and use in source and binary forms, with or without modification, are
## permitted provided that the following conditions are met:

##    1. Redistributions of source code must retain the above copyright notice, this list of
##       conditions and the following disclaimer.

##    2. Redistributions in binary form must reproduce the above copyright notice, this list
##       of conditions and the following disclaimer in the documentation and/or other materials
##       provided with the distribution.

## THIS SOFTWARE IS PROVIDED BY RUSSELL POLDRACK ``AS IS'' AND ANY EXPRESS OR IMPLIED
## WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
## FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL RUSSELL POLDRACK OR
## CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
## CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
## SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
## ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
## NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
## ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.



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



