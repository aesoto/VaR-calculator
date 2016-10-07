# VaR studentT.py
# By: Andres Soto
# This script calculate VaR and CVAR
# Paths simulated throught student T Distribution

import numpy as np
import numpy.random as npr
import matplotlib.pyplot as plt
import math
from scipy import stats

nu = 5                # degrees of freedom for distribution

# First parameterize 
S0 = 1000
r = 0.0               # setting to zero for perhaps use later
sigma = 0.02
T = 10/252.           # assuming to days of a trading year
I = 10000             # number of simulations
delta = .04

# The following runs the simulation
# ST then exists as a numpy array
ST = S0 * np.exp((r - 0.5 * sigma ** 2) * T + sigma * np.sqrt(T) * npr.standard_t(nu,I))

# Calculate payoff amount:
L = 548.35
K = 2208.0
P0 = 1360.75
gamma = 0.3304
NI = (S0*delta - K*.01)*T

PT = np.zeros(shape=(I))

for i in range(I):
    PT[i] = (K- min(np.array(ST[i]),L)) * (L/(max(np.array(ST[i]),L)))**gamma



# Create a second array consisting of sorted values of the difference of ST and S0
R_gbm = np.sort((ST+PT) - (S0+P0) + NI)

# displays histogram of shortfalls
plt.hist(R_gbm, bins=50)
plt.xlabel('absolute return')
plt.ylabel('frequency')
plt.grid(True)
plt.show()

# define confidence interval thresholds
percs = []
for i in np.arange(.1, 5.01, 0.1):
    percs.append(i)

# sorts value at risk by percentiles
var = stats.scoreatpercentile(R_gbm, percs)
print '%16s %16s' % ('Confidence Level', 'Value-at-Risk')
print 33 * '-'
for pair in zip(percs, var):
    print '%16.2f %16.3f' % (100 - pair[0], -pair[1])
    
# report VaR at the 95% confidence interval which is the last value in var    
print         
print('Value-at-Risk at the 95% confidence interval is: {}'.format(round(-var[-1],2)))
print

# Calculate CVAR by summing all values and dividing by number of values; embeddedin the print statement below
print('And the Conditional Value-at-Risk at the 95% confidence interval is: {}'.format(round(-sum(var)/len(var),2)))
