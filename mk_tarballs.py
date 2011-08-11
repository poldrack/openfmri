tbdir='/corral/utexas/poldracklab/openfmri/tarballs'

f=open('sublist_ds103','r')
for l in f.readlines():
    l=l.strip().lstrip('./')
    l_s=l.split('/')
    subcode='%s_%s'%(l_s[0],l_s[1])
    print 'cp %s/*_key.txt %s'%(l_s[0],l)
    print 'cp %s/README* %s'%(l_s[0],l)
    print 'tar zcvf %s/%s.tgz %s/behav %s/BOLD/*/bold.nii.gz %s/anatomy/highres*.nii.gz %s/anatomy/inplane*.nii.gz %s/README* %s/*key.txt'%(tbdir,subcode,l,l,l,l,l,l)
