import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path: sys.path.insert(0, HERE)
from util.Util   import * 
from util import drawPreds as DP 
from util import drawVarious as DV 



# Extended Data Figure: Odds Ratios For Pseudo 1% Prevalent Tail Traits #  




class MyFigure:
    def __init__(self, options, traits, progress, figName=None): 
        self.options, self.traits, self.data, self.progress, self.figName = options, traits.members, traits, progress, figName
        self.rep_color_key = {'rep': 'xkcd:purpley', 'poc': 'xkcd:barney', 'aou': 'xkcd:leaf green'} 
        self.fs0, self.fs1, self.fs2, self.fs3, self.fs4 = 20, 15, 10, 8, 5 
    
    def draw(self): 
        self.setup() 
        self.create() 
        self.finish() 

    def setup(self): 
        self.ax_index = 0 
        self.fig, self.axes = matplotlib.pyplot.gcf(), [] 
        self.rows, self.cols, self.WD, self.HT = 23, 35, 7.1, 6.5

    def create(self): 
        pred_pairs, idx, cs1 = [], 0, 8 
        for rl in [0,11]:
            for cl in [0,19]: 
                try: 
                    T = self.traits[self.options.indexTraits[idx]] 
                    idx += 1 
                    if 'pred' in T.pts: 
                        for i in [0,5]: 
                            for j in [0,cs1]: 
                                if i == 0: self.axes.append(plt.subplot2grid((self.rows,self.cols), (i+rl,j+cl), rowspan = 5, colspan =cs1))
                                else:      self.axes.append(plt.subplot2grid((self.rows,self.cols), (i+rl,j+cl), rowspan = 3, colspan =cs1))
                        pred_pairs.append([T, self.axes[-4::]]) 
                except: pass 
        self.fig.set_size_inches(self.WD, self.HT) 
        for T,axes in pred_pairs:
            dp = DP.PredPlot(self.options) 
            dp.draw_odds(T, axes, QT=True) 
        try: 
            ax = self.axes[len(self.axes)-5] 
            axl = DV.AxLims(ax) 
            x1, x2, y1 = axl.xMin + 1.25*axl.xStep, axl.xMin + axl.xStep*12, axl.yMin - 8.5*axl.yStep 
            axl.ax.plot([x1,x1+15],[y1,y1], clip_on=False,color='blue',lw=1) 
            axl.ax.scatter(x1,y1, color='blue', s=52,clip_on=False) 
            axl.ax.scatter(x1+15,y1, color='blue', s=52,clip_on=False) 
            axl.ax.text(x1+19,y1,'Observed Performance',va='center',fontsize=self.fs3) 
            axl.ax.plot([x2,x2+14],[y1,y1], clip_on=False,color='darkorange',linestyle='--',lw=1) 
            axl.ax.text(x2+15,y1,'Expected Performance',va='center',fontsize=self.fs3) 
            y1,y2 = y1-0.45,y1+0.45
            DV.draw_square(axl.ax, x1-axl.xHop*5, x2+axl.xStep*10, y1, y1 + axl.yStep*4) 
        except: pass 
        return 

    def finish(self): 
        plt.subplots_adjust(left=0.04, bottom=-0.022, right=0.99, top=0.955,wspace=0.05, hspace=0.05) 
        if self.figName is not None: figPath = self.options.out+self.figName+'.pdf' 
        else:                        figPath = self.options.out+'Sup2.pdf' 
        plt.savefig(figPath, dpi=self.options.dpi) 
        plt.clf() 
        self.progress.save('(Figure Saved: '+figPath+')')
        return
