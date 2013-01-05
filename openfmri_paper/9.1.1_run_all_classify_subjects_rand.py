
f=open('9.1.1_run_all_classify_subjects_rand.sh','w')

for i in range(500):
    cmd='python 9.1_classify_subjects_rand.py %d'%i
    f.write(cmd+'\n')
f.close()
