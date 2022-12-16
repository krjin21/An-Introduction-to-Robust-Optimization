import gurobipy as gp
import math
from gurobipy import GRB
import numpy as np


def budget(e):
    ### Compute the parameters
    gamma = math.sqrt(-2 * math.log(e, math.e) * 199)
    mu = np.array([1.05 + 0.3 * ((200 - i - 1) / 199) for i in range(199)])
    sigma = np.array([0.05 + 0.6 * ((200 - i) / 199) for i in range(199)])

    ### Generate a model
    m = gp.Model('Box')
    m.setAttr('ModelSense', GRB.MAXIMIZE)
    m.Params.OutputFlag = 0

    ### Add variables
    x = []
    z = []
    absz = []
    w = []
    R = m.addVar(0, GRB.INFINITY, 1, vtype=GRB.CONTINUOUS, name='R')
    maxw = m.addVar(0, GRB.INFINITY, vtype=GRB.CONTINUOUS, name='Maxw')
    for i in range(199):
        x.append(m.addVar(lb=0, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS, name='x{}'.format(i)))
        z.append(m.addVar(vtype=GRB.CONTINUOUS, name='z{}'.format(i)))
        absz.append(m.addVar(vtype=GRB.CONTINUOUS, name='absz{}'.format(i)))
        w.append(m.addVar(vtype=GRB.CONTINUOUS, name='w{}'.format(i)))
    x.append(m.addVar(lb=0, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS, name='x199'))

    ### Add Constraints
    cons = []
    for i in range(199):
        cons.append(m.addConstr(z[i] + w[i] == sigma[i] * x[i], name='RC_Constraints{}'.format(i)))
        cons.append(m.addConstr(z[i] <= absz[i], name='Abs1_z{}'.format(i)))
        cons.append(m.addConstr(z[i] >= -absz[i], name='Abs2_z{}'.format(i)))
        cons.append(m.addConstr(w[i] <= maxw, name='Max_w{}'.format(i)))
    cons.append(m.addConstr(gp.quicksum(x) == 1, name='Money_Constraint'))
    cons.append(m.addConstr(
        gp.quicksum([mu[i] * x[i] for i in range(199)]) + 1.05 * x[199] - gp.quicksum(absz) - gamma * maxw >= R,
        name='RC2_Constraints'))

    ### Solve the model
    m.update()
    m.optimize()
    x = [i.x for i in x]
    R = R.x

    return [R, x]


R, x = budget(0.005)
