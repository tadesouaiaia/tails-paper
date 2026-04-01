import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path: sys.path.insert(0, HERE)
from util.Util   import * 
from util import drawScatter as SP 
from util import drawTables as DT
from util import drawVarious as DV 

# Extended Data Figure: All Tail Plots # 

class MyFigure:
    def __init__(self, options, traits, progress, figName='allTails'): 
        self.options, self.traits, self.data, self.figName = options, traits.members, traits, figName
        self.progress = progress.update(self) 

    def draw(self, step=75): 
        n, trait_ids = 2, [x[1] for x in sorted([[T.name.mini, T.ti] for T in self.traits.values()])] 
        if len(trait_ids) <= step: self.fignames = [self.figName+'.pdf'] 
        else:                      self.fignames = [self.figName+'-1.pdf'] 
        
        if len(trait_ids) <= step: self.fig_prefixes = [self.options.out+self.figName] 
        else:                      self.fig_prefixes = [self.options.out+self.figName+'-1.pdf'] 
        
        
        if self.progress.SAVESRC: 
            self.pop_handle = open(self.progress.src_prefix+'-POPout.csv','w') 
            self.pop_handle.write('%s,%s,%s,%s,%s\n' % ('Panel', 'Trait-ID','PRS-Type','Data','Values'))
            self.sib_handle = open(self.progress.src_prefix+'-STANDout.csv','w') 
            self.sib_handle.write('%s,%s,%s,%s\n' % ('Panel', 'Trait-ID','Data','Values'))
            self.evo_handle = open(self.progress.src_prefix+'-UnderSelection.csv','w') 
            self.evo_handle.write('%s,%s,%s,%s\n' % ('Panel', 'Trait-ID','Type','Values'))
        for i in range(0,len(trait_ids),step): 
            self.my_ids, self.my_len = trait_ids[i:i+step], len(trait_ids[i:i+step]) 
            self.setup() 
            self.create() 
            self.finish() 
            self.fignames.append(self.fignames[-1].split('-')[0]+'-'+str(n)+'.pdf') 
            self.fig_prefixes.append(self.options.out+self.fignames[-1].split('-')[0]+'-'+str(n)) 
            n+=1 
        self.progress.save(NULL=True) 
        return 
                                                    

    def setup(self): 
        self.i1, self.i2 = 'whitesmoke','gainsboro'
        self.i1, self.i2 = 'white', 'white' 
        self.fig, self.axes = matplotlib.pyplot.gcf(), []
        ss = 16
        self.subplots = 3*ss                           
        cs1 = 30
        t_rows  = math.ceil(self.my_len/3.0) 
        self.rows, self.cols = (2*t_rows) + 3 , 2+(cs1 + self.subplots)*3
        self.WD = 7.2 
        if self.my_len >= 70: self.HT = 9.7 
        else:                 self.HT = (self.my_len / 8.0) + 1  
        self.rows = (2*math.ceil(self.my_len/3.0)) + 3   
        self.axes.append(plt.subplot2grid((self.rows,self.cols),(0,0), rowspan = 3, colspan =cs1))                                                                           
        self.axes.append(plt.subplot2grid((self.rows,self.cols),(0,cs1), rowspan = 3, colspan =self.subplots))                                                               
        self.axes.append(plt.subplot2grid((self.rows,self.cols),(0,cs1+self.subplots+1), rowspan = 3, colspan =cs1))                                                                           
        self.axes.append(plt.subplot2grid((self.rows,self.cols),(0,cs1+self.subplots+1+cs1), rowspan = 3, colspan =self.subplots))                                                               
        self.axes.append(plt.subplot2grid((self.rows,self.cols),(0,2*cs1+2*self.subplots+2), rowspan = 3, colspan =cs1))                                                                           
        self.axes.append(plt.subplot2grid((self.rows,self.cols),(0,3*cs1+2*self.subplots+2), rowspan = 3, colspan =self.subplots))                                                                           
        for i in range(3,self.rows,2):                                                                                                                                        
            self.axes.append(plt.subplot2grid((self.rows,self.cols),(i,0),rowspan = 2,colspan =cs1))                                                                       
            for z in range(0,self.subplots,ss): self.axes.append(plt.subplot2grid((self.rows,self.cols),(i,cs1+z),rowspan=2,colspan=ss))                                    
            self.axes.append(plt.subplot2grid((self.rows,self.cols),(i,cs1+1+self.subplots),rowspan = 2,colspan =cs1))                                                                       
            for z in range(0,self.subplots,ss): self.axes.append(plt.subplot2grid((self.rows,self.cols),(i,2*cs1+self.subplots+1+z),rowspan=2,colspan=ss))                                    
            self.axes.append(plt.subplot2grid((self.rows,self.cols),(i,2*cs1+2*self.subplots+2),rowspan = 2,colspan =cs1))                                                                       
            for z in range(0,self.subplots,ss): self.axes.append(plt.subplot2grid((self.rows,self.cols),(i,3*cs1+2*self.subplots+2+z),rowspan=2,colspan=ss))                                    
        self.fig.set_size_inches(self.WD,self.HT)                                                                                                                                  
        self.ax_index,self.xLoc,self.fq1,self.fq2 = 0, 1, 24, 22                


    def finish(self):
        plt.subplots_adjust(left=0.015, bottom=0.01, right=0.985, top=0.98,wspace=0.0,hspace=0.03) 
        for ff in self.options.figFormats: plt.savefig(self.fig_prefixes[-1]+'.'+ff, dpi=500) 
        plt.clf() 



    def create(self): 
        dt = DT.SummaryTable(self).initalize(self.axes[0],self.axes[1],c1=self.i1,c2=self.i2) 
        dt = DT.SummaryTable(self).initalize(self.axes[2],self.axes[3],c1=self.i1,c2=self.i2) 
        dt = DT.SummaryTable(self).initalize(self.axes[4],self.axes[5],c1=self.i1,c2=self.i2) 
        self.ax_index += 6 
        count = 0 
        self.clr = 'white' 
        for ti in self.my_ids: 
            T = self.traits[ti] 
            dt.add_trait(self.axes[self.ax_index], T, self.clr) 
            for j in [1,2,3]: self.axes[self.ax_index+j].set_facecolor(self.clr) 
            self.draw_subplots(T) 
            self.ax_index += 4 
            count += 1
            continue 
        for ax in self.axes[self.ax_index::]: ax.axis('off') 
        return self




    def draw_subplots(self, T, mp = 9.08, lw = 4):  
        subs = [] 
        axes = self.axes[self.ax_index+1::] 
        if self.progress.SAVESRC: 
            

            self.progress.out3, self.progress.panel = self.pop_handle, 'POPout'
            subs.append(SP.POPplot(axes[0], self, T.ti, lw2=0.5, sz1=4, sz2=3, sz3=4.0, alp=0.3).draw_common_popout(MINI=True)) 
            self.progress.out3, self.progress.panel = self.sib_handle, 'STANDout'
            subs.append(SP.SibPlot(axes[1], self, T.ti, sz1=7, sz2=4, sz3=3, alp=0.3, fs2=5).draw_mini_sib_pair()) 
            self.progress.out3, self.progress.panel = self.evo_handle, 'Selection'
            subs.append(SP.EvoScatter(axes[2], self, T.ti).mini_box(fs=5,sz=6,lw=0.25)) 
        else: 
            subs.append(SP.POPplot(axes[0], self, T.ti, lw2=0.5, sz1=4, sz2=3, sz3=4.0, alp=0.3).draw_common_popout(MINI=True)) 
            subs.append(SP.SibPlot(axes[1], self, T.ti, sz1=7, sz2=4, sz3=3, alp=0.3, fs2=5).draw_mini_sib_pair()) 
            subs.append(SP.EvoScatter(axes[2], self, T.ti).mini_box(fs=5,sz=6,lw=0.33)) 
        return

