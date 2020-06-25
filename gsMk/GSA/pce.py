'''
Basis Polynomial Chaos Expansion Modeling

Ref: Sudret, Bruno. "Global sensitivity analysis using polynomial chaos expansions."
Reliability engineering & system safety 93.7 (2008): 964-979.
https://www.sciencedirect.com/science/article/pii/S0951832007001329
'''

import numpy as np
import itertools
from collections import Counter
from sklearn import linear_model
from sklearn.model_selection import KFold

from .order_scheme import total_combination
from .poly import Hermite, Plain, Legendre
from .train_construct import build_xy

class PCE:
    '''
    Class: polynomial chaos expansion
    nvar: number of variable
    nord: maximum order of multivariate polynomial
    polytype: multivariate type, default: 'Herm'
              available options: 'Herm', 'Legd', 'Plain'
    withdev: whether include the derivative information
    copy_xy: whether store the expanded X and Y for further checking, default False
    regr: regression scheme, default 'OLS'
          available options: 'OLS', 'Lasso', 'Ridge', 'LassoCV', 'RidgeCV'
    jtmax: maximum interaction term, default np.inf
    qnorm: normal of interaction, default 1
    order_list: prededined order list for expansion, default None
    '''
    def __init__(self, nvar, nord, polytype='Herm',
                 withdev=True, copy_xy=False, regr='OLS', 
                 jtmax=np.inf, qnorm=1, order_list=None):
        self.nvar = nvar
        self.nord = nord
        self.jtmax = jtmax
        self.qnorm = qnorm
        self.polytype = polytype
        self.withdev = withdev
        self.copy_xy = copy_xy
        self.regr = regr
        if order_list is None:
            self.order_list = self.generate_order()
        else:
            self.order_list = order_list
        self.coef = None
        self.cov_coef = None

        self.plain_order = None
        self.plain_coef = None
        self.trans_mat = None

        self.x = None
        self.y = None
        self.xdev = None
        self.dydx = None
        self.X = None
        self.Y = None

        # sobol indices
        self.svar = None

    def generate_order(self):
        order_list = total_combination(self.nvar, self.nord, self.jtmax, self.qnorm)
        return order_list

    def fit(self, x, y, xdev=[], dydx=[],  weights=1, uncer=False, njob=1):
        '''
        fit polynomial chaos expansion model, given data w/wo derivative
        input:
            x: input dataset, array-like Nd by nvar
            y: output dataset, array-like Nd
            xdev: input dataset correspond to derivative info, default [], Nd by nvar
            dydx: output dy/dx, default [], Nd by nvar
            weights: weights on each datapoints, arraylike, default 1
            uncer: whether calculate uncertainty on the parameters with information matrix,
                   default: False
            njob: number of job in expansion with parallel backend "joblib"
        the regression parameters is stored in self.coef
        '''
        x = np.array(x)
        assert np.shape(x)[1] == self.nvar
        assert np.shape(x)[0] == np.shape(y)[0]
        if self.withdev:
            assert np.shape(xdev)[1] == self.nvar
            assert np.shape(dydx)[0] == len(dydx)
            for term in dydx:
                assert len(term) == self.nvar
        # build X, Y for pce fitting
        X, Y = build_xy(self.order_list, self.polytype, x, y, xdev, dydx)
        if self.copy_xy:
            self.x = x
            self.y = y
            self.xdev = xdev
            self.dydx = dydx
            self.X = X
            self.Y = Y
        # Linear Regressor
        if self.regr == 'OLS':
            clf = linear_model.LinearRegression(fit_intercept=False, copy_X=False)
        elif self.regr == 'Lasso':
            clf = linear_model.Lasso(alpha=1e-5, fit_intercept=False,
                                     copy_X=False, max_iter=1e3,
                                     selection = 'random')
        else:
            raise ValueError(self.regr, 'is not a valid regressor')
        print('Logarithm of determinant of Information Matrix = ', np.linalg.slogdet(X.T.dot(X)))
        print('Rank of Information Matrix = ', np.linalg.matrix_rank(X.T.dot(X)))
        if weights == 1:
            weightsX = np.copy(X)
            weightsY = np.copy(Y)
        else:
            weightsX = np.diag(weights).dot(X)
            weightsY = np.diag(weights).dot(Y)
        clf.fit(weightsX, weightsY)
        self.coef = clf.coef_


    def predict(self, xpred):
        '''
        predict the output, given input xpred
        input:
            xpred: array-like, Nd by nvar
        output:
            sampled output: Nd
        '''
        Xpred, _ = build_xy(self.order_list, self.polytype, xpred, [])
        ypred = Xpred.dot(self.coef)
        return ypred

    def sobol_svar(self):
        if self.polytype == 'Herm':
            Poly = Hermite
        elif self.polytype == 'Plain':
            Poly = Plain
        elif self.polytype == 'Legd':
            Poly = Legendre
        else:
            raise ValueError("%s is not available" % self.polytype)
        
        svar = []
        for i, order in enumerate(self.order_list):
            sv = self.coef[i] ** 2
            for o in order:
                sv *= Poly(order=o).int(p=2)
            svar.append(sv)
        self.svar = svar
        return svar
    def sobol_index(self, indices=[0]):
        """
        Sobol Index
        """
        if self.svar is None:
            svar = self.sobol_svar()
        else:
            svar = self.svar
        DPC = np.sum(svar[1:])
        # print(DPC)
        St = 0
        for i, order in enumerate(self.order_list):
            sv = svar[i]
            flag = True
            for idx in range(self.nvar):
                if idx in indices and order[idx] == 0:
                    flag = False
                if idx not in indices and order[idx] != 0:
                    flag = False 
            if flag:
                St += svar[i]
        return St / float(DPC)

    def sobol_totalindex(self, indices=[0]):
        """
        Sobol Total Index
        """
        if self.svar is None:
            svar = self.sobol_svar()
        else:
            svar = self.svar

        DPC = np.sum(svar[1:])
        St = 0
        for i, order in enumerate(self.order_list):
            sv = svar[i]
            flag = True
            for idx in indices:
                if order[idx] == 0:
                    flag = False
            if flag:
                St += svar[i]
        return St / float(DPC)
        
