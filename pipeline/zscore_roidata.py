import numpy as N
f=open('ev2_lsone_scatlas_roi.txt','r')
l= f.readlines()
f.close()
ntp=len(l[0].strip().split('\t'))
nroi=len(l)
data=N.zeros((ntp,nroi))
ctr=0
for line in l:
    data[:,ctr]=[float(x) for x in line.strip().split('\t')]
    ctr=ctr+1
cor=N.corrcoef(data.T)

colmean=N.mean(data,1)
colstd=N.std(data,1)
zdata=N.zeros(data.shape)

for col in range(data.shape[0]):
    zdata[col,:]=(data[col,:]-colmean[col])/colstd[col]
