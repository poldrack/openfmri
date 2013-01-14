"""
create polar task fingerprint plots
"""

import matplotlib.pyplot as plt
import numpy as N

outdir='/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_Dec2012/ICA_smoothed_6mm/task_projection_figure'

datafile='/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_Dec2012/ICA_smoothed_6mm/all_mean_run1_proj_20comp.txt'


for tasknum in range(23):

    data=N.loadtxt(datafile)[tasknum,:]

    size=8
    fig = plt.figure(figsize=(size/2, size))
    #ax = fig.add_axes([1,1,1,1], polar=True, axisbg='#d5de9c')
    #plt.axes(polar=True)

    plt.plot(data,N.arange(1,21),lw=3)
    axis=plt.gca()
    xlims=axis.get_xlim()
    axis.set_ylim(0,21)
    plt.xlabel('Component loading',size=18)
    plt.ylabel('Components',size=18)
    for i in range(1,21):
        plt.plot(xlims,[i,i],'k--')
        
    plt.savefig('%s/task%d_loading_plot.pdf'%(outdir,tasknum+1),format='pdf')
    #plt.show()
