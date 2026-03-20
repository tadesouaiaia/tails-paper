#!/usr/bin/python3

import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path: sys.path.insert(0, HERE)

from util.Util   import * 
from util import drawTables as DT
from util import drawVarious as DV 


class MyFigure:
    def __init__(self, options, traits, progress, figName=None): 
        self.options, self.traits, self.data, self.progress, self.figName = options, traits.members, traits, progress, figName
        self.C1 = 'xkcd:very light blue' 
        self.C1 = 'xkcd:very light pink' 
        self.C2 = 'xkcd:off white' 
        self.E1, self.E2 = 'darkslategray','gray' 


    
    def draw(self): 
        
        group1, group2 = [], [] 
        for ti,T in self.traits.items(): 
            if 'sanjak' in T.vals.keys(): 
                if T.vals['sanjak'].key['SEX-DIFF'] == 'True': group2.append(T) 
                else:                                          group1.append(T) 
        self.setup() 
        self.create(group1, group2) 
        self.finish() 


    def setup(self): 
        self.i1, self.i2 = 'whitesmoke','gainsboro'
        self.fig, self.axes = matplotlib.pyplot.gcf(), []
        self.WD, self.HT, self.rows, self.cols = 17, 16, 1, 1
        self.WD, self.HT = 7.2, 6

        self.axes.append(plt.subplot2grid((self.rows,self.cols),(0,0), rowspan =1, colspan =1))                                                                           
        self.fig.set_size_inches(self.WD, self.HT)
        self.ax_index, self.xLoc = 0, 1
        return
 






    def create(self, regular_traits, sex_diffs): 
        dt = DT.CompTable(self.axes[0], self.options).initialize(c1=self.i1,c2=self.i2)
        dt.add_data(regular_traits, sex_diffs) 
        

        ax = self.axes[0]

        ax.axis('off') 

        return self















    def finish(self):
        plt.subplots_adjust(left=0.015, bottom=-0.1, right=0.985, top=0.98,wspace=0.0,hspace=0.03) 
        c = 'xkcd:cool grey' 
        
        if self.figName is not None: figPath = self.options.out+self.figName+'.pdf' 
        else:                        figPath = self.options.out+'Sup9.pdf' 
        plt.savefig(figPath, dpi=self.options.dpi) 
        plt.clf() 
        self.progress.save('(Figure Saved: '+figPath+')')
        return




        #if self.figName is not None: plt.savefig(self.options.out+self.figName+'.pdf',dpi=400)        
        #else: plt.savefig(self.options.out+'table3.pdf',dpi=400)     
        #plt.clf() 










   



















