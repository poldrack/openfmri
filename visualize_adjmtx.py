#!/usr/bin/env python
""" create a figure showing an adjacency matrix in brain space
"""

import networkx as nx
import numpy as N
import matplotlib.pyplot as plt
import nibabel as nib

roilabelfile='/work/01329/poldrack/software_lonestar/atlases/sc_HO_atlas/ROIlabels.txt'

atlasroifile='/scratch/01329/poldrack/openfmri/shared2/scatlas_goodcols.npy'

adjmtxfile='resid_adjcount.txt'
thresh=10

roicoords={}
roinames={}
f=open(roilabelfile,'r')
for l in f.readlines():
    l_s=l.strip().split('\t')
    if not l_s[0]=='ROI':
        # convert coords to voxel index space
        roicoords[int(l_s[0])]=[int(l_s[1]),int(l_s[2]),int(l_s[3])]
        roinames[int(l_s[0])]=l_s[4]

atlasrois=N.load(atlasroifile)[0]
atlasroipositions_xy={}
atlasroipositions_xz={}
atlasroipositions_yz={}

for r in range(len(atlasrois)):
    atlasroipositions_xy[r]=roicoords[atlasrois[r]+1][0:2]
    atlasroipositions_xz[r]=[roicoords[atlasrois[r]+1][0],roicoords[atlasrois[r]+1][2]]
    atlasroipositions_yz[r]=roicoords[atlasrois[r]+1][1:3]
    
# create dictionary for positions of each ROI


# create nx graph adj. matrix

adj=N.genfromtxt(adjmtxfile)
adj=adj*(adj>thresh).astype('int')

G=nx.from_numpy_matrix(adj)

weights = [x[2]['weight'] for x in G.edges(data=True)]
weights=weights-N.min(weights)+1
# draw graph

plt.figure(num=None,figsize=(12,8))

plt.subplot(221)
#plt.imshow(anat_xy)
nx.draw_networkx(G,pos=atlasroipositions_xy,with_labels=False,node_size=10,edge_color=weights,edge_cmap=plt.cm.Reds,width=4)

plt.subplot(222)
#plt.imshow(anat_yz)

nx.draw_networkx(G,pos=atlasroipositions_xz,with_labels=False,node_size=10,edge_color=weights,edge_cmap=plt.cm.Reds,width=4)

plt.subplot(223)

nx.draw_networkx(G,pos=atlasroipositions_yz,with_labels=False,node_size=10,edge_color=weights,edge_cmap=plt.cm.Reds,width=4)


plt.show()

#plt.savefig(',dpi=300)
#plt.show()

