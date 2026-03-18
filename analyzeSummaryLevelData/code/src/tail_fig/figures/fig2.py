#!/usr/bin/python3

import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path: sys.path.insert(0, HERE)

from util.Util   import * 
from util import drawForest as FP 
from util import drawScatter as SP 
from util import drawPreds as DP 
from util import drawVarious as DV 
from util import drawLabels  as DL 











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
        self.ax_index, self.base = 0, 20
        self.fig, self.axes = matplotlib.pyplot.gcf(), [] 
        self.rows, self.cols, self.WD, self.HT = 36, 42, 7.1, 6.6 
        self.rows, self.cols, self.WD, self.HT = 100, 100, 7.1, 6.6 
        rs1, rs2, rs3  =  6, 12, 18
        cs1, cs2, cs3  =  8, 10, 13
        rs1, rs2, rs3, rs4 = 17, 50, 15, 9 
        cs1, cs2 = 18, 30 
        for i in [0,rs1]: 
            for j in [0,cs1]: 
                self.axes.append(plt.subplot2grid((self.rows,self.cols), (i,j), rowspan = rs1, colspan =cs1))
        self.axes.append(plt.subplot2grid((self.rows,self.cols), (3,4+cs1*2), rowspan = rs2+2, colspan =cs2))
        self.axes.append(plt.subplot2grid((self.rows,self.cols), (5,4+cs1*2+cs2), rowspan = rs2+4, colspan =cs2))
        for rl in [rs1*2+9, rs1*2+9+(rs3+rs4)+6]: 
            for i in [0,rs3]: 
                for j in [0,cs1]: 
                    if i == 0: self.axes.append(plt.subplot2grid((self.rows,self.cols), (i+rl,j), rowspan = rs3, colspan =cs1))
                    else:      self.axes.append(plt.subplot2grid((self.rows,self.cols), (i+rl,j), rowspan = rs4, colspan =cs1))
        self.axes.append(plt.subplot2grid((self.rows,self.cols), (rs2+16,cs1*2+9), rowspan = self.rows-(rs2+16), colspan =self.cols-(cs1*2+17)))
        self.fig.set_size_inches(self.WD, self.HT) 
        return self       
   

    def create(self):
        xLabs, yLabs, popRes = [None,None,'Trait Centile','Trait Centile'],['PRS',None,'PRS',None], [] 
        for i,ti in enumerate(self.options.indexTraits): 
            sp = SP.POPplot(self.axes[i], self.traits, ti, xLab=xLabs[i], yLab=yLabs[i]) 
            sp.draw_common_popout() 
        
        DL.BoxKeys(self.axes[2]).add_popout_key('bottom-2') 
        
        self.ax_index += len(self.options.indexTraits) 
        fp = FP.ForestPlot(self.axes[self.ax_index: self.ax_index+2], self).draw_up_to_three()   
        self.add_preds(self.axes[self.ax_index+2:self.ax_index+10]) 
        
        DL.BoxKeys(self.axes[-3]).add_prediction_key('bottom-2') 
        self.create_reps(self.axes[-1]) 
        return


    def finish(self):
        letters = ['$a$','$b$','$c$','$d$','$e$','$f$'] 
        for i,ax in enumerate([self.axes[0], self.axes[4], self.axes[6], self.axes[-1]]): 
            lms = DV.AxLims(ax) 
            xp, yp, xs, xh, ys, yh = lms.xMin, lms.yMax, lms.xStep, lms.xHop, lms.yStep, lms.yHop 
            if i == 0: ax.text(xp-1.5*xs, yp-ys, letters[i], fontsize=self.fs1, fontweight='bold', ha='left', va='bottom', clip_on=False) 
            elif i == 1: 
                ax.text(xp, yp+yh, letters[i], fontsize=self.fs1, fontweight='bold', ha='left', va='bottom', clip_on=False) 
                ax.text(xp+xs*6,yp+yh*1.5,'UKB $POPout$ Analysis (EUR)',fontsize=self.fs2+0.6,ha='center',va='bottom',clip_on=False) #fontweight='bold') 
            else: ax.text(xp-xs, yp, letters[i], fontsize=self.fs1, fontweight='bold', ha='left', va='bottom', clip_on=False) 

        plt.subplots_adjust(left=0.03, bottom=0.04, right=1.02, top=0.98,wspace=0.01, hspace=0.05) 
        if self.figName is not None: figPath = self.options.out+self.figName+'.pdf' 
        else:                        figPath = self.options.out+'Fig2.pdf' 
        plt.savefig(figPath, dpi=self.options.dpi) 
        plt.clf() 
        self.progress.save('(Figure Saved: '+figPath+')')
        return 








    def add_preds(self, axes): 
        dp = DP.PredPlot(self.options) 
        if self.options.indexTraits[1] in self.traits: dp.draw_odds(self.traits[self.options.indexTraits[1]], axes[0:4]) 
        elif self.options.indexTraits[0] in self.traits: dp.draw_odds(self.traits[self.options.indexTraits[0]], axes[0:4]) 
        else:                                            dp.draw_odds(None, axes[0:4]) 
        if self.options.indexTraits[2] in self.traits: dp.draw_odds(self.traits[self.options.indexTraits[2]], axes[4:8]) 
        elif self.options.indexTraits[3] in self.traits: dp.draw_odds(self.traits[self.options.indexTraits[3]], axes[4:8]) 
        else:                                            dp.draw_odds(None, axes[4:8]) 
        return
        

    def collect_reps(self, MIN_REPS=20): 
        PD, rep_removes = dd(lambda: dd(list)), dd(lambda: dd(int))  
        AS = dd(list) 
        for k in self.rep_color_key.keys(): 
            RK = dd(list) 
            for ti,T in self.traits.items(): 
                e1, e2 = T.vals['pop']['common-snp'].e1 , T.vals['pop']['common-snp'].e2  
                try: 
                    R = T.vals['pop'][k] 
                    r1, r2, name, size, QC= R.e1, R.e2, R.name, R.size, (R.QC == 'PASS') 
                    AS[k].append(size) 
                    if QC and size > 5000: 
                        for n,data in [['X',[e1,e2]],['Y',[r1,r2]],['xL',[e1]],['xH',[e2]],['yL',[r1]],['yH',[r2]], ['S',[size]]]: RK[n].extend(data)
                    else: 
                        if not QC: rep_removes[k]['QC'] += 1 
                        if size <= 5000: rep_removes[k]['5k'] += 1 
                        rep_removes[k]['TOTAL'] += 1 
                except KeyError: continue 
            if len(RK['X']) > MIN_REPS: PD[k] = RK  
        
        rems = sorted([k+'(Total/QC/5k): '+str(V['TOTAL'])+','+str(V['QC'])+','+str(V['5k']) for k,V in rep_removes.items()]) 
        kept = ",".join([str(len(PD[k]['xL'])) for k in ['aou','poc','rep']]) 
        self.progress.report_result('Replication Removals: '+', '.join(rems)) 
        
        self.progress.report_result('Replication Kept: aou,poc,rep: '+kept) 
        return PD 





    def create_reps(self,ax, fs = 7, fs2 = 6): 
        PD = self.collect_reps() 
        try: xe = 0.1 + max([max(T.vals['pop']['common-snp'].e1,T.vals['pop']['common-snp'].e2) for T in self.traits.values()]) 
        except: xe = 0.58
        for k,clr in self.rep_color_key.items(): 
            if k not in PD: continue     
            ax.scatter(PD[k]['xL'], PD[k]['yL'], marker='v', color = clr, s= 12, ec='k',lw=0.1, zorder=10) 
            ax.scatter(PD[k]['xH'], PD[k]['yH'], marker='^', color = clr, s= 12, ec='k',lw=0.1, zorder=10) 
            #X,Y = PD[k]['X'], PD[k]['Y'] 
            R,Rpv = DV.add_scatter_corr(ax, PD[k]['X'], PD[k]['Y'], clr=clr, fs=fs+1, lw=1.5, EXTEND=xe, REP=k) 
            ss_str = ' (Avg SampleSize: '+str(round(np.mean(PD[k]['S']),1))+') '
            self.progress.report_result('Replication on '+k+' '+str(len(PD[k]['xL']))+' Traits, R='+str(round(R,3))+', p='+str(Rpv)+ss_str) 
        x1,x2 = -0.26, 0.76
        x1,x2 = -0.26, 0.78
        y1,y2 = -0.4, 0.64
        ax.set_xlim(x1,x2) 
        ax.set_ylim(y1,y2) 
        ax.set_xticks([-0.2,0,0.2,0.4,0.6]) 
        ax.set_xlabel('UKB $POPout$ Effect (EUR)',fontsize=fs+1, x=0.525,labelpad=1) 
        ax.set_ylabel('Replication $POPout$ Effect',fontsize=fs+1, x=0.58,labelpad=1) 
        ax.scatter(x2-0.25,y1+0.15,marker='^', s = 10, color='k') 
        ax.text(x2-0.225, y1+0.13, 'Upper Tail', fontsize=fs) 
        ax.scatter(x2-0.25,y1+0.07,marker='v', s = 10, color='k') 
        ax.text(x2-0.225, y1+0.05, 'Lower Tail', fontsize=fs) 
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)



    def draw_alternate(self, figprefix = 'Fig2Alt', fs1=8): 


        self.ax_index = 0 
        self.fig, self.axes = matplotlib.pyplot.gcf(), [] 
        self.rows, self.cols, self.WD, self.HT = 23, 35, 50, 50
        self.WD, self.HT = 35, 25 
        self.WD, self.HT = 7.1, 6.5 
        rs1, rs2, rs3 = 6, 12, 18
        cs1, cs2, cs3  = 8, 10, 13 
        rl = 0 
        pred_pairs, idx = [], 0
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
            axl.ax.text(x1+19,y1,'Observed Performance',va='center',fontsize=fs1) 
            axl.ax.plot([x2,x2+14],[y1,y1], clip_on=False,color='darkorange',linestyle='--',lw=1) 
            axl.ax.text(x2+15,y1,'Expected Performance',va='center',fontsize=fs1) 
            y1,y2 = y1-0.45,y1+0.45
            DV.draw_square(axl.ax, x1-axl.xHop*5, x2+axl.xStep*10, y1, y1 + axl.yStep*4) 
        except: pass 
        plt.subplots_adjust(left=0.03, bottom=-0.022, right=0.99, top=0.955,wspace=0.05, hspace=0.05) 
        
        if self.figName is not None: plt.savefig(self.options.out+self.figName+'.pdf',dpi=400)        
        else: plt.savefig(self.options.out+figprefix+'.pdf',dpi=400)     






