from box import box
from ball import ball
from budget import budget
import matplotlib.pyplot as plt
import numpy as np

### Simulation Parameters
epsilon = 0.005
itera = 1000000

### Compute the expected,lowest and uppest returns of all assets; Plot the figure
mu = np.array([1.05 + 0.3 * ((200 - i - 1) / 199) for i in range(199)])
sigma = np.array([0.05 + 0.6 * ((200 - i) / 199) for i in range(199)])
plt.subplot(2, 1, 1)
plt.plot(mu, color='grey', linestyle='--', label='expected return')
plt.plot(mu - sigma, color='b', linestyle='--', label='lowest return')
plt.plot(mu + sigma, color='b', linestyle='--', label='uppest return')
plt.grid()
plt.xlabel('The Assets')
plt.ylabel('The return(%)')
plt.legend()

#### Solve the three models
R1, x1 = box()
R2, x2 = ball(epsilon)
R3, x3 = budget(epsilon)
# x1=[i*100 for i in x1]
x2 = [i * 100 for i in x2]
x3 = [i * 100 for i in x3]
# plt.plot(x1,label='Box')
plt.subplot(2, 1, 2)
plt.plot(x2, label='Ball')
plt.plot(x3, label='Budget')
plt.grid()
plt.xlabel('The Assets')
plt.ylabel('Investment Ratios(%)')
plt.legend()

### Simulation
P1, P2, P3 = [], [], []
for i in range(itera):
    zeta = np.random.random(199) * 2 - 1
    P1.append(1 if (np.dot(mu + zeta * sigma, x1[:199]) + 1.05 * x1[-1] >= R1) else 0)
    P2.append(1 if (np.dot(mu + zeta * sigma, x2[:199]) + 1.05 * x2[-1] >= R2) else 0)
    P3.append(1 if (np.dot(mu + zeta * sigma, x3[:199]) + 1.05 * x3[-1] >= R3) else 0)
P1 = np.array(P1)
P2 = np.array(P2)
P3 = np.array(P3)
print("\n Box\t: {}\n Ball\t: {}\n Budget\t: {}".format(P1.mean(), P2.mean(), P3.mean()))
