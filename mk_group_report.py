#!/usr/bin/env python
""" mk_group_report - create a report showing all activation maps for a study

USAGE: python mk_group_report.py <basedir - default is pwd>
"""

## Copyright 2011, Russell Poldrack. All rights reserved.

## Redistribution and use in source and binary forms, with or without modification, are
## permitted provided that the following conditions are met:

##    1. Redistributions of source code must retain the above copyright notice, this list of
##       conditions and the following disclaimer.

##    2. Redistributions in binary form must reproduce the above copyright notice, this list
##       of conditions and the following disclaimer in the documentation and/or other materials
##       provided with the distribution.

## THIS SOFTWARE IS PROVIDED BY RUSSELL POLDRACK ``AS IS'' AND ANY EXPRESS OR IMPLIED
## WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
## FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL RUSSELL POLDRACK OR
## CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
## CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
## SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
## ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
## NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
## ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.



import os,sys
from run_shell_cmd import *
from openfmri_utils import *

def usage():
    """ print the docstring and exit"""
    sys.stdout.write(__doc__)
    sys.exit(2)


#def main():
if 1==1:
    if len(sys.argv)>1:
        basedir=sys.argv[1]
    else:
        basedir=os.curdir
    print 'using basedir: %s'%basedir
    contrasts=load_contrastkey(basedir+'/contrast_key.txt')

    outfilename=basedir+'/group_stats_report.html'
    outfile=open(outfilename,'w')
    outfile.write('<html>\n<body>\n')

    for task in contrasts.iterkeys():
        for c in contrasts[task].iterkeys():
            cnum=int(c.replace("contrast",''))
            pngfile=basedir+'/group/%s/cope%03d.gfeat/cope1.feat/rendered_thresh_zstat1.png'%(task,cnum)
            outfile.write('%s %s cope%03d (%s)<br>\n'%(basedir,task,cnum,contrasts[task][c]))
            outfile.write('<img src="%s" width=100%%/>\n'%pngfile)
    
    outfile.write('</body>\n</html>\n')
    outfile.close()

#if __name__ == '__main__':
#   main()
