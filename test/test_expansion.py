"""
test the polynomial expansion
"""

import numpy as np
from gsMk import PCE
from gsMk.GSA.train_construct import build_xy


def test_poly_expand1():
    pce = PCE(nvar=2, nord=2)
    orders = pce.order_list

    x = [[0, 0],
         [1, 2]]
    x = np.array(x)
    xexpand = [[1, 0, 0, 0, 0, 0],
               [1, 2, 1, 4, 1, 2]]
    y = []

    Xbuild, _ = build_xy(orders, 'Plain', x, y)
    np.testing.assert_array_equal(Xbuild, np.array(xexpand))

def test_poly_expand2():
    pce = PCE(nvar=2, nord=2)
    orders = pce.order_list

    x = [[0, 0],
         [1, 2]]
    x = np.array(x)
    xexpand = [[1, 0, 0, -1, -1, 0],
               [1, 2, 1, 3, 0, 2]]
    y = []

    Xbuild, _ = build_xy(orders, 'Herm', x, y)
    np.testing.assert_array_equal(Xbuild, np.array(xexpand))


def test_poly_expand_der():
    pce = PCE(nvar=2, nord=2)
    orders = pce.order_list

    x = [[0, 0],
         [1, 2]]
    x = np.array(x)
    xexpand = [[1, 0, 0, 0, 0, 0],
               [1, 2, 1, 4, 1, 2],
               [0, 0, 1, 0, 0, 0],
               [0, 1, 0, 0, 0, 0],
               [0, 0, 1, 0, 2, 2],
               [0, 1, 0, 4, 0, 1]]
    y = []

    Xbuild, _ = build_xy(orders, 'Plain', x, y, x)
    np.testing.assert_array_equal(Xbuild, np.array(xexpand))



def test_expand_time1():
    pce = PCE(nvar=20, nord=3)
    orders = pce.order_list
    import time
    tic = time.time()
    x = np.random.uniform(0, 1, [10000, 20])
    XX, _ = build_xy(orders, 'Plain', x, [])
    toc = time.time()
    print('Expansion time = %.2f min' % ((toc - tic) / 60.))
    print XX.shape
    assert 1 == 1

