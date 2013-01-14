"""
rename model001 to model001_fsl4
"""

import os
import glob
import shutil
import run_shell_cmd

dirs=glob.glob('ds*/sub*/model/model001')

# make target dirs

for d in dirs:
    print d
    newdir=d+'_fsl4'
    if not os.path.exists(newdir):
        os.mkdir(newdir)

    to_copy=glob.glob(os.path.join(d,'*.gfeat'))
    #if 0:
    for c in to_copy:
        cmd='cp -r %s %s'%(c,newdir)
        print cmd
        run_shell_cmd.run_shell_cmd(cmd)

    if 0:
      for c in to_copy:
        if os.path.exists(c.replace('model001','model001_fsl4')):
            cmd='rm -rf %s'%c
            print cmd
            run_shell_cmd.run_shell_cmd(cmd)
                        
