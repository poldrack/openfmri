#!/usr/bin/env
"""  combine betaseries ROI estimates for good conditions
"""

import os

goodconds={'ds001':{1:[1,2,3,4]},'ds002':{3:[1,2]},'ds005':{1:[1]},'ds006':{1:[1,2,3,4]},'ds007':{1:[1,2,3],2:[1,2,3],3:[1,2,3]},'ds008':{1:[1,2,3],2:[1,2,3]},'ds011':{4:[1,2]},'ds017A':{2:[1,2,3,4,5]}, 'ds018':{1:[1],2:[1,2,3]},'ds051':{1:range(1,17)},'ds052':{1:[1,2],2:[1,2]},'ds101':{1:[1,3]},'ds102':{1:[1,3]}}

basedir='/scratch/01329/poldrack/openfmri/shared2/'
outdir='/scratch/01329/poldrack/openfmri/analyses/betaseries/'

for study in goodconds.iterkeys():
    subs=[s for s in os.listdir(basedir+study) if s.find('sub')==0]
    for sub in subs:
        for task in goodconds[study].iterkeys():
            rundirs=[s for s in os.listdir('%s%s/%s/model/model001'%(basedir,study,sub)) if s.find('task%03d'%task)==0 and s.find('.feat')>1]
            for r in rundirs:
                rd='%s%s/%s/model/model001/%s'%(basedir,study,sub,r)
                outfile=outdir+'%s_%s_%s_bs.txt'%(study,sub,r.replace('.feat',''))
                f=open(outfile,'w')
                bsfiles=[]
                for ev in goodconds[study][task]:
                    bsfiles.append(rd+'/betaseries/ev%d_lsone.nii.gz'%ev)
                    bsf=rd+'/betaseries/ev%d_lsone_sc.txt'%ev
                    if not os.path.exists(bsf):
                        print 'problem with '+bsf
                    else:
                        bsf_file=open(bsf,'r')
                        for l in bsf_file.readlines():
                            f.write(l)
                        bsf_file.close()
                f.close()
                cmd='fslmerge -t %s/all_lsone.nii.gz %s'%(rd,' '.join(bsfiles))
                print cmd
