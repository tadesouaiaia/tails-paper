import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))                                                                                                                                                                                                                                            
if HERE not in sys.path: sys.path.insert(0, HERE)                                                                                                                                                                                                                                            
from Util import *
import drawVarious as DV
import drawLabels as DL 


class SlimLib: 
    def __init__(self, options, XTD=False):
        self.options, self.XTD = options, XTD
        self.colors = ['dimgrey','xkcd:tea','cornflowerblue','xkcd:electric pink','springgreen','magenta','deeppink','pink','orange','gold','yellow']
        self.colors = ['dimgrey','xkcd:tea','cornflowerblue','xkcd:pumpkin orange','springgreen','magenta','deeppink','pink','orange','gold','yellow']
        self.c1, self.c2 = self.colors[0], self.colors[3] 
        self.fs1, self.fs2, self.fs3, self.fs4, self.fs5 = 10, 8, 7,6,5
        self.sz1, self.sz2,self.sz3 = 15,12,10
        self.lw1, self.lw2,self.lw3 = 1,0.8,0.6
        if XTD: self.read_in_dists(options.simPath) 
        else:   self.read_in_files(options.simPath) 

    def read_in_dists(self, simPath): 
        self.SLIM = False  
        for f in os.listdir(simPath): 
            if f == 'slim.dists.txt':
                try: self.s_data = self.read_dists(simPath+'/'+f) 
                except: continue 
                self.SLIM=True
        return 

    def read_in_files(self, simPath): 
        found = [] 
        for f in os.listdir(simPath): 
            try:
                if f == 'enrich.csv': 
                    try: self.e_data = self.read_enrichment(simPath+'/'+f) 
                    except: pass 
                    found.append('enrich') 
                elif f == 'deltas.txt': 
                    try: self.d_data = self.read_deltas(simPath+'/'+f) 
                    except: continue 
                    found.append('deltas') 
                else: continue 
            except: pass 
        if 'deltas' in found and 'enrich' in found: self.SLIM = True 
        else:                                       self.SLIM = False 
        return 


    def read_deltas(self, F): 
        K = dd(lambda: {}) 
        with open(F) as f:
            for line in f: 
                line = line.split() 
                if len(line) == 0: continue  
                b = int(line[0]) 
                bd = [float(x) for x in line[-1].split(',')] 
                if line[1] == 'SELECT': K['SELECT'][b] = bd 
                else:                   K['NEUTRAL'][b] = bd 
        return K 


    def read_enrichment(self, F): 
        K = dd(lambda: {}) 
        G = dd(lambda: {}) 
        with open(F) as f:
            header = [x.strip('\"') for x in f.readline().strip().split(',')] 
            for line in f: 
                line = [x.strip('\"') for x in line.strip().split(',')]
                mean, c_lo, c_hi = float(line[5]), float(line[6]), float(line[7]) 
                dt = line[1]+'@'+line[2] 
                loc = int(line[3]) 
                K[dt][loc] = [mean, c_lo, c_hi] 
                if dt == 'f1@maf1': pn = 'maf1_sel_all' 
                elif dt == 'f1@maf1_top': pn = 'maf1_sel_large' 
                elif dt == 'f1@n1_10': pn = 'maf05_sel_all' 
                elif dt == 'f1@n1_10_top': pn = 'maf05_sel_large' 
                elif dt == 'f100@maf1': pn = 'maf1_str_all' 
                elif dt == 'f100@maf1_top': pn = 'maf1_str_large' 
                elif dt == 'f100@n1_10': pn = 'maf05_str_all' 
                elif dt == 'f100@n1_10_top': pn = 'maf05_str_large' 
                else:                        pn = dt 
                G[pn][loc] = [mean, c_lo, c_hi] 
        return G 


    def read_dists(self, F): 
        K = dd(lambda: dd(lambda: dd(lambda: dd(list)))) 
        with open(F) as f:
            for line in f: 
                line = line.split() 
                try:    vals = [float(v) for v in line[-1].split(',')] 
                except: vals = [v for v in line[-1].split(',')] 
                K[line[0]][line[1]][line[2]][line[3]] = vals 
        return K 
        



    def plot_sim_curves(self, ax, lw=2): 
        VK = {} 
        XP = [1,2,3,4,5,6,11,16,21,26,31,36,41,46,51,56,61,66,71,76,81,86,91,96,97,98,99,100] 
        for k in self.e_data.keys(): VK[k] = [round(self.e_data[k][x][0],4) for x in XP] 
        keys = ['maf1_sel_all','maf1_sel_large','maf05_sel_all','maf05_sel_large','f10@maf1','f10@maf1_top','f10@n1_10','f10@n1_10_top','maf1_str_all','maf1_str_large','maf05_str_all','maf05_str_large'] 
        keys = ['maf1_sel_all','maf1_sel_large','maf1_str_large','maf05_str_large'] 
        x1,x2 = 5,8
        yp = 18 
        for i,k in enumerate(keys): 
            maf, sel, kind = k.split('_') 
            Y = VK[k] 
            c = self.colors[i] 
            if i == 0: txt = 'Weak Selection, MAF<$1\%$, All Effects' 
            elif k == 'maf1_sel_large': txt = 'Weak Selection, MAF<$1\%$, Large Effects' #($<1\%$ $MAF$) of Large Effect'  
            elif k == 'maf1_str_large': txt = 'Strong Selection, MAF<$1\%$, Large Effects' #($<1\%$ $MAF$) of Large Effect'  
            elif k == 'maf05_str_large': txt = 'Strong Selection, MAF<$0.05\%$, Large Effects'  
            else: txt = 'yo' 
            ax.plot([x1,x2],[yp,yp],lw=lw,color=c) 
            ax.text(x2+1,yp,txt,va='center',fontsize=self.fs3) 
            ax.plot(XP,Y,lw=lw,color=c)  
            yp+=3 
        ax.plot([-3,103],[1,1],linestyle='--', lw=3,color='dimgrey',zorder=0) 
        ax.set_xlim(-2,102) 
        ax.set_xlabel('Trait Quantiles',fontsize=self.fs2)  
        ax.set_ylabel('Rare Enrichment',fontsize=self.fs2) 
        ax.spines[['top','right']].set_visible(False) 
        return




    def plot_sim_boxes(self, ax, c1 = 'red',c2='grey', sz=100): 
        self.c2 = 'xkcd:darkish red'
        X = [x for x in range(100)]
        dt = [np.random.normal(0,0.3,100) for i in range(36)] 
        keys = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100]
        s_data, n_data = [self.d_data['SELECT'][k] for k in keys], [self.d_data['NEUTRAL'][k] for k in keys] 
        s_err = [2*stats.sem(d) for d in s_data] 
        n_err = [2*stats.sem(d) for d in n_data] 
        s_means = [np.mean(d) for d in s_data] 
        n_means = [np.mean(d) for d in n_data] 
        xp = [i for i in range(len(keys))] 
        ax.plot(keys,s_means, color=self.c2, lw=self.lw2) 
        ax.plot(keys,n_means, color=self.c1, lw=self.lw2) 
        for i,(x,s,n,se,ne) in enumerate(zip(keys,s_means, n_means, s_err, n_err)): 
            ax.scatter(x,s,color=self.c2,s=self.sz2,clip_on=False) 
            ax.plot([x,x],[s-se,s+se], color = self.c2,lw=self.lw2,clip_on=False)  
            ax.scatter(x,n,color=self.c1,s=self.sz2,clip_on=False) 
            ax.plot([x,x],[n-ne,n+ne], color = self.c1,lw=self.lw2,clip_on=False)  
        xlocs = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35]
        ax.set_xlabel('Trait Quantiles', fontsize=self.fs2) 
        ax.set_ylabel('POPout Effects', fontsize=self.fs2) 
        ax.plot([-2,36],[0,0],lw=1,color='k') 
        ax.set_yticks([0,0.25,0.5,0.75,1.0,1.25]) 
        ax.set_ylim(-0.1,1.45)
        ax.set_xlim(-1,101) 
        x1,x2,yp= 4,8,1.2
        for i,k in enumerate(['Neutrality','Selection']): 
            if i == 0: c = self.c1
            else:      c = self.c2 
            ax.plot([x1,x2],[yp,yp],lw=1,color=c) 
            ax.scatter(x1,yp,color=c,marker='o',s=self.sz1) 
            ax.scatter(x2,yp,color=c,marker='o',s=self.sz1) 
            ax.text(x2+3,yp,k,va='center',fontsize=self.fs4) 
            yp+=0.15
        ax.spines[['top','right']].set_visible(False) 
        return




    def plot_dists(self, axes, c1 = 'red',c2='grey', sz=100): 
        self.colors = [['#1b9e77','#d95f02','#7570b3'],['#1b9e77','#d95f02','#7570b3','#e7298a']]
        
        self.colors = [['blue','xkcd:pumpkin orange','xkcd:tea'],['#1b9e77','gold','#7570b3','#e7298a']]
        

        #self.colors = ['dimgrey','xkcd:tea','cornflowerblue','xkcd:pumpkin orange','springgreen','magenta','deeppink','pink','orange','gold','yellow']



        self.styles = ['-','--',':','-'] 
        opts = [['10k', '50k', '100k'],['gamma(u=0.05)', 'gamma(u=0.1)', 'gamma(u=0.2)', 'gaussian']]
        
        for i,et in enumerate(['EnrichmentByTime', 'EnrichmentByDist']): 
            for j,dt in enumerate(['Weak,1,All', 'Weak,1,Large', 'Strong,1,Large', 'Strong,0.05,Large']): 
                d1, d2, d3 = dt.split(',') 
                d_title = d1+' Selection, MAF < '+d2+'%,\n'+d3+' Effects' 
                ax = axes[i*4:i*4+4][j] 
                for ki,k in enumerate(opts[i]): 
                    X, Y = self.s_data[et][dt][k]['X'], self.s_data[et][dt][k]['Y'] 
                    ax.plot(X, Y, color=self.colors[i][ki], linewidth=self.lw1*2, alpha=0.7, linestyle=self.styles[ki], label=k) 
                lms = DV.AxLims(ax, yLim=[0,12], COMMANDS=['nospines'], xlab='Trait Quantiles',ylab='Rare Enrichment', fs=self.fs2) 
                ax.plot([lms.xMin, lms.xMax],[1,1], linestyle='--', color='k') 
                ax.text(lms.xMid, lms.yMax - 2*lms.yStep, d_title, ha='center', va='center', fontsize=self.fs2)  
        
        for i,ax in enumerate([axes[2], axes[6]]): 
            lms = DV.AxLims(ax) 
            xs, ys, xh, yh, yp = lms.xStep, lms.yStep, lms.xHop, lms.yHop, lms.yMin - 4*lms.yStep

            if i == 0: X, yp = [lms.xMid + xs*v for v in [2.5,3,5.5,8,10.5]], lms.yMin - 3*ys
            else:      X, yp = [lms.xMid + xs*v for v in [0.5,1,4,7,10,12.5]], lms.yMin - 4*ys
            yl = yp + yh*3 
            DV.draw_square(ax, X[0], X[-1], yp, yp + 1.5*ys, lw=0.3) 
            for j,(k,c) in enumerate(zip(opts[i],self.colors[i])): 
                ax.plot([X[j+1],X[j+1]+xs], [yl,yl], color=c, linestyle=self.styles[j],clip_on=False) 
                if i == 0: ax.text(X[j+1]+5.35*xh, yl, k, fontsize=self.fs2, va='center') 
                else: 
                    if k[0:5] == 'gamma': gs = '$\\gamma$('+k.split('=')[-1].split(')')[0]+')' 
                    else:                 gs = 'N(0,1)' 
                    ax.text(X[j+1]+5.4*xh, yl, gs, va='center', fontsize=self.fs2) 
        return



    def plot_pops(self, axes, c1 = 'red',c2='grey', sz=100): 
        for i,k in enumerate(['gamma0.05,Weak', 'gamma0.05,Strong', 'gamma0.1,Weak', 'gamma0.1,Strong', 'gamma0.2,Weak', 'gamma0.2,Strong', 'gaussian,Weak', 'gaussian,Strong']): 
            ax = axes[i] 
            for j,(t,c) in enumerate(zip(['Neutrality','Selection'],['grey','darkred'])):  
                X,Y,yL,yH = [self.s_data['POPoutByDist'][k][t][z] for z in ['X','Y','yL','yH']] 
                ax.scatter(X,Y, color=c, s = self.sz3, zorder=4) 
                for x,y1,y2 in zip(X,yL,yH): 
                    ax.plot([x,x],[y1,y2], lw= self.lw2, zorder=2, color=c) 
                lms = DV.AxLims(ax, yLim=[-0.2,3], COMMANDS=['nospines'], xlab='Trait Quantiles',ylab='POPout Effects', fs=self.fs2) 
                ax.plot([lms.xMin, lms.xMax],[0,0], color='k', lw = self.lw3, zorder=0) 
                dist, sel = k.split(',')[0].split('gamma')[-1], k.split(',')[-1]+' Selection' 
                if dist == 'gaussian': ax.text(lms.xMid, lms.yMax - 3*lms.yStep, 'N(0,1)\n'+sel, ha='center')  
                else:                  ax.text(lms.xMid, lms.yMax - 3*lms.yStep, '$\\gamma$('+dist+')\n'+sel, ha='center')
        ax = axes[2] 
        lms = DV.AxLims(ax) 
        xs, ys, xh, yh, yp = lms.xStep, lms.yStep, lms.xHop, lms.yHop, lms.yMin - lms.yStep*5
        X = [lms.xMid + xs*v for v in [3.5,4.25,7.5,9.75]]
        yl = yp + yh*3.65 
        DV.draw_square(ax, X[0], X[-1], yp, yp + 1.9*ys, lw=0.3) 
        for j,(k,c) in enumerate(zip(['Neutrality','Selection'],['grey','darkred'])): 
            ax.scatter(X[j+1], yl, color=c,s=self.sz1*2, clip_on=False) 
            ax.text(X[j+1]+1.0*xh, yl, k, fontsize=self.fs2, va='center') 










