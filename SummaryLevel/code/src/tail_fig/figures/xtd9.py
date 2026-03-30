import sys, os                                                                                                                                                                                                                                                                               
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path: sys.path.insert(0, HERE)
from util.Util   import *
from util import drawVarious as DV
from util import drawSims    as DI 

class MyFigure:
    def __init__(self, options, traitData, progress, figName=None):
        self.options, self.data, self.traits, self.figName = options, traitData, traitData.members, figName
        self.progress = progress.update(self) 
        self.fs0, self.fs1, self.fs2, self.fs3, self.fs4, self.fs5 = 12,10, 9,7.5,6, 5       
        self.lw1,self.lw2,self.lw3 = 1, 0.7,0.5
        self.sz1,self.sz2,self.sz3 = 20,15,10

    def draw(self): 
        self.read_slim_data() 
        self.setup() 
        self.lib.plot_dists(self.axes) 
        self.finish() 

    def read_slim_data(self):  
        self.SIM = False 
        if self.options.simPath == None: 
            self.progress.error('Slim Simulation Results Not Provided (--simPath [PathToSimResult])\n                 Figure Cannot Create Simulation Panels')  
            return 
        self.lib  =  DI.SlimLib(self, XTD=True)
        self.SIM  =  self.lib.SLIM 
        if not self.SIM: self.progress.error('Invalid Slim Results (--simPath requires slim.dist.txt)\n                 Figure Cannot Create Simulation Panels')  
        return         

    def setup(self):
        self.fig, self.axes = matplotlib.pyplot.gcf(), [] 
        self.rows, self.cols, self.WD, self.HT = 17, 2, 7.1,9
        for i in [0,4,9,13]: 
            for j in range(self.cols): 
                self.axes.append(plt.subplot2grid((self.rows,self.cols), (i,j), rowspan =4, colspan =1))                                                             
        self.fig.set_size_inches(self.WD, self.HT) 
        self.ax_index, self.xLoc, self.fq1, self.fq2 = 0, 1, 24, 22 
    
    def finish(self,fs=22):
        lms = DV.AxLims(self.axes[0]) 
        for i,x in enumerate(['a','b','c','d','e','f','g','h']): self.axes[i].set_title('$'+x+'$', x= -0.07, y=0.935, fontsize=13) 
        plt.subplots_adjust(left=0.05, bottom=0.08, right=0.99, top=0.97,wspace=0.3, hspace=2) 
        self.progress.save() 
        return 
