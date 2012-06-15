#!/usr/bin/env python
""" create gifti vector file for rendering in caret
- based on fo_write_vectors_nodes_to_CARET.m by Nico Dosenbach
"""

import scipy.io
import numpy as N

basedir='/scratch/01329/poldrack/openfmri/analyses/connectivity_paper/'
atlasdir='/work/01329/poldrack/software_lonestar/atlases/sc_HO_atlas/'

def get_roi_coords(roilabelfile='/work/01329/poldrack/software_lonestar/atlases/sc_HO_atlas/ROIlabels.txt'):
    roicoords={}
    roinames={}
    f=open(roilabelfile,'r')
    for l in f.readlines():
        l_s=l.strip().split('\t')
        if not l_s[0]=='ROI':
            # convert coords to voxel index space
            roicoords[int(l_s[0])]=[int(l_s[1]),int(l_s[2]),int(l_s[3])]
            roinames[int(l_s[0])]=l_s[4]
    return roicoords,roinames

def get_adjacency_mtx(adjmtxfile,thresh):
    adj=N.genfromtxt(adjmtxfile)
    adj=adj*(adj>thresh).astype('int')
    return adj

def mk_gifti_vector(adjmtxfile,thresh=0.0):

    template='/scratch/01329/poldrack/openfmri/analyses/connectivity_paper/11_gifti_renderings/template_vector_gii.mat'
    goodcols_file='/scratch/01329/poldrack/openfmri/analyses/connectivity_paper/1_data_preparation/scatlas_goodcols.npy'
    outfile=adjmtxfile.replace('.txt','.vector.gii')
    adj=get_adjacency_mtx(adjmtxfile,thresh)
    mk_gifti_vector_from_adjmtx(adj,outfile,thresh=thresh)

def mk_gifti_vector_from_adjmtx(adj,outfile,thresh=0.0):
    template='/scratch/01329/poldrack/openfmri/analyses/connectivity_paper/11_gifti_renderings/template_vector_gii.mat'
    goodcols_file='/scratch/01329/poldrack/openfmri/analyses/connectivity_paper/1_data_preparation/scatlas_goodcols.npy'

    m=scipy.io.loadmat(template)
    template=[x[0][0] for x in m['xml_template_text'] if len(x[0])>0]
    
    roicoords_full,roinames_full=get_roi_coords()
    
    adj=adj*(adj>thresh).astype('int')

    # get appropriate coords for this roi set
    goodcols=N.load(goodcols_file)[0]
    nrois=len(goodcols)

    adj[N.tril_indices(nrois)]=0
    edges=N.where(adj>0)
    nedges=len(edges[0])
    roicoords=N.zeros((nrois,3))

    for g in range(len(goodcols)):
        roicoords[g,:]=roicoords_full[goodcols[g]+1]

    # rescale edge sizes
    min_vect_width = 0.5
    max_vect_width =10

    edgeweight=N.zeros(nedges)
    for x in range(nedges):
        edgeweight[x]=adj[edges[0][x],edges[1][x]]
    if N.min(edgeweight)==N.max(edgeweight):
        edgeweight[:]=(max_vect_width - min_vect_width)/2.0 + min_vect_width
    else:
        edgeweight=(edgeweight-N.min(edgeweight))/(N.max(edgeweight)-N.min(edgeweight))*(max_vect_width - min_vect_width) + min_vect_width
    
    # create unit vector
    vect=N.zeros((nedges,3))
    unitvect=N.zeros((nedges,3))
    normvect=N.zeros(nedges)

    for x in range(nedges):
        vect[x,:]=roicoords[edges[1][x]] - roicoords[edges[0][x]]
        normvect[x]=N.linalg.norm(vect[x,:])
        unitvect[x,:]=vect[x,:]/normvect[x]

    # write to output file
    f=open(outfile,'w')
    for x in range(46):
        f.write(template[x]+'\n')

    # write node numbers
    for x in range(nrois):
        f.write('%d\n'%x)

    for x in range(46,68):
        f.write(template[x]+'\n')

    # write origin_x
    for x in range(nedges):
        f.write('%f\n'%roicoords[edges[0][x],0])

    for x in range(68,90):
        f.write(template[x]+'\n')

    # write origin_y
    for x in range(nedges):
        f.write('%f\n'%roicoords[edges[0][x],1])

    for x in range(90,112):
        f.write(template[x]+'\n')

     # write origin_z
    for x in range(nedges):
        f.write('%f\n'%roicoords[edges[0][x],2])

    for x in range(112,134):
        f.write(template[x]+'\n')

    # write unitvect_x
    for x in range(nedges):
        f.write('%f\n'%unitvect[x,0])

    for x in range(134,156):
        f.write(template[x]+'\n')

    # write unitvect_y
    for x in range(nedges):
        f.write('%f\n'%unitvect[x,1])

    for x in range(156,178):
        f.write(template[x]+'\n')

    # write unitvect_z
    for x in range(nedges):
        f.write('%f\n'%unitvect[x,2])

    for x in range(178,200):
        f.write(template[x]+'\n')

    # write normvect
    for x in range(nedges):
        f.write('%f\n'%normvect[x])

    for x in range(200,222):
        f.write(template[x]+'\n')

    # write connection_Weights_scaled
    for x in range(nedges):
        f.write('%f\n'%edgeweight[x])

    for x in range(222,244):
        f.write(template[x]+'\n')

    # write red
    for x in range(nedges):
        f.write('255\n')

    for x in range(244,266):
        f.write(template[x]+'\n')

    # write green
    for x in range(nedges):
        f.write('100\n')

    for x in range(266,288):
        f.write(template[x]+'\n')

    # write blue
    for x in range(nedges):
        f.write('0\n')

    for x in range(288,310):
        f.write(template[x]+'\n')

    # write alpha
    for x in range(nedges):
        f.write('1\n')

    for x in range(310,313):
        f.write(template[x]+'\n')

    f.close()



