#!/usr/bin/python3

import sys, os                                                                                                                                                                                                                                                                               
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path: sys.path.insert(0, HERE)

from util.Util   import *
#from util import drawScatter as DS
from util import drawVarious as DV
from util import drawLabels  as DL
#from util import drawTables  as DT
from util import drawSims    as DI 
#from util import drawEvo     as DE 







class MyFigure:
    def __init__(self, options, traitData, progress, figName=None):
        self.options, self.data, self.traits, self.progress, self.figName = options, traitData, traitData.members, progress, figName
        self.fs0, self.fs1, self.fs2, self.fs3, self.fs4, self.fs5 = 12,10, 9,7.5,6, 5       
        self.lw1,self.lw2,self.lw3 = 1, 0.7,0.5
        self.sz1,self.sz2,self.sz3 = 20,15,10

    def draw(self): 
        self.read_slim_data() 
        self.setup() 
        self.create() 
        self.finish() 

    def read_slim_data(self):  
        self.SIM = False 
        if self.options.simPath == None: 
            self.progress.error('Slim Simulation Results Not Provided (--simPath [PathToSimResult])\n                 Figure Cannot Create Simulation Panels')  
            return 
        self.lib  =  DI.SlimLib(self.options, XTD=True)
        self.SIM  =  self.lib.SLIM 
        if not self.SIM: self.progress.error('Invalid Slim Results (--simPath requires slim.dist.txt)\n                 Figure Cannot Create Simulation Panels')  
        return         




    def setup(self):
        self.fig, self.axes = matplotlib.pyplot.gcf(), [] 
        r1,r2,r3 = 20, 12, 41 
        c1,c2,c3 = 39, 10, 19 
        self.rows, self.cols, self.WD, self.HT = 9, 2, 7.1,9
        
        for i in [0,2,5,7]: 
            for j in range(self.cols): 
                self.axes.append(plt.subplot2grid((self.rows,self.cols), (i,j), rowspan =2, colspan =1))                                                             



        self.fig.set_size_inches(self.WD, self.HT) 
        self.ax_index, self.xLoc, self.fq1, self.fq2 = 0, 1, 24, 22 
    
    def create(self):
        
        self.lib.plot_pops(self.axes) 

        
        return 


   







    def finish(self,fs=22):
        lms = DV.AxLims(self.axes[0]) 
        
        for i,x in enumerate(['a','b','c','d','e','f','g','h']): 
            self.axes[i].set_title('$'+x+'$', x= -0.07, y=0.935, fontsize=13) 

        plt.subplots_adjust(left=0.06, bottom=0.03, right=0.96, top=0.97,wspace=0.3, hspace=0.7) 
        if self.figName is not None: figPath = self.options.out+self.figName+'.pdf' 
        else:                        figPath = self.options.out+'Xtd9.pdf' 
        plt.savefig(figPath, dpi=self.options.dpi) 
        plt.clf() 
        self.progress.save('(Figure Saved: '+figPath+')')
        return            


