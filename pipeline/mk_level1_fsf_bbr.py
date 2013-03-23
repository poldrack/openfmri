#!/usr/bin/env python
""" mk_fsf.py - make first-level FSF model
- this version has support for BBR and also introduces a new set of command line options

USAGE: mk_level1_fsf.py <taskid> <subnum> <tasknum> <runnum> <smoothing - mm> <use_inplane> <basedir> <nonlinear>

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


# create fsf file for arbitrary design
import numpy as N
import sys
import os
import subprocess as sub
from openfmri_utils import *
import argparse


def parse_command_line():
    parser = argparse.ArgumentParser(description='setup_subject')
    #parser.add_argument('integers', metavar='N', type=int, nargs='+',help='an integer for the accumulator')
    # set up boolean flags


    parser.add_argument('--taskid', dest='taskid',
        required=True,help='Task ID')
    parser.add_argument('--subnum', dest='subnum',type=int,
        required=True,help='subject number')
    parser.add_argument('--tasknum', dest='tasknum',type=int,
        required=True,help='Task number')
    parser.add_argument('--runnum', dest='runnum',type=int,
        required=True,help='Run number')
    parser.add_argument('--basedir', dest='basedir',
        required=True,help='Base directory (above taskid directory)')
    parser.add_argument('--smoothing', dest='smoothing',type=int,
        default=0,help='Smoothing (mm FWHM)')
    parser.add_argument('--use_inplane', dest='use_inplane', type=int,
        default=0,help='Use inplane image')
    parser.add_argument('--nonlinear', dest='nonlinear', action='store_true',
        default=False,help='Use nonlinear regristration')
    parser.add_argument('--modelnum', dest='modelnum',type=int,
        default=1,help='Model number')
    
    args = parser.parse_args()
    return args

# create as a function that will be called by mk_all_fsf.py
# just set these for testing
## taskid='ds103'
## subnum=1
## tasknum=1
## runnum=1
## smoothing=6
## use_inplane=0
## nonlinear=1

def main():

    args=parse_command_line()
    print args
    
    taskid=args.taskid
    subnum=args.subnum
    tasknum=args.tasknum
    runnum=args.runnum
    smoothing=args.smoothing
    use_inplane=args.use_inplane
    basedir=args.basedir
    nonlinear=args.nonlinear
    modelnum=args.modelnum
    print taskid,subnum,tasknum,runnum,smoothing,use_inplane,basedir,nonlinear,modelnum
    
    mk_level1_fsf_bbr(taskid,subnum,tasknum,runnum,smoothing,use_inplane,basedir,nonlinear,modelnum)
    
def mk_level1_fsf_bbr(taskid,subnum,tasknum,runnum,smoothing,use_inplane,basedir='/corral/utexas/poldracklab/openfmri/staged/',nonlinear=1,modelnum=1):
    
    subdir='%s/%s/sub%03d'%(basedir,taskid,subnum)

    # read the conditions_key file
    cond_key=load_condkey(os.path.join(basedir,taskid,'models/model%03d/condition_key.txt'%modelnum))

    conditions=cond_key[tasknum].values()
    print 'found conditions:',conditions
    
    # check for orthogonalization file
    orth={}
    orthfile=os.path.join(basedir,taskid,'models/model%03d/orthogonalize.txt'%modelnum)
    if os.path.exists(orthfile):
        f=open(orthfile)
        for l in f.readlines():
            orth_tasknum=int(l.split()[0].replace('task',''))
            if orth_tasknum==tasknum:
                orth[int(l.split()[1])]=int(l.split()[2])
        f.close()
    else:
        print 'no orthogonalization found'
        
    # check for QA dir
    qadir='%s/BOLD/task%03d_run%03d/QA'%(subdir,tasknum,runnum)


    print 'loading contrasts'
    contrasts_all=load_contrasts(os.path.join(basedir,taskid,'models/model%03d/task_contrasts.txt'%modelnum))
    print 'added contrasts:',contrasts_all

    contrasts=[]
    if contrasts_all.has_key('task%03d'%tasknum):
        contrasts=contrasts_all['task%03d'%tasknum]
 
 
        
    scan_key=load_scankey(os.path.join(basedir,taskid,'scan_key.txt'))
    tr=float(scan_key['TR'])
    if scan_key.has_key('nskip'):
        nskip=int(scan_key['nskip'])
    else:
        nskip=0
        
    stubfilename='/corral-repl/utexas/poldracklab/openfmri/code/design_level1_fsl5.stub'
    modelbasedir=subdir+'/model/'
    if not os.path.exists(modelbasedir):
        os.mkdir(modelbasedir)
    modeldir=modelbasedir+'model%03d/'%modelnum
    if not os.path.exists(modeldir):
        os.mkdir(modeldir)
    
    outfilename='%s/model/model%03d/task%03d_run%03d.fsf'%(subdir,modelnum,tasknum,runnum)
    print('%s\n'%outfilename)
    outfile=open(outfilename,'w')
    outfile.write('# Automatically generated by mk_fsf.py\n')

    # first get common lines from stub file
    stubfile=open(stubfilename,'r')
    for l in stubfile:
        outfile.write(l)

    stubfile.close()
    # figure out how many timepoints there are

    p = sub.Popen(['fslinfo','%s/BOLD/task%03d_run%03d/bold_mcf_brain'%(subdir,tasknum,runnum)],stdout=sub.PIPE,stderr=sub.PIPE)
    output, errors = p.communicate()
    ntp=int(output.split('\n')[4].split()[1])

    outfile.write('\n\n### AUTOMATICALLY GENERATED PART###\n\n')
    # now add custom lines
    outfile.write( 'set fmri(regstandard_nonlinear_yn) %d\n'%nonlinear)
    # Delete volumes
    outfile.write('set fmri(ndelete) %d\n'%nskip)


    outfile.write('set fmri(outputdir) "%s/model/model%03d/task%03d_run%03d.feat"\n'%(subdir,modelnum,tasknum,runnum))
    outfile.write('set feat_files(1) "%s/BOLD/task%03d_run%03d/bold_mcf_brain.nii.gz"\n'%(subdir,tasknum,runnum))
    if use_inplane==1:
        outfile.write('set fmri(reginitial_highres_yn) 1\n')
        outfile.write('set initial_highres_files(1) "%s/anatomy/inplane001_brain.nii.gz"\n'%subdir)
    else:
        outfile.write('set fmri(reginitial_highres_yn) 0\n')

    outfile.write('set highres_files(1) "%s/anatomy/highres001_brain"\n'%subdir)
    outfile.write('set fmri(npts) %d\n'%ntp)
    outfile.write('set fmri(tr) %0.2f\n'%tr)
    nevs=len(conditions)
    outfile.write('set fmri(evs_orig) %d\n'%nevs)
    outfile.write('set fmri(evs_real) %d\n'%(2*nevs))
    outfile.write('set fmri(smooth) %d\n'%smoothing)
    outfile.write('set fmri(ncon_orig) %d\n'%(len(conditions)+1+len(contrasts)))
    outfile.write('set fmri(ncon_real) %d\n'%(len(conditions)+1+len(contrasts)))

    # loop through EVs
    convals_real=N.zeros(nevs*2)
    convals_orig=N.zeros(nevs)
    empty_evs=[]

    for ev in range(len(conditions)):
        outfile.write('\n\nset fmri(evtitle%d) "%s"\n'%(ev+1,conditions[ev]))
        condfile='%s/model/model%03d/onsets/task%03d_run%03d/cond%03d.txt'%(subdir,modelnum,tasknum,runnum,ev+1)
        if os.path.exists(condfile):
            outfile.write('set fmri(shape%d) 3\n'%(ev+1))
            outfile.write('set fmri(custom%d) "%s"\n'%(ev+1,condfile))
        else:
             outfile.write('set fmri(shape%d) 10\n'%(ev+1))
             print '%s is missing, using empty EV'%condfile
             empty_evs.append(ev+1)
             
        outfile.write('set fmri(convolve%d) 3\n'%(ev+1))
        outfile.write('set fmri(convolve_phase%d) 0\n'%(ev+1))
        outfile.write('set fmri(tempfilt_yn%d) 1\n'%(ev+1))
        outfile.write('set fmri(deriv_yn%d) 1\n'%(ev+1))

        # first write the orth flag for zero, which seems to be turned on whenever
        # anything is orthogonalized
        
        if orth.has_key(ev+1):
                outfile.write('set fmri(ortho%d.0) 1\n'%int(ev+1))
        else:
                outfile.write('set fmri(ortho%d.0) 0\n'%int(ev+1))
        
        for evn in range(1,nevs+1):
            if orth.has_key(ev+1):
                if orth[ev+1]==evn:
                    outfile.write('set fmri(ortho%d.%d) 1\n'%(ev+1,evn))
                else:
                    outfile.write('set fmri(ortho%d.%d) 0\n'%(ev+1,evn))
            else:
                outfile.write('set fmri(ortho%d.%d) 0\n'%(ev+1,evn))
        # make a T contrast for each EV
        outfile.write('set fmri(conpic_real.%d) 1\n'%(ev+1))
        outfile.write('set fmri(conpic_orig.%d) 1\n'%(ev+1))
        outfile.write('set fmri(conname_real.%d) "%s"\n'%(ev+1,conditions[ev]))
        outfile.write('set fmri(conname_orig.%d) "%s"\n'%(ev+1,conditions[ev]))
        for evt in range(nevs*2):
            outfile.write('set fmri(con_real%d.%d) %d\n'%(ev+1,evt+1,int(evt==(ev*2))))
            if (evt==(ev*2)):
                convals_real[evt]=1
        for evt in range(nevs):
            outfile.write('set fmri(con_orig%d.%d) %d\n'%(ev+1,evt+1,int(evt==ev)))
            if (evt==ev):
                convals_orig[evt]=1
                
    if len(empty_evs)>0:
        empty_ev_file=open('%s/model/model%03d/onsets/task%03d_run%03d/empty_evs.txt'%(subdir,modelnum,tasknum,runnum),'w')
        for eev in empty_evs:
            empty_ev_file.write('%d\n'%eev)
        empty_ev_file.close()

    # make one additional contrast across all conditions
    outfile.write('set fmri(conpic_real.%d) 1\n'%(ev+2))
    outfile.write('set fmri(conname_real.%d) "all"\n'%(ev+2))
    outfile.write('set fmri(conname_orig.%d) "all"\n'%(ev+2))

    for evt in range(nevs*2):
            outfile.write('set fmri(con_real%d.%d) %d\n'%(ev+2,evt+1,convals_real[evt]))
    for evt in range(nevs):
            outfile.write('set fmri(con_orig%d.%d) %d\n'%(ev+2,evt+1,convals_orig[evt]))

    # add custom contrasts
    if len(contrasts)>0:
        print contrasts
        contrastctr=ev+3;
        for c in contrasts.iterkeys():
            
            outfile.write('set fmri(conpic_real.%d) 1\n'%contrastctr)
            outfile.write('set fmri(conname_real.%d) "%s"\n'%(contrastctr,c))
            outfile.write('set fmri(conname_orig.%d) "%s"\n'%(contrastctr,c))
            cveclen=len(contrasts[c])
            con_real_ctr=1
            for evt in range(nevs):
                if contrasts[c][evt]!=0:
                    outfile.write('set fmri(con_real%d.%d) %s\n'%(contrastctr,con_real_ctr,contrasts[c][evt]))
                    outfile.write('set fmri(con_real%d.%d) 0\n'%(contrastctr,con_real_ctr+1))
                    con_real_ctr+=2
                    
                else:
                    outfile.write('set fmri(con_real%d.%d) 0\n'%(contrastctr,evt+1))
                    
            for evt in range(nevs):
                if evt<cveclen:
                    outfile.write('set fmri(con_orig%d.%d) %s\n'%(contrastctr,evt+1,contrasts[c][evt]))
                else:
                    outfile.write('set fmri(con_orig%d.%d) 0\n'%(contrastctr,evt+1))

            contrastctr+=1

    # Add confound EVs text file
    confoundfile="%s/BOLD/task%03d_run%03d/QA/confound.txt"%(subdir,tasknum,runnum)
    if os.path.exists(confoundfile):
        outfile.write('set fmri(confoundevs) 1\n')
        outfile.write('set confoundev_files(1) "%s"\n'%confoundfile)
    else:
        outfile.write('set fmri(confoundevs) 0\n')
        
        

        
    outfile.close()

    return outfilename

if __name__ == '__main__':
    main()
