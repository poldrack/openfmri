#######
# make behavdata.txt files from a CSV corresponding to that task's data
# copy this file to the dataset root directory (e.g. inprocess/dsXXX/)
# have csv files named task001.csv, ... task00N.csv that contain the data for that task in that folder
# if a task has multiple runs, have data for both runs conflated into that one csv
# (same behavdata.txt is generated for _run001 and _run002, so csv must contain data for both)
# alter the tasks dict to reflect the correct runs and csv names
# written by: Arjun Mukerji <arjun@utexas.edu>
# created on: 2015-04-08
# built and tested for shared2/ds009 - check there for worked example
#######

import os, glob
import csv

# associate csv files (minus the .csv) and task_run folders
tasks = {'task001':['task001_run001',], 'task002':['task002_run001','task002_run002'], 'task003':['task003_run001','task003_run002'], 'task004':['task004_run001',]}

def build_task_dict(fname):
    print "reading {0}...".format(fname)
    reader = csv.reader(open(fname,"r"))
    d = {'colnames':[]} # will hold all the info for this task
    for row in reader:
        if row[0]: # eliminate empty rows
            print row, row[0], row[0].isdigit()
            if not row[0].isdigit(): #row doesn't start with a numeric column (subject #), and so is the first row and contains column names
                d['colnames'] = row[1:]
            else: # row corresponding to one subject's data
                sstr = 'sub' + row[0].zfill(3) # e.g., sub004, sub013
                d[sstr] = row[1:]
    return d

def write_bdata(d,task, tasks):
    print "writing {0}...".format(task)
    datasetdir = '/corral-repl/utexas/poldracklab/openfmri/shared2/ds009/'
    colnames = d.pop('colnames') # after this, d contains only 'subXXX':[vals,] entries
    for k in sorted(d.keys()):
        if not os.path.isdir(os.path.join(datasetdir,k)): continue # if dsXXX/subYYY doesn't exist, skip this line of the file (must have been a bad subject and dropped)
        bdstr = ' '.join(colnames)
        bdstr = bdstr + '\n' + ' '.join(d[k]) + '\n'
        print bdstr
        for taskstr in tasks[task]:
            bdfolname = os.path.join(datasetdir,k,'behav',taskstr)
            if not os.path.isdir(bdfolname):
                os.mkdir(bdfolname)
            bdfname = os.path.join(bdfolname,'behavdata.txt')
            print bdfname
            #print k, bdfname, d[k]
            bdf = open(bdfname,"w")
            bdf.write(bdstr)
            bdf.close()

for t in tasks:
    taskcsv = t + '.csv'
    td = build_task_dict(taskcsv)
    write_bdata(td,t,tasks) 
