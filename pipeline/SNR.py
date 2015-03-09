"""
Script used to view SNR values in qadata.csv ; script also finds minimum, maximum, and mean SNR values

run script in directory that dataset is located in
USAGE python ../code/SNR.py <name of dataset> <basedir>

for questions contact Natalie Picchetti at nataliepicchetti@gmail.com
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
                SNR = line1[1]
                print '%s/%s/BOLD/%s '%(ds,s,td) + str(SNR)
                if float(line1[1]) < 15:
                    print '%s/%s/BOLD/%s '%(ds,s,td) + str(SNR) + ' SNR less than 15'
x=[]

dsdir=os.path.join(basedir,ds) #/corral-repl/utexas/poldracklab/openfmri/staged/ds0XX
for s in os.listdir(dsdir): #everything listed in the dataset directory
    if s[0:3]=='sub': #exclusively use sub0XX
        for td in os.listdir('%s/%s/BOLD/'%(dsdir,s)): #go into the task00X_run00X directories
            if os.path.exists('%s/%s/BOLD/%s/QA/qadata.csv'%(dsdir,s,td)): #if qadata.csv data exists continue
                qadata = open('%s/%s/BOLD/%s/QA/qadata.csv'%(dsdir,s,td),'r')
                csvreader = csv.reader(qadata)
                line1 = csvreader.next()
                SNR = line1[1]
                x.append(float(line1[1]))

print 'list of SNR values: ' + str(x)
minimum = min(x)
maximum = max(x)
mean = numpy.mean(x)
print str(minimum) + ' is the minimum SNR value'
print str(maximum) + ' is the maximum SNR value'
print str(mean) + ' is the mean SNR value'
                
                



"""
if want ['SNR', 'number'] format

dsdir=os.path.join(basedir,ds) #/corral-repl/utexas/poldracklab/openfmri/staged/ds0XX
for s in os.listdir(dsdir): #everything listed in the dataset directory
    if s[0:3]=='sub': #exclusively use sub0XX
        for td in os.listdir('%s/%s/BOLD/'%(dsdir,s)): #go into the task00X_run00X directories
            if os.path.exists('%s/%s/BOLD/%s/QA/qadata.csv'%(dsdir,s,td)): #if qadata.csv data exists continue
                qadata = open('%s/%s/BOLD/%s/QA/qadata.csv'%(dsdir,s,td),'r')
                csvreader = csv.reader(qadata)
                line1 = csvreader.next()
                SNR = line1
                print '%s/%s/BOLD/%s '%(ds,s,td) + str(SNR)
"""
