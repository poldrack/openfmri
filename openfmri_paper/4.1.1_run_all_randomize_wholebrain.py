
f=open('4.1.2_run_all_randomize_wholebrain.sh','w')

for i in range(1000):
    cmd='python 4.1_randomize_wholebrain.py %d'%i
    f.write(cmd+'\n')
f.close()
