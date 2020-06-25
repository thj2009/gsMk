import numpy as np
import numpy.polynomial.hermite_e as her
import numpy.polynomial.legendre as legd

class Polynomial(object):
    '''
    class: polynomial class
    '''
    def __init__(self, order, coef):
        self.order = order
        self.coef = coef

    def __str__(self):
        string = 'P(x)='
        for i, c in enumerate(self.coef):
            string += '%+.2f'%c + '*x^%d' %i
        if self.coef.any() == 0:
            string += '0'
        return string

    def evaluate(self, x):
        px = 0
        for i, c in enumerate(self.coef):
            px += c * x ** i
        return px

    def der(self, m=1):
        coef = np.copy(self.coef)
        if m == 0:
            return Polynomial(self.order, self.coef)
        if len(coef) in [0, 1]:
            return Polynomial(0, np.array([0]))
        for de in range(m):
            coef = np.array([i*c for i,c in enumerate(coef) if i!=0])
        return Polynomial(len(coef)-1, coef)

    def int(self, p=1):
        pass

class Hermite(Polynomial):
    '''
    Hermite Polynomial Class
    '''
    def __init__(self, order):
        self.order = order
        Polynomial.__init__(self, order, self.her_coef())

    def her_coef(self):
        c = [0] * self.order + [1]
        return her.herme2poly(c)

    def int(self, p=1):
        pass

class Plain(Polynomial):
    '''
    Plain Polynomial Class
    '''
    def __init__(self, order):
        self.order = order
        Polynomial.__init__(self, order, self._coef())

    def _coef(self):
        c = [0] * self.order + [1]
        return np.array(c)

    def int(self, p=1):
        pass        


class Legendre(Polynomial):
    '''
    Hermite Polynomial Class
    '''
    def __init__(self, order):
        self.order = order
        Polynomial.__init__(self, order, self.legd_coef())

    def legd_coef(self):
        c = [0] * self.order + [1]
        return legd.leg2poly(c)

    def int(self, p=1):
        if p == 1:
            if self.order == 0:
                return 1
            else:
                return 0
        elif p == 2:
            return 1. / (2 * self.order + 1)


if __name__ == '__main__':
    for o in range(6):
        l = Legendre(order=o)
#        l = Hermite(order=o)
        print(l)
        print(l.der())
        print('-----------')