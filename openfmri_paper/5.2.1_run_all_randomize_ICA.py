
f=open('5.2.1_run_all_randomize_ICA.sh','w')

for i in range(1000):
    cmd='python 5.2_classify_task_ICA_randperm.py %d'%i
    f.write(cmd+'\n')
f.close()
