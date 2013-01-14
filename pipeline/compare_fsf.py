import sys

f1='/corral/utexas/poldracklab/openfmri/staged/ds103/cope1.gfeat/design.fsf'
f2='/corral/utexas/poldracklab/openfmri/staged/ds103/group/task001/cope001.fsf'

f=open(f1,'r')
f1dict={}
for l in f.readlines():
    l=l.strip()
    if len(l)==0:
        continue
    if l[0]=='#' or l.find('set')<0:
        continue
    #print l
    f1dict[l.split(' ')[1]]=' '.join(l.split(' ')[2:])

f=open(f2,'r')
f2dict={}
for l in f.readlines():
    l=l.strip()
    if len(l)==0:
        continue
    if l[0]=='#' or l.find('set')<0:
        continue
    #print l
    f2dict[l.split(' ')[1]]=' '.join(l.split(' ')[2:])

for k in f1dict.iterkeys():
    if not f2dict.has_key(k):
        print 'f2 missing key: %s'%k
    elif not f1dict[k]==f2dict[k]:
        print 'diff: %s %s %s'%(k,f1dict[k],f2dict[k])

for k in f2dict.iterkeys():
    if not f1dict.has_key(k):
        print 'f1 missing key: %s'%k
