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


