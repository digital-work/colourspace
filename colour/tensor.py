#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tensor: Compute colour metric tensors as data.TensorData objects.

Copyright (C) 2013 Ivar Farup

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import numpy as np
import data
import space

#==============================================================================
# Colour metric tensors
#==============================================================================

def euclidean(sp, dat):
    """
    Compute the general Euclidean metric in the given colour space as TensorData.
    
    Parameters
    ----------
    sp : Space
        The colour space in which the metric tensor is Euclidean.
    dat : Data
        The colour points for which to compute the metric.
        
    Returns
    -------
    Euclidean : TensorData
        The metric tensors.
    """
    g = sp.empty_matrix(dat.linear_XYZ)
    for i in range(np.shape(g)[0]):
        g[i] = np.eye(3)
    return data.TensorData(sp, dat, g)

def dE_ab(dat):
    """
    Compute the DEab metric as TensorData for the given data points.

    Parameters
    ----------
    dat : Data
        The colour points for which to compute the metric.
        
    Returns
    -------
    DEab : TensorData
        The metric tensors.
    """
    return euclidean(space.cielab, dat)

def dE_uv(dat):
    """
    Compute the DEuv metric as TensorData for the given data points.

    Parameters
    ----------
    dat : Data
        The colour points for which to compute the metric.
        
    Returns
    -------
    DEuv : TensorData
        The metric tensors.
    """
    return euclidean(space.cieluv, dat)

def dE_00(dat, k_L=1, k_C=1, k_h=1):
    """
    Compute the CIEDE00 metric as Tensordata for the given data points.
    
    Parameters
    ----------
    dat : Data
        The colour points for which to compute the metric.
    k_L : float
        Parameter of the CIEDE00 metric
    k_C : float
        Parameter of the CIEDE00 metric
    k_h : float
        Parameter of the CIEDE00 metric
        
    Returns
    -------
    DE00 : TensorData
        The metric tensors.
    """
    lch = dat.get_linear(space.ciede00lch)
    L = lch[:,0]
    C = lch[:,1]
    h = lch[:,2]
    h_deg = np.rad2deg(h)
    h_deg[h_deg < 0] = h_deg + 360
    S_L = 1 + (0.015 * (L - 50)**2) / np.sqrt(20 + (L - 50)**2)
    S_C = 1 + 0.045 * C
    T = 1 - 0.17 * np.cos(np.deg2rad(h_deg - 30)) + \
        .24 * np.cos(2*h) + \
        .32 * np.cos(np.deg2rad(3 * h_deg + 6)) - \
        .2 * np.cos(np.deg2rad(4 * h_deg - 63))
    S_h = 1 + 0.015 * C * T
    R_C = 2 * np.sqrt(C**7 / (C**7 + 25**7))
    d_theta = 30 * np.exp(-((h_deg - 275) / 25)**2)
    R_T = - R_C * np.sin(np.deg2rad(2 * d_theta))
    g = space.ciede00lch.empty_matrix(lch)
    g[:,0,0] = (k_L * S_L)**(-2)
    g[:,1,1] = (k_C * S_C)**(-2)
    g[:,2,2] = C**2 * (k_h * S_h)**(-2)
    g[:,1,2] = .5 * C * R_T / (k_C * S_C * k_h * S_h)
    g[:,2,1] = .5 * C * R_T / (k_C * S_C * k_h * S_h)
    return data.TensorData(space.ciede00lch, dat, g)

def poincare_disk(sp, dat):
    """
    Compute the general Poincare Disk metric in the given colour space as TensorData

    Parameters
    ----------
    dat : Data
        The colour points for which to compute the metric.
        
    Returns
    -------
    Poincare : TensorData
        The metric tensors.
    """
    
    d = dat.get_linear(sp)
    g = sp.empty_matrix(d)
    for i in range(np.shape(g)[0]):
        g[i, 0, 0] = 1
        g[i, 1, 1] = 4. / (1 - d[i, 1]**2 - d[i, 2]**2)**2
        g[i, 2, 2] = 4. / (1 - d[i, 1]**2 - d[i, 2]**2)**2
    return data.TensorData(sp, dat, g)

# TODO:
#
# Functions (returning TensorData):
#     dE_00
#     stiles
#     helmholz
#     schrodinger
#     vos
#     SVF
#     CIECAM02
#     DIN99xx
#     +++

#==============================================================================
# Test module
#==============================================================================

def test():
    """
    Test entire module, and print report.
    """
    d = data.build_d_regular(space.cielab,
                             np.linspace(0, 100, 10),
                             np.linspace(-100, 100, 21),
                             np.linspace(-100, 100, 21))
    ndat = np.shape(d.get_linear(space.cielab))[0]
    gab = dE_ab(d)
    guv = dE_uv(d)
    gD = poincare_disk(space.cielab, d)
    print "Metric shapes (all should be true):"
    print np.shape(gab.get(space.xyz)) == (ndat, 3, 3)
    print np.shape(guv.get(space.xyz)) == (ndat, 3, 3)
    print np.shape(gD.get(space.xyz)) == (ndat, 3, 3)