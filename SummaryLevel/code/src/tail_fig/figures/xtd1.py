import sys,os 
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path: sys.path.insert(0, HERE)
from util.Util import * 
from util import drawScatter as SP
from util import drawVarious as DV

class SumStats:
    def __init__(self, betas, pvs): 
        self.betas, self.pvs = betas, pvs 
        self.binnedB = self.get_binned_betas() 
        self.binnedP   = self.get_binned_pvs() 
        
    def get_binned_betas(self): 
        C = dd(int) 
        betas = sorted(self.betas) 
        self.beta_avg = str(round(np.mean(betas),2)) 
        cutoffs, c = [-0.15,-0.05,0.05,0.15,0.25,0.35,0.45,0.55,0.65,0.75,0.85,0.95,1.05,1.15,1.25], 0
        for e in betas:
            while e > cutoffs[c]: c+=1 
            C[cutoffs[c]] += 1 
        X,Y = [], [] 
        for c in cutoffs: 
            X.append(round(c-0.05,2)) 
            Y.append(C[c]) 
        return X,Y 

    def get_binned_pvs(self): 
        self.sig = len([p for p in self.pvs if p < 0.05]) 
        C = dd(int)         
        cutoffs, c = [1.3, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29,999], 0 
        pvs = sorted(self.pvs,reverse=True) 
        log_p = [-math.log(p,10) for p in pvs] 
        for pv,p in zip(pvs,log_p): 
            if p > cutoffs[c]: c+= 1 
            C[cutoffs[c]] += 1 
        X,Y = [], [] 
        for c in cutoffs: 
            if c < 999:  X.append(c) 
            else:        X.append(32.3) 
            Y.append(C[c]) 
        return X,Y 

    def get_bin_data(self, X, loc, dt = 'pvs'): 
        SIG, C = 0, dd(int)  
        if dt == 'pvs': 
            for p in X: 
                if p < 0.5: xx = -0.7
                elif p < 1.3: xx = 0.3
                else: 
                    SIG+=1 
                    if p < 20: xx = int(p) + 0.3 
                    else:      xx = 20.3
                C[xx] += 1
            return SIG, C 
        else: 
            for e in X: 
                if e < -0.2: xx = -0.1 
                elif e > 1.0: xx = 1.0 
                else: xx = round(e,1) 
                C[xx] += 1 
            return SIG, C 












