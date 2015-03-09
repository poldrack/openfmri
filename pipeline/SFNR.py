"""
Script used to view SFNR values in qadata.csv ; script also finds minimum, maximum, and mean SFNR values

run script in directory that dataset is located in
USAGE python ../code/SFNR.py <name of dataset> <basedir>

for questions, contact Natalie Picchetti at nataliepicchetti@gmail.com
"""


import sys
import csv
import os
import numpy

if len(sys.argv)>1:
    ds=sys.argv[1]

if len(sys.argv)>2:
    basedir=sys.argv[2]

dsdir=os.path.join(basedir,ds) #/corral-repl/utexas/poldracklab/openfmri/staged/ds0XX
for s in os.listdir(dsdir): #everything listed in the dataset directory
    if s[0:3]=='sub': #exclusively use sub0XX
        for td in os.listdir('%s/%s/BOLD/'%(dsdir,s)): #go into the task00X_run00X directories
            if os.path.exists('%s/%s/BOLD/%s/QA/qadata.csv'%(dsdir,s,td)): #if qadata.csv data exists continue
                qadata = open('%s/%s/BOLD/%s/QA/qadata.csv'%(dsdir,s,td),'r')
                csvreader = csv.reader(qadata)
                line1 = csvreader.next()
                line2 = csvreader.next()
                SNR = line1
                SFNR = line2[1]
                print '%s/%s/BOLD/%s '%(ds,s,td) + str(SFNR)
                if float(line2[1]) < 15:
                    print '%s/%s/BOLD/%s '%(ds,s,td) + str(SFNR) + ' SFNR less than 15'
                  
x=[]

dsdir=os.path.join(basedir,ds) #/corral-repl/utexas/poldracklab/openfmri/staged/ds0XX
for s in os.listdir(dsdir): #everything listed in the dataset directory
    if s[0:3]=='sub': #exclusively use sub0XX
        for td in os.listdir('%s/%s/BOLD/'%(dsdir,s)): #go into the task00X_run00X directories
            if os.path.exists('%s/%s/BOLD/%s/QA/qadata.csv'%(dsdir,s,td)): #if qadata.csv data exists continue
                qadata = open('%s/%s/BOLD/%s/QA/qadata.csv'%(dsdir,s,td),'r')
                csvreader = csv.reader(qadata)
                line1 = csvreader.next()
                line2 = csvreader.next()
                SNR = line1[1]
                SFNR = line2[1]
                x.append(float(line2[1]))

print 'list of SFNR values: ' + str(x)
minimum = min(x)
maximum = max(x)
mean = numpy.mean(x)
print str(minimum) + ' is the minimum SFNR value'
print str(maximum) + ' is the maximum SFNR value'
print str(mean) + ' is the mean SFNR value'


"""
if want ['SFNR', 'number'] format

dsdir=os.path.join(basedir,ds) #/corral-repl/utexas/poldracklab/openfmri/staged/ds0XX
for s in os.listdir(dsdir): #everything listed in the dataset directory
    if s[0:3]=='sub': #exclusively use sub0XX
        for td in os.listdir('%s/%s/BOLD/'%(dsdir,s)): #go into the task00X_run00X directories
            if os.path.exists('%s/%s/BOLD/%s/QA/qadata.csv'%(dsdir,s,td)): #if qadata.csv data exists continue
                qadata = open('%s/%s/BOLD/%s/QA/qadata.csv'%(dsdir,s,td),'r')
                csvreader = csv.reader(qadata)
                line1 = csvreader.next()
                line2 = csvreader.next()
                SNR = line1
                SFNR = line2
                print '%s/%s/BOLD/%s '%(ds,s,td) + str(SFNR)

"""
