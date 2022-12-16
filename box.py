import gurobipy as gp
from gurobipy import GRB
import numpy as np


def box():
    ### Compute the parameters
    mu = np.array([1.05 + 0.3 * ((200 - i - 1) / 199) for i in range(199)])
    sigma = np.array([0.05 + 0.6 * ((200 - i) / 199) for i in range(199)])

    ### Generate a model
    m = gp.Model('Box')
    m.setAttr('ModelSense', GRB.MAXIMIZE)
    m.Params.OutputFlag = 0

    ### Add variables
    x = []
    for i in range(200):
        x.append(m.addVar(lb=0, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS, name="x{}".format(i)))
    R = m.addVar(lb=0, ub=GRB.INFINITY, obj=1, vtype=GRB.CONTINUOUS, name='R')

    ### Add Constraints
    cons = []
    cons.append(m.addConstr(gp.quicksum([(mu[i] - sigma[i]) * x[i] for i in range(199)]) + 1.05 * x[199] >= R,
                            name='RC1_Constraint'))
    cons.append(m.addConstr(gp.quicksum(x[:200]) == 1, name='RC2_Constraint'))

    ### Solve the model
    m.update()
    m.optimize()
    R = R.X
    x = [i.X for i in x]

    return [R, x]


R, x = box()
