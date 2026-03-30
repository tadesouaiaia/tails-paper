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
from matplotlib.colors import to_rgb, ListedColormap


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






def make_colormap(color1, color2, n=10):
    """
    Create an n-color colormap between any two named or hex colors.
    """
    c1 = np.array(to_rgb(color1))
    c2 = np.array(to_rgb(color2))
    gradient = np.linspace(c1, c2, n+2)
    return gradient.tolist()[-10::]

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


def merge_csv_to_excel_sheets(goals,progress,args): 
    progress.start_step('\n  Merging CSV to Excel Sheets')
    try: 
        import pandas as pd 
        import openpyxl 
    except: 
        sys.stderr.write('\n   Error: Missing Libraries\n    pandas and openpyxl are needed to merge csv to excel (skipping this step)\n') 
        return 

    SK = dd(list)
    for f in os.listdir(args.srcPath): SK[f.split('-')[0]].append(args.srcPath+f) 
    for k,KL in SK.items(): 
        progress.dot(3)  
        #if k not in goals: continue 
        KL.sort() 
        try: 
            with pd.ExcelWriter(args.xlsPath+k+'.xlsx') as writer: 
                for st in KL: 
                    cand = st.split('-')[-1].split('.csv')[0] 
                    try: pd.read_csv(st).to_excel(writer, sheet_name=cand, index=False)
                    except: continue 
        except IndexError: continue 
    csv_tables = [f for f in os.listdir(args.out) if f.split('.')[-1] == 'csv'] 
    progress.dot(3)  
    if len(csv_tables) > 0:
        try: 
            CK = {c.split('-')[-1].split('.')[0]: args.out+c for c in csv_tables} 
            with pd.ExcelWriter(args.xlsPath+'auxillaryData.xlsx') as writer: 
                for k in ['traitSummaries', 'commonTails','rareTails','rareSNPs', 'glossary']:  
                    if k in CK: 
                        pd.read_csv(CK[k]).to_excel(writer, sheet_name = k, index=False) 

        except IndexError: pass  
    progress.show('...Complete (xlsx sheets saved: '+args.xlsPath+')') 
