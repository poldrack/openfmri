"""
Script used to determine which task/runs had more than 25% of timepoints scrubbed

run script in directory that dataset is located in
USAGE python ../code/scrubvols.py <name of dataset> <basedir>

for questions contact Natalie Picchetti at nataliepicchetti@gmail.com
"""
import sys
import os

if len(sys.argv)>1:
    ds=sys.argv[1]

if len(sys.argv)>2:
    basedir=sys.argv[2]


dsdir=os.path.join(basedir,ds) #/corral-repl/utexas/poldracklab/openfmri/staged/ds0XX
for s in os.listdir(dsdir): #everything listed in the dataset directory
    if s[0:3]=='sub': #exclusively use sub0XX
        for td in os.listdir('%s/%s/BOLD/'%(dsdir,s)): #go into the task00X_run00X directories
            if os.path.exists('%s/%s/BOLD/%s/bold_mcf.par'%(dsdir,s,td)): #look for bold_mcf.par and if it exists continue
                Count_all_tp = len(open('%s/%s/BOLD/%s/bold_mcf.par'%(dsdir,s,td)).readlines())
                #print '%s/%s/BOLD/%s/bold_mcf.par'%(dsdir,s,td) +' has '+ str(Count_all_tp) + ' timepoints'
            if os.path.exists('%s/%s/BOLD/%s/QA/scrubvols.txt'%(dsdir,s,td)):
                Count_scrubvols = len(open('%s/%s/BOLD/%s/QA/scrubvols.txt'%(dsdir,s,td)).readlines())
                #print '%s/%s/BOLD/%s/QA/scrubvols.txt'%(dsdir,s,td) + ' has '+ str(Count_scrubvols) + ' scrubvols'
                if float(Count_scrubvols)/float(Count_all_tp) > .2:
                    print '%s/BOLD/%s'%(s,td) + ': ' + str((float(Count_scrubvols)/float(Count_all_tp))*100) + '% of timepoints scrubbed'


                    # print '%s/%s/BOLD/%s'%(dsdir,s,td) + ' has ' + str((float(Count_scrubvols)/float(Count_all_tp))*100) + '% of timepoints scrubbed'
                                     



















"""

dsdir=os.path.join(basedir,ds) #/corral-repl/utexas/poldracklab/openfmri/staged/ds0XX
for s in os.listdir(dsdir): #everything listed in the dataset directory
    if s[0:3]=='sub': #exclusively use sub0XX
        for td in os.listdir('%s/%s/BOLD/'%(dsdir,s)):
            for m in os.listdir('%s/%s/BOLD/%s/'%(dsdir,s,td)):
                if m=='bold_mcf.par':
                    Count_all_tp = len(open('%s/%s/BOLD/%s/%s'%(dsdir,s,td,m)).readlines())
                    print '%s/%s/BOLD/%s/%s'%(dsdir,s,td,m) +' has '+ str(Count_all_tp) + ' timepoints'

def percentage(count_scrubvols, count_total):
    return 100 * float(count_scrubvols)/float(count_total)
"""
