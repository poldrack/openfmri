#!/usr/bin/env python
""" launch_qsub.py - a python function to launch SGE jobs on TACC Lonestar

this is a function version of the launch command line script 

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



import argparse
import sys,os
from tempfile import *
import subprocess

MAXCORES=4104


def usage():
    """ print the docstring and exit"""
    sys.stdout.write(__doc__)
    sys.exit(2)
    
class C(object):
    pass

def SetupParser():
    c=C()
    parser = argparse.ArgumentParser(description='process SGE job.')

    parser.add_argument('-s','--script',help='name of parallel script to run',dest='script_name')
    parser.add_argument('-d','--cwd',help='name of working directory',dest='directory')
    parser.add_argument('-r','--runtime',help='maximum runtime for job',default='01:00:00',dest='runtime')
    parser.add_argument('-o','--outfile',help='outputfile',dest='outfile')
    parser.add_argument('-p','--numproc',help='number of cores',dest='ncores')
    parser.add_argument('-e','--parenv',help='name of parallel environment (use smaller way for more memory per job)',default='12way',dest='parenv')
    parser.add_argument('-n','--jobname',help='job name',default='launch',dest='jobname')
    parser.add_argument('-j','--projname',help='name of project',dest='projname')
    parser.add_argument('-q','--queue',help='name of queue',default='normal',dest='queue')
    parser.add_argument('-m','--email',help='email address for notification',dest='email')
    parser.add_argument('-f','--qsubfile',help='name of qsub file',dest='qsubfile')
    parser.add_argument('-k','--keepqsubfile',help='keep qsub file',dest='keepqsubfile', action="store_true",default=False)
    parser.add_argument('-u','--ignoreuser',help='ignore ~/.launch_user',dest='ignoreuser', action="store_true",default=False)
    parser.add_argument('-t','--test',help='do not actually launch job',dest='test', action="store_true",default=False)
    parser.add_argument('-c','--compiler',help='compiler (default=intel, use gcc for numpy)',dest='compiler', default='intel')
    parser.add_argument('-i','--hold_jid',help='job ID to wait for before starting this job',dest='hold', default=[])

    return c,parser


def launch_qsub(serialcmd='',script_name='',runtime='01:00:00',ncores=0,parenv='12way',jobname='launch',projname='',queue='normal',email=False,qsubfile='',keepqsubfile=False,ignoreuser=False,test=False,compiler='intel',parser=[],c=[],verbose=0,hold=[],outfile=[],cwd=[]):
    """ function to launch SGE job

    launch(serialcmd='',script_name='',runtime='01:00:00',ncores=0,parenv='12way',jobname='launch',projname='',queue='normal',email,qsubfile='',keepqsubfile=False,ignoreuser=False,test=False,compiler='intel',parser=[],verbose=0,hold=[])
    """

    if parser==[]:
        c,parser=SetupParser()

    # set email prior to reading .launch file
    # so that setting overrides default
    if c.__dict__.has_key('email'):
        email=c.email

    # first check for .launch file in home directory
    if os.path.exists(os.path.expanduser('~')+'/.launch_user') and not ignoreuser:
        f=open(os.path.expanduser('~')+'/.launch_user')
        for cmd in f.readlines():
            if verbose:
                print cmd
            parser.parse_args([cmd.strip()],namespace=c)
        f.close()
        
    if c.projname:
        projname=c.projname
    if not projname:
        print 'You must specify a project name'
        sys.exit(0)
        #return []

    if len(serialcmd)>0:
        parametric=0
        print 'Running serial command: '+serialcmd
        ncores=12
        parenv='1way'
        queue='serial'
    elif script_name:
        parametric=1
        if verbose:
            print 'Submitting parametric job file: '+script_name
        try:
            f=open(script_name,'r')
        except:
            print '%s does not exist -e!'%script_name
            sys.exit(0)
        script_cmds=f.readlines()
        f.close()
        ncmds=len(script_cmds)
        if verbose:
            print 'found %d commands'%ncmds
        # need to check for empty lines
        for s in script_cmds:
            if s.strip()=='':
                print 'command file contains empty lines - please remove them first'
                sys.exit()
        if not ncores:
            ncores=(ncmds/12+1)*12
            if verbose:
                print 'Number of processors not specified - estimating as %d'%ncores

        if int(ncores)>MAXCORES:
            ncores=MAXCORES
    else:
        print 'ERROR: you must either specify a script name (using -s) or a command to run\n\n'
        parser.print_help()
        sys.exit()

    if not qsubfile:
        qsubfile_fd,qsubfile=mkstemp(prefix=jobname+"_",dir='.',suffix='.qsub',text=True)
        os.close(qsubfile_fd)

    if verbose:
        print 'Outputting qsub commands to %s'%qsubfile
    qsubfile_fd=open(qsubfile,'w')
    if parametric:
        qsubfile_fd.write('#!/bin/csh\n#\n')
    else:
        qsubfile_fd.write('#!/bin/bash\n#\n')
    qsubfile_fd.write('# SGE control file automatically created by launch\n')
    if parametric==1:
        qsubfile_fd.write('# Using parametric launcher with control file: %s\n'%script_name)
    else:
        qsubfile_fd.write('# Launching single command: %s\n#\n#\n'%serialcmd)

    qsubfile_fd.write('#$ -V                    #Inherit the submission environment\n')
    qsubfile_fd.write('#$ -cwd                  # Start job in submission directory\n')
    qsubfile_fd.write('#$ -j y                  # Combine stderr and stdout\n')
    qsubfile_fd.write('#$ -N %s       # Job Name\n'%jobname)
    qsubfile_fd.write('#$ -A %s\n'%projname)
    qsubfile_fd.write('#$ -o $JOB_NAME.o$JOB_ID # Name of the output file (eg. myMPI.oJobID)\n')
    qsubfile_fd.write('#$ -pe %s %d\n'%(parenv,int(ncores)))
    qsubfile_fd.write('#$ -q %s\n'%queue)
    qsubfile_fd.write('#$ -l h_rt=%s\n'%runtime)
 
    if email:
        qsubfile_fd.write('#$ -M %s\n'%email)
        qsubfile_fd.write('#$ -m be\n')
    if c.hold:
        hold=int(c.hold)
    if hold:
        if verbose:
            print 'will hold until completion of job %d'%hold
        qsubfile_fd.write('#$ -hold_jid %d\n'%hold)
        

    qsubfile_fd.write('#----------------\n# Job Submission\n#----------------\n')

    if not parametric:
        qsubfile_fd.write('\n\nset -x                   # Echo commands, use "set echo" with csh\n')
        qsubfile_fd.write(serialcmd+'\n')

    else:
        qsubfile_fd.write('module load launcher\n')
        if compiler=='intel':
            qsubfile_fd.write('module swap gcc intel\n')
        if compiler=='gcc':
            qsubfile_fd.write('module swap intel gcc\n')

        qsubfile_fd.write('setenv EXECUTABLE     $TACC_LAUNCHER_DIR/init_launcher\n')
        qsubfile_fd.write('setenv CONTROL_FILE %s\n'%script_name)
        qsubfile_fd.write('setenv WORKDIR .\n')

        qsubfile_fd.write('cd $WORKDIR/\n')
        qsubfile_fd.write('echo " WORKING DIR:   $WORKDIR/"\n')
        qsubfile_fd.write('$TACC_LAUNCHER_DIR/paramrun $EXECUTABLE $CONTROL_FILE\n')

        qsubfile_fd.write('echo " "\necho " Parameteric Job Complete"\necho " "\n')

    qsubfile_fd.close()


    output=[]
    jobid=0
    if c.directory:
        cwd=c.directory
    if not test:
        if cwd:
            print 'outputting to %s'%cwd
            process = subprocess.Popen('qsub %s'%qsubfile, shell=True, stdout=subprocess.PIPE,cwd=cwd)
        else:
            process = subprocess.Popen('qsub %s'%qsubfile, shell=True, stdout=subprocess.PIPE)
        for line in process.stdout:
            if verbose:
                print line.strip()
            output.append(line.strip())
            if line.find('Your job')>-1 and line.find('has been submitted')>-1:
                jobid=int(line.split(' ')[2])
                print 'job id: ',jobid
        process.wait()

    if not keepqsubfile:
        if verbose:
            print 'Deleting qsubfile: %s'%qsubfile
        os.remove(qsubfile)

    return jobid,output


