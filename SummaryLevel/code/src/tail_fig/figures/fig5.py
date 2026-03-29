import sys, os                                                                                                                                                                                                                                                                               
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path: sys.path.insert(0, HERE)
from util.Util   import *
from util import drawVarious as DV
from util import drawLabels  as DL
from util import drawSims    as DI 
from util import drawEvo     as DE 


class MyFigure:
    def __init__(self, options, traitData, progress, figName=None):
        self.options, self.data, self.traits, self.figName = options, traitData, traitData.members, figName
        self.progress = progress.update(self) 
        self.fs0,self.fs1,self.fs2,self.fs3,self.fs4,self.fs5,self.sz1,self.lw1,self.lw2,self.lw3 = 12,10,9,7.5,6,5,20,1,0.7,0.5    

    def draw(self): 
        self.read_slim_data() 
        self.setup() 
        self.create() 
        self.finish() 

    def read_slim_data(self):  
        self.SIM = False 
        if self.options.simPath == None: 
            self.progress.warn('Slim Simulation Results Not Provided (--simPath [PathToSimResult])\n                 Figure Will Omit Slim Simulation Panels')  
            return 
        self.lib  =  DI.SlimLib(self)
        self.SIM  =  self.lib.SLIM 
        if not self.SIM: self.progress.warn('Invalid Slim Results (--simPath requires valid enrich/delta.csvs)\n                 Figure Will Omit Slim Simulation Panels')  
        return         

    def setup(self):
        self.fig, self.axes = matplotlib.pyplot.gcf(), [] 
        r1,r2,r3 = 20, 12, 41 
        c1,c2,c3 = 39, 10, 19 
        if self.SIM: 
            self.rows, self.cols, self.WD, self.HT = 100, 100, 7.1,6.0
            self.axes.append(plt.subplot2grid((self.rows,self.cols), (0,1), rowspan =r1, colspan =c1))                                                             
            self.axes.append(plt.subplot2grid((self.rows,self.cols), (0,c1+14), rowspan =r1, colspan =c1+3)) 
            ri, ri2 = r1 + 16, r1 + 11 
        else: 
            self.rows, self.cols, self.WD, self.HT = 80, 100, 7.1,5.0
            ri,ri2 = 3, 0 
        for j in range(0,c2*4,c2):                                                                                                                                               
            for i in range(ri,ri+(4*r2),r2):                                                                                                                                   
                self.axes.append(plt.subplot2grid((self.rows,self.cols), (i,j), rowspan = r2, colspan =c2))                                                                   
        ci = c2*4+4
        self.axes.append(plt.subplot2grid((self.rows,self.cols), (ri2,ci), rowspan =r3, colspan =c3))                                                             
        self.axes.append(plt.subplot2grid((self.rows,self.cols), (ri2,ci+c3), rowspan =r3, colspan =c3))                                                             
        self.axes.append(plt.subplot2grid((self.rows,self.cols), (ri2,ci+c3+c3), rowspan =r3, colspan =c3))                                                             
        self.axes.append(plt.subplot2grid((self.rows,self.cols), (ri2+r3+9,ci+14), rowspan =12, colspan =37))                                                             
        self.fig.set_size_inches(self.WD, self.HT) 
        self.ax_index, self.xLoc, self.fq1, self.fq2 = 0, 1, 24, 22 
    
    def create(self):
        if self.SIM: 
            self.progress.set_panel('a') 
            self.lib.plot_sim_curves(self.axes[0]) 
            self.progress.set_panel('b') 
            self.lib.plot_sim_boxes(self.axes[1]) 
            self.ax_index = 2

        self.progress.set_panel('c') 
        self.evo = DE.EvoPlot(self) 
        self.evo.classify() 
        self.evo.plot_boxes() 
        DL.BoxKeys(self.axes[self.ax_index+3]).add_group_key('bottom-4',self.data) 
        self.ax_index += 16
        
        self.progress.set_panel('d') 
        self.evo.plot_scores(self.axes[self.ax_index:self.ax_index+3]) 
        self.progress.set_panel('e') 
        self.evo.plot_health_tails(self.axes[-1]) 
        return 

    def finish(self,fs=22):
        lms = DV.AxLims(self.axes[2]) 
        if self.SIM: idx, labs = [2, 0, 1, 18, 21], ['c','a','b','d','e'] 
        else:        idx, labs = [0,16,19], ['a','b','c']  
        AX = [self.axes[i] for i in idx] 
        lms = DV.AxLims(AX[0]) 
        AX[0].text(lms.xMin - lms.xStep*3.5,lms.yMax + lms.yStep*6, labs[0], fontsize = fs+3) 
        for i,ax,x in zip(idx[1::], AX[1::], labs[1::]): 
            if i == 0:   ax.set_title('$'+x+'$', x= -0.08, y = 0.88, fontsize=fs) 
            elif i == 1:   ax.set_title('$'+x+'$', x= -0.16, y = 0.86, fontsize=fs) 
            elif i in [16,18]:   ax.set_title('$'+x+'$', x= 0.1, y = 1.05, fontsize=fs) 
            elif i in [19,21]:   ax.set_title('$'+x+'$', x= -0.33, y = 0.95, fontsize=fs) 
        if self.SIM: plt.subplots_adjust(left=0.04, bottom=-0.04, right=1.01, top=0.97,wspace=0.05, hspace=0.07) 
        else:        plt.subplots_adjust(left=0.05, bottom=-0.15, right=0.99, top=0.90,wspace=0.05, hspace=0.07) 
        self.progress.save() 
        return 
