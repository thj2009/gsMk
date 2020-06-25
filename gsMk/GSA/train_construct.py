"""
Build Training dataset give orderlist and polynomial type
"""

import numpy as np

from .poly import Hermite, Plain, Legendre

def build_xy(order_list, poly, x, y, xdev=[], dydx=[]):
    '''
    build large X, Y for linear regression
    '''
    X = expand_x(order_list, x, poly)
    Y = np.array(y).flatten()
    if len(xdev) != 0:
        Xdev = expand_dev_xy(order_list, xdev, poly)
        Dydx = np.array(dydx).flatten()
        X = np.vstack((X, Xdev))
        Y = np.append(Y, Dydx)
    return X, Y

def expand_dev_single(order_list, _x, Poly):

    nvar = len(_x)
    norder = len(order_list)
    no = len(order_list[0])
    _XX = np.empty([nvar, norder], dtype=float)
    xx = np.empty((norder,), dtype=float)


    for i in range(nvar):
        xx = np.empty((norder,), dtype=float)
        for j in range(norder):
            order = order_list[j]
            _xx = 0
            if order[i] != 0:
                _xx = 1
                for k in range(no):
                    o = order[k]
                    if o != 0:
                        if k != i:
                            _xx *= Poly(order=o).evaluate(_x[k])
                        else:
                            _xx *= Poly(order=o).der(m=1).evaluate(_x[k])
            xx[j] = _xx
        _XX[i, :] = xx
    return _XX


def expand_x(order_list, x, polytype):
    '''
    expand x according to orderlist
    '''
    if polytype == 'Herm':
        Poly = Hermite
    elif polytype == 'Plain':
        Poly = Plain
    elif polytype == 'Legd':
        Poly = Legendre
    else:
        raise ValueError("%s is not available" % polytype)

    ndata = np.shape(x)[0]
    nvar = np.shape(x)[1]
    norder = len(order_list)
    no = len(order_list[0])

    X = np.empty((ndata, norder), dtype=float)      # initialize the input matrix X
    xx = np.ones((ndata, ), dtype=float)


    for i in range(norder):
        order = order_list[i]
        xx = np.ones((ndata, ), dtype=float)
        for j in range(no):
            o = order[j]
            xx *= Poly(order=o).evaluate(x[:, j])
        X[:, i] = xx
    return X



def expand_dev_xy(order_list, xdev, polytype):
    if polytype == 'Herm':
        Poly = Hermite
    elif polytype == 'Plain':
        Poly = Plain
    elif polytype == 'Legd':
        Poly = Legendre
    else:
        raise ValueError("%s is not available" % polytype)
    
    nx = np.shape(xdev)[0]
    nvar = np.shape(xdev)[1]
    
    Xfull = [expand_dev_single(order_list, _x, Poly) for _x in xdev]
    Xfull = np.concatenate(Xfull, axis=0)
    return Xfull
