import sys, os                                                                                                                                                                                                                                                                               
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path: sys.path.insert(0, HERE)
from util.Util   import *
from util import drawTables  as DT
from util import drawEvo     as DE 

class MyFigure:
    def __init__(self, options, traitData, progress, figName=None):
        self.options, self.data, self.traits, self.progress, self.figName = options, traitData, traitData.members, progress, figName
        self.fs0, self.fs1, self.fs2, self.fs3, self.fs4, self.fs5 = 12,10, 9,7.5,6, 5
        self.lw1,self.lw2,self.lw3 = 1, 0.7,0.5
        self.sz1,self.sz2,self.sz3 = 20,15,10

    def draw(self): 
        self.setup() 
        self.create() 
        self.finish() 
    
    def setup(self): 
        self.fig, self.axes,self.ax_index = matplotlib.pyplot.gcf(), [], 0 
        self.rows, self.cols, self.WD, self.HT = 60, 46, 7.2,8.7
        rsA,rsB,cs = 14,10,7 
        self.axes.append(plt.subplot2grid((self.rows,self.cols), (0,0), rowspan =rsA, colspan =self.cols-1))                                                             
        self.axes.append(plt.subplot2grid((self.rows,self.cols), (rsA+2,0), rowspan =rsB, colspan =self.cols-1))                                                             
        ri = rsA+rsB + 5 
        rs = (self.rows - ri) - 1 
        for ci in [0,23]: 
            self.axes.append(plt.subplot2grid((self.rows,self.cols), (ri,ci), rowspan =rs, colspan =cs))                                                             
            self.axes.append(plt.subplot2grid((self.rows,self.cols), (ri,ci+cs), rowspan =rs, colspan =cs))                                                             
            self.axes.append(plt.subplot2grid((self.rows,self.cols), (ri,ci+cs+cs), rowspan =rs, colspan =cs))                                                             
        self.fig.set_size_inches(self.WD, self.HT) 

    def create(self): 
        bt = DT.BicTable(self.options)
        bt.generate_bic_models(self.traits) 
        bt.draw_bic_table(self.axes[0], self.axes[1]) 
        self.evo = DE.EvoPlot(self) 
        self.evo.classify() 
        self.evo.plot_scores(self.axes[2:5], PRINTPV=True, INIT=True) 
        self.evo.classify(ALT=True) 
        self.evo.plot_scores(self.axes[5::], PRINTPV=True, INIT=False) 

    def finish(self,fs=22): 
        for i,x in zip([0,2,5],['$a$','$b$','$c$']): 
            if i == 0: self.axes[i].text(0,100,x, fontsize=fs) 
            else:      self.axes[i].set_title(x, x= 0, y = 0.98, fontsize=fs) 
        plt.subplots_adjust(left=0.03, bottom=0.03, right=0.995, top=0.97,wspace=0.05, hspace=0.07) 
        if self.figName is not None: figPath = self.options.out+self.figName+'.pdf' 
        else:                        figPath = self.options.out+'Sup10.pdf' 
        plt.savefig(figPath, dpi=self.options.dpi) 
        plt.clf() 
        self.progress.save('(Figure Saved: '+figPath+')')
        return
