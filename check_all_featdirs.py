from openfmri_utils import *
import os

for root,dirs,files in os.walk('/corral/utexas/poldracklab/openfmri/staged'):
#    for f in files:
        if root.rfind('.feat')==(len(root)-5):
 #           print 'found %s'%root
            foo=check_featdir(root)
 
