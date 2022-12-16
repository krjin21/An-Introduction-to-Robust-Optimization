import gurobipy as gp
from gurobipy import GRB
import numpy as np
import math


def ball(e):
    ### Compute the parameters
    Omega = math.sqrt(2 * math.log(1 / e, math.e))
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
    sqrtw = m.addVar(0, GRB.INFINITY, vtype=GRB.CONTINUOUS, name='Sqrtw')
    for i in range(199):
        x.append(m.addVar(lb=0, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS, name='x{}'.format(i)))
        z.append(m.addVar(vtype=GRB.CONTINUOUS, name='z{}'.format(i)))
        absz.append(m.addVar(vtype=GRB.CONTINUOUS, name='absz{}'.format(i)))
        w.append(m.addVar(vtype=GRB.CONTINUOUS, name='w{}'.format(i)))
    x.append(m.addVar(lb=0, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS, name='x199'))

    ### Add Constraints
    cons = []
    cons.append(m.addConstr(gp.quicksum([i * i for i in w]) <= sqrtw * sqrtw, name='Sqrt_W'))
    for i in range(199):
        cons.append(m.addConstr(z[i] <= absz[i], name='Abs1_z{}'.format(i)))
        cons.append(m.addConstr(z[i] >= -absz[i], name='Abs2_z{}'.format(i)))
        cons.append(m.addConstr(z[i] + w[i] == sigma[i] * x[i], name='RC_Constraints{}'.format(i)))
    cons.append(m.addConstr(gp.quicksum(x) == 1, name='Money_Constraint'))
    cons.append(m.addConstr(
        gp.quicksum([mu[i] * x[i] for i in range(199)]) + 1.05 * x[199] - gp.quicksum(absz) - Omega * sqrtw >= R,
        name='RC2_Constraints'))

    ### Solve the model
    m.update()
    m.optimize()
    x = [i.x for i in x]
    R = R.x

    return [R, x]


R, x = ball(0.005)
