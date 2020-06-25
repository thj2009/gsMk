# Polynomial Chaose Expansion Order Scheme


import numpy as np
from scipy import sparse

class Node(object):
    '''
    Tree Object
    '''
    def __init__(self, data):
        self.data = data 
        self.children = []
    def add_child(self, obj):
        self.children.append(obj)
        
def combination_print(tree, order_list, parent):
    '''
    Retrieve the tree dataset
    '''
    parent_copy = parent[:]         # store the order_listrmation of parents
    if tree.children != []:
        if tree.data != None:
            parent_copy.append(tree.data)
        for child in tree.children:
            combination_print(child, order_list, parent_copy)
    else:
        if tree.data != None:
            parent_copy.append(tree.data)
            order_list.append(parent_copy)
    return(order_list, parent_copy)

def tree_building(tree, nvar, pt, jt):
    '''
    Construct a tree with 
    depth nvar, 
    totol order pt, 
    interaction jt: number of nonzero term
    '''
#    print('New tree', nvar, pt, jt)
    if nvar == 1 and (jt != 0 or pt == 0):
        nn = Node(pt)
        tree.add_child(nn)
    else:
        for ii in range(pt+1):
            next_pt = pt - ii
            if ii == 0:
                next_jt = jt
            else:
                next_jt = jt - 1
#            print('   Next Tree', nvar-1, next_pt, next_jt)
            if next_jt <= nvar - 1 \
            and next_jt <= next_pt \
            and (next_jt > 0 or (next_jt == 0 and next_pt == 0)):
#            and next_pt - next_jt != 1 \

                nn = Node(ii)
                tree.add_child(nn)
                tree_building(nn, nvar-1, next_pt, next_jt)
            else:
                pass
#                print('dead')

def single_combination(nvar, order, jt, max_order, qnorm):
    '''
    construct the single combination with 
    nvar: number of variable
    order: sum to order
    jt: interaction
    max_order: maximum order including
    qnorm: qnnorm constraint
    '''
    # print(nvar, order, jt)
    order_list = [] 
    if nvar >= jt:
        test = np.zeros(nvar)
        for ii in range(jt-1):
            test[ii] = 1
        if nvar != jt:
            test[jt] = order - jt
        min_norm = np.linalg.norm(test, qnorm)
        # print(nvar, order, jt)
        # print(min_norm, np.linalg.norm(test, qnorm), max_order)
        # print(test, qnorm)
        # print(min_norm, max_order + 1e-4)
        # print('------------------')
        # print('===========')
        if min_norm <= max_order + 1e-4:
            # print(nvar, order, jt)
            
            parent = []
            tree = Node(None)
            tree_building(tree, nvar, order, jt)
            order_list, parent = combination_print(tree, order_list, parent)
            # print(order_list)
            # print('======================')
            # print(order_list)
            # print('********')
            # print(order_list)
            # temp = np.array(order_list)
            order_list = [o for o in order_list if np.linalg.norm(o, qnorm) <= max_order + 1e-4]
            # # check norm constraint
            # norm_cal = [np.linalg.norm(temp[ii, :], qnorm) for ii in range(len(order_list))]
            # norm_cal = np.array(norm_cal)
            # # Select the term satisfy the qnorm constraint
            # sat_ = np.argwhere(norm_cal <= max_order).T[0]
            # order_list = [order_list[ii] for ii in sat_]
    return order_list

def total_combination(nvar, order, jtmax=np.inf, qnorm=1):
    '''
    return the Total Combination with
    nvar: number of variable
    order: total order
    qnorm : qnorm constraint
    '''
    order_list = []
    for sum_order in range(order + 1):
        for jt in range(min(sum_order+1, jtmax+1)):
            order_list += single_combination(nvar, sum_order, jt, order, qnorm)
#            print(nvar, sum_order, jt)
#            print(single_combination(nvar, sum_order, jt, order, qnorm))
#            print('==========================')
    return order_list

def single_combination_maxorder(nvar, order, jtmax=np.inf, max_order=np.inf, qnorm=1):
    order_list = []
    for jt in range(min(order+1, jtmax+1)):
        order_list += single_combination(nvar, order, jt, max_order, qnorm)
    return order_list


if __name__ == '__main__':
    nvar = 3
    order = 2
    jtmax = 2
    qnorm = 0.5
#    
##    tic = time.clock()
##    XX = []
##    XX = Tot_Combi_cal(M, order, qnorm)   
##    print XX
##    print len(XX)
##    print math.factorial(M+order)/(math.factorial(order)*math.factorial(M))
##    toc = time.clock()
##    print '==================='
##    print 'Time = %f' %((toc-tic)/60.)
##    for i in range(order + 1):
##        print(nvar, i)
##        print(single_combination_maxorder(nvar, i, jtmax, order, qnorm))
##    print(len(total_combination(nvar, order, jtmax, qnorm)))
    tot = total_combination(nvar, order, jtmax, qnorm)
    print(tot)
##    print('Single Combination')
##    print(single_combination(3, 0, jtmax, 100 ,1))
    from math import factorial as fac
    print(fac(nvar + order)/(fac(nvar) * fac(order)))
    print(len(tot))
#    print(len(tot))
#    a = total_combination(1 , 2, 10, 1)
#    print(a)
    
#    nvar = 3
#    order = 3
#    jt = 2
#    qnorm = 1
##   test tree building
#    order_list = []
#    parent = []
#    tree = Node(None)
#    tree_building(tree, nvar, order, jt)
#    order_list, parent = combination_print(tree, order_list, parent)
#    print(order_list)

#    tree_building(tree, 1, 2, 1)
