"""
make onset files for wash U data
"""

import os
import numpy

def parse_fidl(infile):
    data=numpy.loadtxt(infile,skiprows=1)
    return data

subnum=1
# usually 137 frames * 2.5 secs = 342.5 long


origonsetdir='/Users/poldrack/code/openfmri/washu_metadata/Poldrack_Study1_EventFiles'
newonsetdir='/Users/poldrack/code/openfmri/washu_metadata/Poldrack_Study1_FSLonsets'

if not os.path.exists(newonsetdir):
    os.mkdir(newonsetdir)
    
infile=os.path.join(origonsetdir,'subj%03d_nback.fidl'%subnum)

fidldata=parse_fidl(infile)

cuetimes=fidldata[numpy.where(fidldata[:,1]==0)[0],0]

if not cuetimes[0]==25:
    raise BaseException('0-back mismatch')

if not cuetimes[2]==367.5:
    raise BaseException('1-back mismatch')

if not cuetimes[4]==710:
    raise BaseException('2-back mismatch')

runstart=[0,342,685]

runnum=numpy.zeros(fidldata.shape[0])
for i in range(fidldata.shape[0]):
    if fidldata[i,0]<runstart[1]:
        runnum[i]=0
    elif fidldata[i,0]<runstart[2]:
        runnum[i]=1
    else:
        runnum[i]=2

subdir=os.path.join(newonsetdir,'sub%3d'%subnum)
if not os.path.exists(subdir):
    os.mkdir(subdir)

for i in range(3):
    rundir=os.path.join(subdir,'task%03d_run001'%int(i+1))
    if not os.path.exists(rundir):
        os.mkdir(rundir)
    
    outfile=os.path.join(rundir,'cond%0
