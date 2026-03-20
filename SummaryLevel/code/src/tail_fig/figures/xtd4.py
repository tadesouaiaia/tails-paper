import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path: sys.path.insert(0, HERE)
from util.Util   import * 
from util import drawScatter as SP 
from util import drawTables as DT
from util import drawVarious as DV 

# Extended Data Figure: All Tail Plots # 

class MyFigure:
    def __init__(self, options, traits, progress, figName=None): 
        self.options, self.traits, self.data, self.progress, self.figName = options, traits.members, traits, progress, figName
        self.C1 = 'xkcd:very light blue' 
        self.C1 = 'xkcd:very light pink' 
        self.C2 = 'xkcd:off white' 

        self.E1, self.E2 = 'darkslategray','gray' 


    
    def draw(self, step=75): 
        n, trait_ids = 2, [x[1] for x in sorted([[T.name.mini, T.ti] for T in self.traits.values()])] 
        if self.figName is not None: 
            if len(trait_ids) <= step: self.fignames = [self.figName+'.pdf'] 
            else:                    self.fignames = [self.figName+'-1.pdf'] 
        else: 
            if len(trait_ids) <= step: self.fignames = ['table1.pdf'] 
            else:                    self.fignames = ['table1-1.pdf'] 
        for i in range(0,len(trait_ids),step): 
            self.my_ids, self.my_len = trait_ids[i:i+step], len(trait_ids[i:i+step]) 
            self.setup() 
            self.create() 
            self.finish() 
            self.fignames.append(self.fignames[-1].split('-')[0]+'-'+str(n)+'.pdf') 
            n+=1 
        figPath = self.options.out+self.fignames[0] 
        self.progress.save('(Figure Saved: '+figPath+')')
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
        plt.savefig(self.options.out+self.fignames[-1],dpi=600)  
        plt.clf() 



    def create(self): 
        dt = DT.SummaryTable(self).initalize(self.axes[0],self.axes[1],c1=self.i1,c2=self.i2) 
        dt = DT.SummaryTable(self).initalize(self.axes[2],self.axes[3],c1=self.i1,c2=self.i2) 
        dt = DT.SummaryTable(self).initalize(self.axes[4],self.axes[5],c1=self.i1,c2=self.i2) 
        self.ax_index += 6 
        
        count = 0 
        
        self.clr = self.C1
        self.clr = 'white' 
        for ti in self.my_ids: 
            T = self.traits[ti] 
            dt.add_trait(self.axes[self.ax_index], T, self.clr) 
            for j in [1,2,3]: self.axes[self.ax_index+j].set_facecolor(self.clr) 
            self.draw_subplots(T) 
            self.ax_index += 4 
            count += 1
            continue 
            if count == 3: 
                count = 0 
                if self.clr == self.C1: self.clr = self.C2 
                else:                   self.clr = self.C1 
        
        for ax in self.axes[self.ax_index::]: ax.axis('off') 

        return self




    def draw_subplots(self, T, mp = 9.08, lw = 4):  
        subs = [] 
        axes = self.axes[self.ax_index+1::] 
        subs.append(SP.POPplot(axes[0], self.traits, T.ti, lw2=0.5, sz1=4, sz2=3, sz3=4.0, alp=0.3).draw_common_popout(MINI=True)) 
        subs.append(SP.SibPlot(axes[1], self.traits, T.ti, sz1=7, sz2=4, sz3=3, alp=0.3, fs2=5).draw_mini_sib_pair()) 
        subs.append(SP.draw_mini_evo(axes[2], T,fs = 5, sz=6, lw=0.22, MINI=True)) 
        return
        for i,lms in enumerate(subs): 
            ax = lms.ax
            xs, ys = lms.xHop, lms.yHop
            xp1, yp1  = lms.xMin + xs*2, lms.yMin + ys*2 
            xp2, yp2  = lms.xMax - xs*2, lms.yMax - ys*2 
            if i == 0:
                pp = 0 
                for j,k in enumerate([Z.lower.popout['common-snp'], Z.upper.popout['common-snp']]):
                    if k.e > 0 and k.fdr == True: pp += j+1 
                if pp == 1:    ax.text(xp1, yp2, 'Lower Tail\nPOPout', ha='left', va='top',fontsize=20) 
                elif pp == 2:  ax.text(xp2, yp1, 'Upper\nTail POPout', ha='right', va='bottom',fontsize=20) 
                elif pp == 3:  ax.text(lms.xMid-xs*2, yp2, 'Dual Tail\nPOPout', ha='center', va='top', fontsize=20) 


            elif i == 1: 
                pp, pt = 0, []  
                for j,k in enumerate([Z.lower.sib_pvs.key, Z.upper.sib_pvs.key]): 
                    if k['meta'] > 0.05: continue 
                    else: 
                        if k['novo'] < 0.01 and k['novo'] < k['mend']: 
                            pp += j+1 
                            pt.append('novo') 
                        elif k['mend'] < k['novo'] and k['mend'] < 0.01:  
                            pp += j+1 
                            pt.append('mend') 
                        else: 
                            pt.append('NA')
                
                if 'mend' in pt: ax.text(lms.xMid-xs*2, yp2, 'Mendelian\nUpper Tail', ha='center', va='top',fontsize=20) 
                elif pp != 0: 
                    if pp == 1:    ax.text(xp1, yp2, 'Lower Tail\nDiff', ha='left', va='top',fontsize=20) 
                    elif pp == 2:  ax.text(xp2, yp1, 'Upper\nTail Diff', ha='right', va='bottom',fontsize=20) 
                    elif pp == 3:  ax.text(lms.xMid-xs*2, yp2, 'Dual Tail\nDiffs', ha='center', va='top', fontsize=20) 
            else: 
                model, kind, direc = [Z.summary['evo'][kk] for kk in ['model','type','dir']]
                if model == 'Y~yInt': continue 

                elif T.ti == 3581: 
                    ax.text(xp1, yp2, 'Distruptive,\nPos', ha='left', va='top',fontsize=20) 
                
                elif model == 'Y~yInt+X' and kind == 'linear': 
                    if direc == 'positive': ax.text(xp1, yp2, 'Positive', ha='left', va='top',fontsize=20) 
                    else:                   ax.text(xp2, yp2, 'Negative', ha='right', va='top',fontsize=20) 
                
                elif model == 'Y~yInt+X2' and kind == 'parabolic' and direc == 'stabilizing': 
                    ax.text(lms.xMid-xs*2, yp2, 'Stabilising', ha='center', va='top', fontsize=20) 
                elif model == 'Y~yInt+X+X2' and kind == 'quadratic': 
                    if direc == 'positive': ax.text(xp1, yp2, 'Stabilising,\nPos', ha='left', va='top',fontsize=19) 
                    else:                   ax.text(xp2, yp2, 'Stabilising,\nNeg', ha='right', va='top',fontsize=20) 
                else: 
                    self.progess.error('Unknown Evo Model: '+model) 



        return




   



















