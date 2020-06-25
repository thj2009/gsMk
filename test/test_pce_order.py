import pytest
import numpy as np

from gsMk import PCE

def test_order1():
    pce = PCE(nvar=3, nord=2)
    orders = [[0, 0, 0],
              [1, 0, 0],
              [0, 1, 0],
              [0, 0, 1],
              [2, 0, 0],
              [0, 2, 0],
              [0, 0, 2],
              [1, 1, 0],
              [1, 0, 1],
              [0, 1, 1]]
    pce_order = pce.order_list
    assert len(orders) == len(pce_order)
    for o in pce_order:
        assert o in orders


def test_order2():
    pce = PCE(nvar=3, nord=2, jtmax=1)
    orders = [[0, 0, 0],
              [1, 0, 0],
              [0, 1, 0],
              [0, 0, 1],
              [2, 0, 0],
              [0, 2, 0],
              [0, 0, 2]]
    pce_order = pce.order_list
    assert len(orders) == len(pce_order)
    for o in pce_order:
        assert o in orders


def test_order3():
    pce = PCE(nvar=3, nord=2, qnorm=0.5)
    orders = [[0, 0, 0],
              [1, 0, 0],
              [0, 1, 0],
              [0, 0, 1],
              [2, 0, 0],
              [0, 2, 0],
              [0, 0, 2]]
    pce_order = pce.order_list
    assert len(orders) == len(pce_order)
    for o in pce_order:
        assert o in orders


def test_order4():
    nvar = 10
    nord = 5
    pce = PCE(nvar=nvar, nord=nord, qnorm=1)
    from math import factorial as fac
    num_order = fac(nvar + nord) / (fac(nvar) * fac(nord))
    assert num_order == len(pce.order_list)

