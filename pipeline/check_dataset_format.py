# This script will check a directory to see if it complies with the openfmri
# dataset format, and output a list of places where it does not do so.
#
# Created: 2014-12-11 by Arjun Mukerji <arjun@utexas.edu>

import boto
import os
import sys

#### definition of a dataset ####
# files that should exist for each dataset
top_level_files = ['demographics.txt','task_key.txt','scan_key.txt','task_order.txt','model_key.txt','README']
# subfolders that should exist in each subject
subject_folders = ['anatomy','behav','BOLD','model'] # the base folders
# these may not exist, depending on the study
opt_folders = ['DTI','dwi','diffusion','MEG','fieldmap'] # check if these folders exist; if so, check their contents

subjects = []
tasks = set([]) # names of the task folders (incl. runs) - e.g. taskXXX_runYYY
#### end dataset definiiton ####



# connect to s3, reads keys from environment variables
s3 = boto.connect_s3()

# open openfmri bucket, which contains a tarballs/ folder, and also
# individual folders for each dataset (eg ds115/)
ofbucket = s3.get_bucket('openfmri')

# what dataset are we checking?
try:
    dataset=sys.argv[1]
except:
    print 'USAGE: check_dataset_format.py <ds code>'
    sys.exit()

# all files related to this dataset will have this prefix
dsprefix = '%s/'%dataset
print 'Required subject folders: %s' % ', '.join(subject_folders)
print 'Optional folders which may exist for some studies: %s' % ', '.join(opt_folders)
print 'Required metadata: %s' % ', '.join(top_level_files)
print 'checking %s ...'%dsprefix

# list of keys that correspond to top-level files for this dataset
this_tlf = ['%s%s'%(dsprefix,z) for z in top_level_files]
# dict mapping generic names (eg task_key.txt) to specific names
spec_names = {z:'%s%s'%(dsprefix,z) for z in top_level_files}
# dict which keeps track of whether that key was found
this_tlfcount = {key: 0 for key in this_tlf}

# top-level files - let's check that all the metadata exists
for key in ofbucket.list(prefix=dsprefix, delimiter='/'):
	kname = key.name.encode('utf-8')
	if kname in this_tlf:
		this_tlfcount[kname] = 1
	shortname = kname.split('/')[1]
	if shortname[0:3] == 'sub': # let's make a list of all subjects
		subjects.append(shortname)

tlfstmt = '== Metadata ==\n'
statements = (' is missing',' exists')
for key in this_tlfcount:
	tlfstmt = tlfstmt + '%s%s\n'%(key,statements[this_tlfcount[key]])
print tlfstmt
#print spec_names

n_subs = len(subjects)
all_subs_folders = {}
all_subs_tasks = {}
print 'Checking %d subjects ...' % n_subs
# look in each subject's folder to see that all subfolders exist
# generally, here we build a model of what each subject should have in this dataset
# and also we check what each subject has and make a dict of it
for sub_ind,s in enumerate(subjects): # sub_ind starts at 0!
	subprefix = '%s%s/' % (dsprefix,s)
	shortnames = [] # a list of all the subfolders this subj contains
	for key in ofbucket.list(prefix=subprefix, delimiter='/'):
		kname = key.name.encode('utf-8')
		shortname = kname.split('/')[2]
		if not shortname in subject_folders: # a folder not included in the base list is encountered for the first time
			if shortname in opt_folders:
				print 'It looks like this study has %s data... will check that all subjects have this.' % shortname
			else:
				print 'Unknown data type: %s.' % shortname
			if sub_ind>0:
				print '*** ERROR: %d previous subjects did not have this folder!' % sub_ind
			subject_folders.append(shortname)
			#print subject_folders
		if shortname=='BOLD': #BOLD directory - look for taskXXX_runXXX subdirectories
			taskfolders_sub = set([])
			for folder in ofbucket.list(prefix='%stask'%kname,delimiter='/'):
				taskfoldername = folder.name.encode('utf-8').split('/')[-2]
				if not taskfoldername in tasks:
					tasks.add(taskfoldername)
					if sub_ind>0:
						print '*** ERROR: %d previous subjects did not have this task folder! (%s)' % (sub_ind,taskfoldername)
				taskfolders_sub.add(taskfoldername)
			#print tasks
		#print s, shortname, shortname in subject_folders, kname
		shortnames.append(shortname)
	folders_and_statuses = zip(subject_folders,[f in shortnames for f in subject_folders])
	tasks_and_statuses = zip(tasks,[t in taskfolders_sub for t in tasks])
	# create a dict mapping folders to true/false (there will be an instance of this dict for each subject)
        sub_dict = {folder:status for folder,status in folders_and_statuses}
	taskdict_sub = {taskfolder:status for taskfolder,status in tasks_and_statuses}
	all_subs_folders[s] = sub_dict
	all_subs_tasks[s] = taskdict_sub
	#print 'Finished subject %d.'%sub_ind

print 'All subjects must have these folders: %s'%subject_folders
print 'All subjects must have these tasks/runs: %s'%tasks

#print all_subs_folders
#print all_subs_tasks

for sub in all_subs_folders:
	fstats = all_subs_folders[sub]
	tstats = all_subs_tasks[sub]
	missing_key = set([])
	missing_task_key = set([])
	if len(fstats.keys())!=len(subject_folders): #this subject's dict is missing a key, like it didn't have a folder that was later seen to be necessary
		missing_key = set(subject_folders) - set(fstats.keys())
	if len(tstats.keys())!=len(tasks): # this subject's task dict is missing a key... (as above)
		missing_task_key = tasks - set(tstats.keys())
	missing_val = set([fol for fol in subject_folders if not fstats[fol]])
	missing_task_val = set([tfol for tfol in tasks if not tstats[tfol]])
	all_missing = missing_key.union(missing_val)
	all_missing_tasks = missing_task_key.union(missing_task_val)
	if len(all_missing)>0:
		print '%s is missing folders: %s'%(sub, all_missing)
	if len(all_missing_tasks)>0:
		print '%s is missing tasks: %s'%(sub, all_missing_tasks)

if this_tlfcount[spec_names['task_key.txt']]: # task_key exists
	pass
