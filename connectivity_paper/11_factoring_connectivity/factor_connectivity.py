#!/usr/bin/env python
"""
factor the connectivity matrix for the entire dataset
"""

import numpy as N

basedir='/scratch/01329/poldrack/openfmri/analyses/connectivity_paper/'

datatype='resid'
data=N.load(basedir+'10_classification/%s_data_for_classification.npy'%datatype)
