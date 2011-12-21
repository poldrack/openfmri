#!/usr/bin/env
"""  combine betaseries ROI estimates for good conditions
"""

import os


basedir='/scratch/01329/poldrack/openfmri/shared2/'
outdir='/scratch/01329/poldrack/openfmri/analyses/resid/'

studies=[s for s in os.listdir(basedir) if s.find('ds')==0]

for study in studies:
    subs=[s for s in os.listdir(basedir+study) if s.find('sub')==0]
    for sub in subs:
            rundirs=[s for s in os.listdir('%s%s/%s/model/model001'%(basedir,study,sub)) if s.find('.feat')>1]
            for r in rundirs:
                rd='%s%s/%s/model/model001/%s'%(basedir,study,sub,r)
                outfile=outdir+'%s_%s_%s_resid.txt'%(study,sub,r.replace('.feat',''))
                f=open(outfile,'w')
                rf=rd+'/stats/res4d_sc.txt'
                if not os.path.exists(rf):
                        print 'problem with '+rf
                else:
                        rf_file=open(rf,'r')
                        for l in rf_file.readlines():
                            f.write(l)
                        rf_file.close()
                f.close()
