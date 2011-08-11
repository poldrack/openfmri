from get_partialcorr import *

f=open('lsonelist.txt','r')
lsonefiles=[l.strip() for l in f.readlines()]
f.close()

f=open('get_all_partialcorrs.sh','w')
for l in lsonefiles:
    f.write('python get_partialcorr.py %s %s\n'%(l,l.replace('roi.txt','')))
f.close()
