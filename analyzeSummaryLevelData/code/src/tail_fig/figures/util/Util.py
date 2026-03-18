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


#matplotlib.rcParams['ytick.direction'] = 'inout'
#matplotlib.rcParams['xtick.labelsize'] = 25
#matplotlib.rcParams['ytick.labelsize'] = 25
##matplotlib.rcParams['figure.figsize'] = [26,14]                                                                                                                                    
#matplotlib.rcParams['xtick.direction'] = 'inout'
#matplotlib.rcParams['ytick.direction'] = 'inout'                                                                                                                                   
#matplotlib.rcParams['ytick.direction'] = 'in'




#from matplotlib.colors import to_rgb, ListedColormap
#from matplotlib.patches import Ellipse
#from matplotlib.patches import Rectangle
                                                      
# fontsize 
# Polygenic
# Primary 
#from figUtil import drawForest as FP
#from figUtil import drawPreds as DP
#from pathlib import Path
#from scipy import stats 
#from util import drawForest as FP 
#from util import drawPreds as DP 
#from util import drawScatter as DS
#from util import drawScatter as SP
#from util import drawScatter as SP 
#from util import drawTables as DT
#from util import drawVarious as DV
#from util import drawVarious as DV 
#from util.Util   import * 
#import matplotlib.cm as cm
#import matplotlib.pyplot as plt
#import statsmodels.api as sm                                                                                                                                                        
#import warnings
#matplotlib.rcParams['axes.linewidth'] = 0.65                                                                                                                                        
#matplotlib.rcParams['axes.linewidth'] = 1.85
#matplotlib.rcParams['axes.linewidth'] = 2                                                                                                                                       
#matplotlib.rcParams['axes.linewidth'] = 2.85  
#matplotlib.rcParams['axes.linewidth'] = 3.85
#matplotlib.rcParams['figure.figsize'] = [26,14]                                                                                                                                    
#matplotlib.rcParams.update(matplotlib.rcParamsDefault)
#matplotlib.rcParams['xtick.direction'] = 'inout'                                                                                                                                    
#matplotlib.rcParams['xtick.direction'] = 'inout'
#matplotlib.rcParams['xtick.direction'] = 'inout'   
#matplotlib.rcParams['xtick.direction'] = 'inout'                                                                                                                                    
#matplotlib.rcParams['xtick.labelsize'] = 22                                                                                                                                       
#matplotlib.rcParams['xtick.labelsize'] = 22                                                                                                                                                                                 
#matplotlib.rcParams['xtick.labelsize'] = 27                                                                                                                                  
#matplotlib.rcParams['xtick.labelsize'] = 28
#matplotlib.rcParams['xtick.labelsize'] = 33                                                                                                                                    
#matplotlib.rcParams['xtick.labelsize'] = 40                                                                                                                                        
#matplotlib.rcParams['xtick.labelsize'] = 52
#matplotlib.rcParams['xtick.labelsize'] = 90                                                                                                                                        
#matplotlib.rcParams['xtick.major.pad'] = 5.5                                                                                                                                        
#matplotlib.rcParams['xtick.major.size'] = 10   
#matplotlib.rcParams['xtick.major.size'] = 12                                                                                                                                   
#matplotlib.rcParams['xtick.major.size'] = 20
#matplotlib.rcParams['xtick.major.size'] = 20                                                                                                                                   
#matplotlib.rcParams['xtick.major.size'] = 50
#matplotlib.rcParams['xtick.major.width'] = 1.5
#matplotlib.rcParams['ytick.direction'] = 'inout'                                                                                                                                   
#matplotlib.rcParams['ytick.direction'] = 'in'                                                                                                                                       
#matplotlib.rcParams['ytick.direction'] = 'inout'
#matplotlib.rcParams['ytick.direction'] = 'inout'   
#matplotlib.rcParams['ytick.direction'] = 'inout'                                                                                                                                   
#matplotlib.rcParams['ytick.direction'] = 'inout'                                                                                                                                       
#matplotlib.rcParams['ytick.labelsize'] = 22   
#matplotlib.rcParams['ytick.labelsize'] = 22                                                                                                                                        
#matplotlib.rcParams['ytick.labelsize'] = 27                                                                                                                                        
#matplotlib.rcParams['ytick.labelsize'] = 28
#matplotlib.rcParams['ytick.labelsize'] = 40                                                                                                                                     
#matplotlib.rcParams['ytick.labelsize'] = 52
#matplotlib.rcParams['ytick.major.pad'] = 5.5                                                                                                                                        
##matplotlib.rcParams['ytick.major.size'] = 10   
#matplotlib.rcParams['ytick.major.size'] = 20
#matplotlib.rcParams['ytick.major.size'] = 50
#np.random.seed(42)  # any fixed number you like
#warnings.filterwarnings("ignore")
