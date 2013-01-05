
f=open('6.1.1_run_all_searchlight.sh','w')

for i in range(100):
    cmd='python 6_classify_task_searchlight.py %d'%i
    f.write(cmd+'\n')
f.close()
