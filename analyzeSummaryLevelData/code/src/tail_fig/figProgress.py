#!/usr/bin/python3

#sys.path.append("/home/tade/Current/Tails/analysis/code/python_run3")
#sys.path.append("/home/tade/Current/Tails/analysis/round5/eurNoCancer/QC_NEW/code") 
#from src.ExtremeLoad import traitLoad
#import src.ExtremePlotting as EP
#import src.ExtremeForests as FP

#import functools
#from pathlib import Path
#from collections import defaultdict as dd
#from collections import deque
import sys 

# np

#HERE = Path(__file__).resolve().parent
#SRC_DIR = HERE / "src"
#master_list = SRC_DIR / "ukb_master.txt"
#master_list = SRC_DIR / "MASTER.list" 







#import matplotlib 
#import matplotlib.pyplot as plt
#import sys
#import numpy as np
#import scipy.stats as stats
#import statsmodels.api as sm
#import random
#import math
#import numpy as np
#import pandas as pd
#from scipy.stats import norm
#from pathlib import Path
#from collections import defaultdict as dd 







#import matplotlib
#from mpl_toolkits.axes_grid1.inset_locator import inset_axes      
#matplotlib.rcParams['xtick.labelsize'] = 24                                                                                                                                                                                 
#matplotlib.rcParams['ytick.labelsize'] = 24                                                                                                                                                                                 
#matplotlib.rcParams['xtick.major.size'] = 18                                                                                                                                                                               
#matplotlib.rcParams['ytick.major.size'] = 18                                                                                                                                                                               
#matplotlib.rcParams['axes.linewidth'] = 1.85  


#plt.rc('text', usetex=True)
#matplotlib.use("Cairo")
#import warnings
#warnings.filterwarnings("ignore")




#############################################################################################
##################################  PROGRESS STREAM  ########################################
#############################################################################################


class Progress:
    def __init__(self, args, command_line, MODE='Generate Figures'): 
        self.args = args
        self.out_file = args.out+'runLog.txt' 
        self.out1 = open(self.out_file, 'w')  
        

        if args.silent: self.ACTIVE = False 
        else:           self.ACTIVE = True 
        self.out2  = sys.stderr 
        self.space = '' 
        self.show('\nUKB GEN:  '+command_line+'\n')
        self.show('      Mode:  '+MODE+'\n') 
        
        self.loc = None
        self.spl = '  ' 
        self.INIT=True

    def show(self, msg, space=''):
        if space == 'NA': myspace = '' 
        else:             myspace = self.space
        
        self.out1.write(myspace+msg) 
        if self.ACTIVE: 
            self.out2.write(myspace+msg)
            self.out2.flush() 



    def step(self, dots): self.show(''.join(['.' for x in range(dots)])) 
    
    def start_step(self, msg, STEP=1): 
        if self.ACTIVE: 
            if self.INIT: 
                if STEP<0: self.show('\n'+self.spl+msg)  
                elif STEP==0: self.show('\n'+self.spl+msg+'...')  
                else: self.show(self.spl+msg+'...')  
                self.INIT = False
            else:
                #self.complete_step() 
                if STEP<0: self.show(self.spl+msg)  
                else: self.show(self.spl+msg+'...')  

    def complete_step(self, msg=None, NEW=False):
        if NEW: self.show('\n') 
        if msg is not None: self.show('...Complete ('+msg+')\n') 
        else: self.show('...Complete\n') 
        self.INIT = True 

    def complete_all(self, msg=None, NEW=False): 
        if NEW: self.show('\n') 
        if msg is not None: self.show(self.spl+'Pipeline Complete ('+msg+')\n') 
        else: self.show(self.spl+'Pipeline Complete\n') 
        self.INIT = True 




    def complete_group(self): self.show('...Complete\n\n') 

    def complete_analysis(self): 
        if self.loc is not None: self.show('...Finished\n','NA') 
        self.show('\nQC Complete\n','NA') 

    def finish(self): 
        self.show('\n'+self.spl+'Finished\n\n') 


    def report_result(self, msg=None): 
        self.show('\n'+self.spl+'   Reporting Result: '+msg) 
        self.INIT = True 

    def error(self, msg = 'FAIL', ws=0):
        wj = ' '.join(['' for x in range(ws)])
        self.out1.write('\n\n'+wj+'FigureError: '+msg+'\n')
        sys.stderr.write('\n\n'+wj+'FigureError: '+msg+'\n')
        sys.exit()
    
    def warn(self, msg = 'FAIL', ws=0):
        self.out1.write('\n\n'+self.spl+'FigureWarning: '+msg+'\n')
        sys.stderr.write('\n\n'+self.spl+'FigureWarning: '+msg+'\n')

    
    def save(self, msg, ws = 0): 
        
        if self.INIT: self.show('\n'+self.spl+'  Complete '+msg+'\n')  
        else:         self.show('....Complete '+msg+'\n')  
        self.INIT = False 





#############################################################################################
##################################     TRAIT CLASS      ####################################
#############################################################################################





