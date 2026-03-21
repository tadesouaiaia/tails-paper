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
