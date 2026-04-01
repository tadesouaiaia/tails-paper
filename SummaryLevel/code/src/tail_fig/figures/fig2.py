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
    def __init__(self, options, traits, progress, figName='main2'): 
        self.options, self.traits, self.data, self.figName = options, traits.members, traits, figName 
        self.progress = progress.update(self) 
        self.rep_color_key = {'rep': 'xkcd:purpley', 'poc': 'xkcd:barney', 'aou': 'xkcd:leaf green'} 
        self.fs0, self.fs1, self.fs2, self.fs3, self.fs4 = 20, 15, 10, 8, 5 
        self.name_swap = {'rep': 'rpt', 'poc': 'mlt', 'aou': 'aou'} 


    def draw(self): 
        self.setup() 
        self.create() 
        self.finish() 

    def setup(self): 
        self.ax_index, self.base = 0, 20
        self.fig, self.axes = matplotlib.pyplot.gcf(), [] 
        self.rows, self.cols, self.WD, self.HT = 100, 100, 7.1, 6.6 
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
        self.progress.set_panel('a') 
        for i,ti in enumerate(self.options.indexTraits): 
            sp = SP.POPplot(self.axes[i], self, ti, xLab=xLabs[i], yLab=yLabs[i], INIT=(i==0)) 
            sp.draw_common_popout() 
        DL.BoxKeys(self.axes[2]).add_popout_key('bottom-2') 
        self.ax_index += len(self.options.indexTraits) 
        self.progress.set_panel('b') 
        fp = FP.ForestPlot(self.axes[self.ax_index: self.ax_index+2], self).draw_up_to_three()   
        self.progress.set_panel('c') 
        dp = DP.PredPlot(self).draw_index_pair(self.axes[self.ax_index+2:self.ax_index+10])  
        DL.BoxKeys(self.axes[-3]).add_prediction_key('bottom-2') 
        self.progress.set_panel('d') 
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
                ax.text(xp+xs*6,yp+yh*1.5,'UKB $POPout$ Analysis (EUR)',fontsize=self.fs2+0.6,ha='center',va='bottom',clip_on=False) 
            else: ax.text(xp-xs, yp, letters[i], fontsize=self.fs1, fontweight='bold', ha='left', va='bottom', clip_on=False) 
        plt.subplots_adjust(left=0.03, bottom=0.04, right=1.02, top=0.98,wspace=0.01, hspace=0.05) 
        self.progress.save() 
        return 



    def collect_reps(self, MIN_REPS=20): 
        PD, rep_removes, named_removals, self.rep_src = dd(lambda: dd(list)), dd(lambda: dd(int)), dd(lambda: dd(list)), dd(lambda: {}) 
        for k in self.rep_color_key.keys(): 
            RK = dd(list) 
            for ti,T in self.traits.items(): 
                e1, e2 = T.vals['pop']['common-snp'].e1 , T.vals['pop']['common-snp'].e2  
                self.rep_src[T.ti]['ukb'] = [e1,e2]  
                try: 
                    R = T.vals['pop'][k] 
                    r1, r2, name, size, QC= R.e1, R.e2, R.name, R.size, (R.QC == 'PASS') 
                    if QC and size > 5000: 
                        for n,data in [['X',[e1,e2]],['Y',[r1,r2]],['xL',[e1]],['xH',[e2]],['yL',[r1]],['yH',[r2]], ['S',[size]]]: RK[n].extend(data)
                        self.rep_src[T.ti][k] = [r1,r2]  
                    else: 
                        if not QC: 
                            rep_removes[k]['QC'] += 1 
                            named_removals[k]['QC'].append(T.name.mini) 
                        if size <= 5000: 
                            rep_removes[k]['5k'] += 1 
                            named_removals[k]['5k'].append(T.name.mini) 

                        rep_removes[k]['TOTAL'] += 1 
                except KeyError: continue 
            if len(RK['X']) > MIN_REPS: PD[k] = RK  
        rems = sorted([self.name_swap[k]+'(Total/QC/5k): '+str(V['TOTAL'])+','+str(V['QC'])+','+str(V['5k']) for k,V in rep_removes.items()]) 
        kept = ",".join([str(len(PD[k]['xL'])) for k in ['aou','poc','rep']]) 
        self.progress.report_result('Replication Removals: '+', '.join(rems))  
        self.progress.report_result('Replication Kept: aou,mlt,rpt: '+kept) 
        return PD 





    def create_reps(self,ax, fs = 7, fs2 = 6): 
        PD = self.collect_reps() 
        try: xe = 0.1 + max([max(T.vals['pop']['common-snp'].e1,T.vals['pop']['common-snp'].e2) for T in self.traits.values()]) 
        except: xe = 0.58
        for k,clr in self.rep_color_key.items(): 
            if k not in PD: continue     
            ax.scatter(PD[k]['xL'], PD[k]['yL'], marker='v', color = clr, s= 12, ec='k',lw=0.1, zorder=10) 
            ax.scatter(PD[k]['xH'], PD[k]['yH'], marker='^', color = clr, s= 12, ec='k',lw=0.1, zorder=10) 
            R,Rpv = DV.add_scatter_corr(ax, PD[k]['X'], PD[k]['Y'], clr=clr, fs=fs+1, lw=1.5, EXTEND=xe, REP=k) 
            ss_str = ' (Avg SampleSize: '+str(round(np.mean(PD[k]['S']),1))+') '
            self.progress.report_result('Replication on '+self.name_swap[k]+' '+str(len(PD[k]['xL']))+' Traits, R='+str(round(R,3))+', p='+str(Rpv)+ss_str) 
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

        if self.progress.SAVESRC: 
            w = self.progress.out3
            w.write('%s,%s,%s,%s,%s,%s,%s\n' % ('Panel','Trait-ID','Tail','UKB-Euro-POPoutEffect','RepeatMeasure-RepEffect','Multi-Ancestry-RepEffect','AOU-RepEffect')) 
            Tk, trait_ids = dd(list), sorted([k for k in self.rep_src.keys()]) 
            for ti in trait_ids:
                if len(self.rep_src[ti].keys()) == 1: continue 
                RP = self.rep_src[ti] 
                for i,tail in enumerate(['lower','upper']): 
                    r_data = [self.progress.panel, ti, tail] 
                    for k in ['ukb','rep','poc','aou']: 
                        if k in self.rep_src[ti]: r_data.append(self.rep_src[ti][k][i]) 
                        else:                     r_data.append('NA') 

                    w.write('%s,%s,%s,%s,%s,%s,%s\n' % tuple(r_data)) 
                        

