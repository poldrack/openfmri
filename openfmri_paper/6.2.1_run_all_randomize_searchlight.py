
f=open('6.2.1_run_all_randomize_searchlight.sh','w')

for i in range(500):
    cmd='python 6.2_classify_task_searchlight_randomize.py %d'%i
    f.write(cmd+'\n')
f.close()