class MyFigure:
    def __init__(self, options, traits, progress, figName=None):
        self.options, self.data, self.traits, self.figName = options, traits, traits.members, figName
        self.progress = progress.update(self) 
        self.exampleTraits = self.get_valid_examples()
        self.fs1, self.fs2, self.fs3, self.fs4 = 10, 8, 7 , 5

    def get_valid_examples(self):
        X, cands = [], []
        for c in [50,21002,30020,30070,30870]:
            if c in self.traits and 'apop' in self.traits[c].pts and 'common@5' in self.traits[c].pts['apop']: cands.append(c)
        for i,ti in enumerate(self.options.indexTraits):
            if ti in self.traits and 'pop' in self.traits[ti].pts and 'aou' in self.traits[ti].pts['pop']: X.append(ti)
            else:
                opts = [c for c in cands if c not in self.options.indexTraits + X]
                if len(opts) > 0: X.append(opts[0])
                else:             X.append(ti)
        return X

    def draw(self): 
        self.setup() 
        self.create() 
        self.finish() 

    def setup(self):
        self.rows, self.cols = 13, 25
        self.WD, self.HT = 50, 25
        self.WD, self.HT = 7.2, 3.6
        self.ax_index, self.base = 0, 0
        self.fig, self.axes = matplotlib.pyplot.gcf(), [] 
        for loc in range(0,25,5):
            self.axes.append(plt.subplot2grid((self.rows,self.cols), (0,loc), rowspan = 2, colspan =2))
            self.axes.append(plt.subplot2grid((self.rows,self.cols), (0,loc+2), rowspan = 2, colspan =2))
            self.axes.append(plt.subplot2grid((self.rows,self.cols), (2,loc), rowspan = 2, colspan =2))
            self.axes.append(plt.subplot2grid((self.rows,self.cols), (2,loc+2), rowspan = 2, colspan =2))
        for loc in range(0,25,5): self.axes.append(plt.subplot2grid((self.rows,self.cols), (5,loc), rowspan = 3, colspan =4))
        for loc in range(0,25,5): self.axes.append(plt.subplot2grid((self.rows,self.cols), (9,loc), rowspan = 3, colspan =4))
        self.fig.set_size_inches(self.WD, self.HT) 
        return         

   
    def create(self, fs=33): 
        self.c1, self.c1e, self.c2, self.c2e = 'blue', 'cyan', 'xkcd:shamrock green', 'lime' 
        self.rc, self.rce = 'gold', 'xkcd:bright yellow' 
        xLabs, yLabs = [None,None,'Trait Centile','Trait Centile'],['PRS',None,'PRS',None]
        self.locs = [10, 5, 1, 0.5, 0.1] 
        self.names = ['10%','5%','1%','0.5%','0.1%'] 
        self.lookups = ['common@10','common@5','common-snp','common@0.5','common@0.1'] 
        

        self.progress.set_panel('a') 
        for i,k in enumerate([0.1,0.5,1,5,10]):
            axes = self.axes[i*4:4+i*4] 
            for j,ti in enumerate(self.exampleTraits): 
                sp = SP.POPplot(axes[j], self, ti,xLab=xLabs[j], yLab=yLabs[j], sz1=9,sz2=8,sz3=6)
                if k == 1: 
                    sp.draw_body('common', ALLOW_MISSING=False)
                    if sp.VALID: 
                        sp.draw_tail()
                        sp.mark_significance()
                else:
                    sp.draw_alt(self.lookups[i],ALLOW_MISSING=False)
                x1,y1,xs,ys = sp.lms.xMin, sp.lms.yMax, sp.lms.xHop, sp.lms.yHop
                if j == 0: sp.ax.text(x1+xs*50,y1+ys,self.names[i], ha='center',va='bottom',fontsize=self.fs3, zorder=10) 
                try: 
                    fn = self.traits[ti].name.mini 
                    if len(fn.split()) > 1: fn = " ".join(fn.split()[0:-1])+'\n'+fn.split()[-1] 
                    sp.ax.text(x1+xs,y1-ys,fn, ha='left',va='top',fontsize=self.fs4) 
                except: pass 
        SK = dd(list) 
        for loc,k in zip(self.locs, self.lookups): 
            if k == 'NA': continue 
            effects, pvs = [], [] 
            for ti,T in self.traits.items(): 
                if k not in T.vals['pop']: continue  
                P = T.vals['pop'][k]
                effects.extend([P.e1,P.e2]) 
                pvs.extend([P.p1, P.p2]) 
            SK[loc] = SumStats(effects,pvs) 
        self.ax_index = 20        
        self.draw_bins(SK, self.axes[20::]) 
        if self.progress.SAVESRC: self.save_bins(SK) 
        return 

    def save_bins(self, LK): 
        self.progress.set_panel('b') 
        w = self.progress.out3
        w.write('%s,%s,%s,%s\n' % ('Panel', 'POPout-TailSize','DataType','Values'))
        for i,(name,loc) in enumerate(zip(self.names,self.locs)): 
            if loc in LK:
                w.write('%s,%s,%s,%s\n' % (self.progress.panel,name,'POPoutEffectSize-bins',";".join([str(b) for b in LK[loc].binnedB[0]])))
                w.write('%s,%s,%s,%s\n' % (self.progress.panel,name,'POPoutEffectSize-cnts',";".join([str(b) for b in LK[loc].binnedB[1]])))
        self.progress.set_panel('c') 
        w = self.progress.out3
        w.write('%s,%s,%s,%s\n' % ('Panel', 'POPout-TailSize','DataType','Values'))
        for i,(name,loc) in enumerate(zip(self.names,self.locs)): 
            if loc in LK:
                w.write('%s,%s,%s,%s\n' % (self.progress.panel,name,'POPoutLogP-bins',";".join([str(b) for b in LK[loc].binnedP[0]])))
                w.write('%s,%s,%s,%s\n' % (self.progress.panel,name,'POPoutLogP-cnts',";".join([str(b) for b in LK[loc].binnedP[1]])))
        return 
    
    def draw_bins(self, LK, axes): 
        sB, sP, ax_index = [], [], 20 
        for i,(name,loc) in enumerate(zip(self.names,self.locs)): 
            pt = 'Bin='+name+', ' 
            ax1, ax2 = axes[i], axes[i+5] 
            if loc in LK:
                SS = LK[loc] 
                ax1.bar(SS.binnedB[0], SS.binnedB[1], width=0.1, align='edge', color='purple') 
                X,Y = SS.binnedP[0], SS.binnedP[1] 
                for j,(x,y) in enumerate(zip(X,Y)): 
                    if j == 0:  
                        ax2.bar(0,Y[0],width=X[0],align='edge',color='white',ec='darkgreen') 
                    elif j == 1: ax2.bar(X[j-1],Y[1],width=X[1]-X[0],align='edge',color='green',ec='darkgreen') 
                    else:        ax2.bar(x-2,y,width=2,align='edge',color='green',ec='darkgreen') 
            sB.append(str(SS.beta_avg)) 
            sP.append(str(SS.sig)) 
            lms1 = DV.AxLims(ax1,xlab = 'POPout Effect Size', ylab = 'Count', ystretch=0, xstretch=0,fs = 6, COMMANDS=['noSpines'], CORNERS=[['topRight',pt+'\nAvg='+SS.beta_avg,5]]) 
            lms2 = DV.AxLims(ax2,xlab = '$-log_{10}(P{-}Value)$', ylab = 'Count', ystretch=0, xstretch=0,fs = 6, COMMANDS=['noSpines'], CORNERS=[['topRight',pt+'#nom. sig='+str(SS.sig),5]]) 
        self.progress.report_result('Avg Effect Size Across Alt Bins (10%,5%,1%,0.5%,0.1%): '+str(",".join(sB)))
        self.progress.report_result('Number Non-Sig Across Alt Bins (10%,5%,1%,0.5%,0.1%): '+str(",".join(sP)))

    def finish(self, fs =13):
        letters = ['$a$','$b$','$c$','$d$','$e$','$f$'] 
        for i,x in zip([0,20,25],['$a$','$b$','$c$']): 
            if i == 0:   self.axes[i].set_title(x, x= -0.17, y = 0.80, fontsize=fs) 
            elif i == 20:   self.axes[i].set_title(x, x= -0.11, y = 0.97, fontsize=fs) 
            elif i == 25:   self.axes[i].set_title(x, x= -0.11, y = 0.97, fontsize=fs) 
        plt.subplots_adjust(left=0.04, bottom=0.001, right=1.03, top=0.96,wspace=0.05, hspace=0.05) 
        self.progress.save() 
        return

