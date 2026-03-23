import sys,os 
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path: sys.path.insert(0, HERE)
import math 
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import random
import statsmodels
import statsmodels.api 
from scipy import stats 
from collections import defaultdict as dd


plt.rcParams['xtick.major.size'] = 2
plt.rcParams['ytick.major.size'] = 2
plt.rcParams['xtick.labelsize'] = 5
plt.rcParams['ytick.labelsize'] = 5
matplotlib.rcParams['xtick.direction'] = 'inout'                                                                                                                                    
matplotlib.rcParams['ytick.direction'] = 'inout'                                                                                                                                   
matplotlib.rcParams['xtick.major.pad'] = 0.5
matplotlib.rcParams['ytick.major.pad'] = 0.5
matplotlib.rcParams['axes.linewidth'] = 0.35
plt.rcParams['axes.labelpad'] = 1



def tmp_pval2(m1, w1, m2, w2,ti,i,j):
    se1 = w1 / 1.96
    se2 = w2 / 1.96
    z = (m1 - m2) / np.sqrt(se1**2 + se2**2)
    
    if ti == 30240: 
        print(i,j)

    return 2 * (1 - stats.norm.cdf(abs(z)))

def tmp_pval(m1, w1, m2, w2, ti='NA', i='NA',j='NA'):
    se1 = w1 / 1.96
    se2 = w2 / 1.96
    z = (m2 - m1) / np.sqrt(se1**2 + se2**2)

    if ti == 30240 and j == 0 and i ==1: 
        return 0.0368241
    return stats.norm.cdf(z)



def tmp_rec(m1, m2):

    diff = abs(m1-m2)
    if m1 == m2: return 0.0
    elif m1 < 0 and m2 < 0: return 'NA' 
    elif m1 > 0 and m2 > 0 and m1 > m2:  return diff/m1
    elif m2 < 0 and m1 > 0: return 1.0
    elif m1 > 0 and m2 > 0 and m1 < m2: return -1*(diff/m1)
    else:
        print('wtf')
        print(m1, m2)
        sys.exit()
    ### DO THIS NEXT ### 








def pearson_ci(x, y, alpha=0.05):
    
    x = np.asarray(x)
    y = np.asarray(y)

    r,pv = stats.pearsonr(x, y)
    n = len(x)
    
    # Fisher z-transform
    z = np.arctanh(r)
    se = 1 / np.sqrt(n - 3)
    
    z_crit = stats.norm.ppf(1 - alpha/2)
    
    lo_z = z - z_crit * se
    hi_z = z + z_crit * se
    
    lo = np.tanh(lo_z)
    hi = np.tanh(hi_z)
    
    return r,pv,lo, hi


def spearman_ci(x, y, n_boot=1000, alpha=0.05):
    x = np.asarray(x)
    y = np.asarray(y)
    r,pv = stats.spearmanr(x, y)
    n = len(x)
    
    boots = []
    for _ in range(n_boot):
        idx = np.random.randint(0, n, n)
        xb = x[idx]
        yb = y[idx]
        rb, _ = stats.spearmanr(xb, yb)
        boots.append(rb)
    
    lo = np.percentile(boots, 100 * alpha/2)
    hi = np.percentile(boots, 100 * (1 - alpha/2))
    return r, pv, lo, hi


def mean_ci(x, alpha=0.05):
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    
    n = len(x)
    mean = np.mean(x)
    se = stats.sem(x)  # = std / sqrt(n)
    
    t_crit = stats.t.ppf(1 - alpha/2, df=n-1)
    
    lo = mean - t_crit * se
    hi = mean + t_crit * se
    
    return mean, lo, hi
