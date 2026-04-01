import sys, os                                                                                                                                                                                                                                                                               
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path: sys.path.insert(0, HERE)
from util.Util   import *
from util import drawScatter as DS
from util import drawVarious as DV
from util import drawCartoon  as DC


class MyFigure:
    def __init__(self, options, traits, progress, figName=None):         
        self.options, self.data, self.figName = options, traits, figName
        self.traits = {ti: T for ti,T in traits.members.items() if 'sib' in T.vals} 
        self.progress = progress.update(self) 
        self.colors = ['red','green','blue','purple','orange','lime'] 
        self.fs0, self.fs1, self.fs2, self.fs3, self.fs4 = 10, 7, 6, 5, 5 
        self.sz1, self.sz2, self.sz3 = 15,10,8
        self.lib = DC.FigLib(options) 

    def draw(self): 
        self.setup() 
        self.create() 
        self.finish() 
    
    def draw_sib_schematic(self, axes): 
        ax1, ax2, ax3 = axes 
        self.lib.make_fake_sibs(ax1, TYPE='POLY') 
        self.lib.make_fake_sibs(ax2, TYPE='NOVO') 
        self.lib.make_fake_sibs(ax3, TYPE='MEND') 

    def setup(self): 
        self.fig, self.axes = matplotlib.pyplot.gcf(), [] 
        self.rows, self.cols, self.WD, self.HT = 60,73, 7.1,5 
        rs1,rs2,rs3, cs1,cs2,cs3 = 22,15,30,  12,13,(13*3)+8 
        self.axes.append(plt.subplot2grid((self.rows,self.cols), (0,1), rowspan = rs1+2, colspan =cs2))                                                                   
        self.axes.append(plt.subplot2grid((self.rows,self.cols), (0,1+cs2), rowspan = rs1+2, colspan =cs2))                                                                   
        self.axes.append(plt.subplot2grid((self.rows,self.cols), (0,1+2*cs2), rowspan = rs1+2, colspan =cs2))                                                                   
        self.axes.append(plt.subplot2grid((self.rows,self.cols), (0,cs3), rowspan = rs2, colspan =cs1))                                                                   
        self.axes.append(plt.subplot2grid((self.rows,self.cols), (0,cs3+cs1), rowspan = rs2, colspan =cs1))                                                                   
        self.axes.append(plt.subplot2grid((self.rows,self.cols), (rs2,cs3), rowspan = rs2, colspan =cs1))                                                                   
        self.axes.append(plt.subplot2grid((self.rows,self.cols), (rs2,cs3+cs1), rowspan = rs2, colspan =cs1))                                                                   
        self.axes.append(plt.subplot2grid((self.rows,self.cols), (rs2+15,2), rowspan = rs3-1, colspan =(cs2*3)-1))                                                               
        self.axes.append(plt.subplot2grid((self.rows,self.cols), (rs2*2+5,cs3), rowspan = rs2+9, colspan =cs1*2))                                                                   
        self.fig.set_size_inches(self.WD, self.HT)                                                                                                                                  
        self.ax_index, self.xLoc, self.fq1, self.fq2 = 0, 1, 24, 22                

    def finish(self):
        letters = ['a','b','c','d','e','e'] 
        fz =20
        for i,ai in enumerate([0,3,7,8]):
            ax = self.axes[ai] 
            lms = DV.AxLims(ax) 
            x,y,xs,ys = lms.xMin, lms.yMax, lms.xStep, lms.yStep 
            x-=xs*0.2
            if i == 0: ax.text(x+xs*0.65,y-ys*0.5, '$'+letters[i]+'$', ha='right', clip_on=False,fontsize=fz) 
            elif i == 1: ax.text(x-xs*0.3,y-ys*0.8, '$'+letters[i]+'$', ha='right', clip_on=False,fontsize=fz) 
            elif i == 2: ax.text(x,y, '$'+letters[i]+'$', ha='right', clip_on=False,fontsize=fz) 
            elif i == 3: ax.text(x,y, '$'+letters[i]+'$', ha='right', clip_on=False,fontsize=fz) 
        plt.subplots_adjust(left=0.01, bottom=0.025, right=1.01, top=0.97,wspace=0.5, hspace=0.5) 
        self.progress.save() 

    def create(self): 
        self.draw_sib_schematic(self.axes[0:3]) 
        self.ax_index = 3 
        self.progress.set_panel('b') 
        for i,ti in enumerate(self.options.indexTraits): sp = DS.SibPlot(self.axes[self.ax_index+i], self, ti, INIT=(i==0)).draw_sib_pair(i, LABEL=True) 
        self.progress.set_panel('c') 
        self.add_sib_pairs(self.axes[7]) 
        self.progress.set_panel('d') 
        self.add_h2_coord(self.axes[8]) 
        return 
        

    def add_h2_coord(self, ax, fs1 = 30, fs2 = 24, fs3 = 14): 
        T,X,Y = self.set_h2_coord(ax) 
        lw, ms, sb, D,F,C = 0.5, 1, 0, 'data', 'fancy','black'                                                                                                                                             
        astr = "fancy,head_width=2.5,head_length=2.5,tail_width=0.01"                                                                                                                               
        for t,x,y in zip(T,X,Y): 
            fn = t.name.box 
            if t.ti in [845]:     ax.text(x-0.03,y-0.03,fn, ha='left',va='center',fontsize = self.fs3, zorder=3, fontweight='bold') 
            elif t.ti in [20022]: ax.text(x,y+0.02,fn, ha='left',va='bottom',fontsize = self.fs3, zorder=3, fontweight='bold') 
            elif t.ti in [20015]: ax.text(x+0.005,y+0.022,'Sitting\nHeight', ha='center',va='bottom',fontsize = self.fs3, zorder=3, fontweight='bold') 
            elif t.ti in [50]:    ax.text(x,y+0.02,fn, ha='right',va='bottom',fontsize = self.fs3, zorder=3, fontweight='bold') 
            elif t.ti in [30070]: ax.text(x+0.0045,y-0.002,fn, ha='left',va='top',fontsize = self.fs2, zorder=3, fontweight='bold')  
            elif t.ti in [30810]: 
                x1,y1 = x,y-0.018
                x2,y2 = x-0.005, y-0.185
                cs = "arc3,rad=-0.02"                                                                                                                                                   
                el = matplotlib.patches.Ellipse((x1, y1), 0, 0, angle=0, alpha=0.0,fc=None,ec='black',zorder=0,linewidth=1,fill=False)                                                            
                AP=dict(arrowstyle=astr,linewidth=lw,mutation_scale=ms,color='black',patchB=el,shrinkB=sb,connectionstyle=cs)                                                           
                ax.annotate("",xy=(x1, y1), xycoords='data',xytext=(x2,y2),textcoords='data',arrowprops=AP)                                                           
                ax.text(x2+0.005,y2-0.02,fn, ha='center',va='center',fontsize = self.fs3, zorder=3, fontweight='bold') 
            elif t.ti in [30020]: 
                x1,y1 = x,y-0.0195
                x2,y2 = x-0.005, y-0.185
                cs = "arc3,rad=-0.02"                                                                                                                                                   
                el = matplotlib.patches.Ellipse((x1, y1), 0, 0, angle=0, alpha=0.0,fc=None,ec='black',zorder=0,linewidth=1,fill=False)                                                            
                AP=dict(arrowstyle=astr,linewidth=lw,mutation_scale=ms,color='black',patchB=el,shrinkB=sb,connectionstyle=cs)                                                           
                ax.annotate("",xy=(x1, y1), xycoords='data',xytext=(x2,y2),textcoords='data',arrowprops=AP)                                                           
                ax.text(x2+0.005,y2-0.033,'\n'.join(fn.split()), ha='center',va='center',fontsize = self.fs3, zorder=3, fontweight='bold') 

        xLab, yLab= 'SNP-estimated '+'$h^2$', 'Sibling-estimated '+'$h^2$'
        lms = DV.AxLims(ax,xlab=xLab,ylab=yLab,xstretch=0.5,ystretch=[1,0.01],xt=[0,0.1,0.2,0.3,0.4],yt=[0,0.2,0.4,0.6,0.8,1],fs = self.fs2,COMMANDS=['nospines']) 
        ax.set_xticklabels([0,0.1,0.2,0.3,0.4]) 
        ax.set_yticklabels([0,0.2,0.4,0.6,0.8,1]) 
        R, pv = DV.add_scatter_corr(ax,X,Y, fs=7, INTERCEPT=True) 
        self.progress.report_result('Sib/SnpH2 Correlation: '+str(round(R,3))+', pv='+str(pv))
        return 

    def set_h2_coord(self, ax): 
        if self.progress.SAVESRC: self.progress.out3.write('%s,%s,%s,%s\n' % ('Panel','Trait-ID','SNP-h2','Sib-h2'))
        T,X,Y = [], [], [] 
        for t in self.traits.values(): 
            T.append(t)
            X.append(vars(t.qc['misc'])['h2'])
            Y.append(t.vals['sib'].h2)   
            ax.scatter(X[-1],Y[-1], color=t.group_color, ec='k', s = self.sz2, lw=0.3, zorder=1) 
            if self.progress.SAVESRC: self.progress.out3.write('%s,%s,%s,%s\n' % (self.progress.panel,t.id,X[-1],Y[-1]))
        return T,X,Y 


    def add_sib_pairs(self, ax): 
        if self.progress.SAVESRC: self.progress.out3.write('%s,%s,%s,%s,%s\n' % ('Panel', 'Trait-ID','Tail','-log(POPout-P)','-log(STANDOUT-P)'))
        self.ax, X,Y,cnt = ax, [],[],0 
        for ti,T in self.traits.items(): 
            cnt += 1 
            p1, p2  =  [-math.log(T.vals['pop']['common-snp'].key[k],10) for k in ['p1','p2']]
            sd = T.vals['sib'].key 
            d1,d2 = [T.vals['sib'].key[k] for k in ['novo1','novo2']] 
            m1,m2 = [T.vals['sib'].key[k] for k in ['mend1','mend2']]
            b1,b2 = [T.vals['sib'].key[k] for k in ['meta1','meta2']]
            meta1, meta2 = -math.log(self.get_meta_p(d1,m1),10), -math.log(self.get_meta_p(d2,m2),10)
            for i,(x,y) in enumerate([[p1,meta1],[p2,meta2]]):  
                self.scatter_sib(x, y, i, T) 
                X.append(x) 
                Y.append(y) 
        xLab, yLab = '$POPout$ $P$-value ($-log_{10}P$)', '$STANDout$ $P$-value ($-log_{10}P$)'
        lms = DV.AxLims(self.ax,xlab=xLab,ylab=yLab,xLim=[min(X)-3,max(X)+5],yLim=[min(Y)-0.5,max(Y)+1],fs = self.fs2,COMMANDS=['nospines']) 
        R, pv = DV.add_scatter_corr(ax,X,Y, fs=7, INTERCEPT=False) 
        self.progress.report_result('POPout/STANDout Correlation: '+str(round(R,3))+', pv='+str(pv)) 
        x1, y1 = lms.xMax - lms.xStep * 3.6, lms.yMin + lms.yStep * 2 
        for i,(g,c) in enumerate(zip(self.data.group_names, self.data.group_colors)): 
            ax.scatter(x1,y1-lms.yHop*3.6*i,marker='s',color=c,s=self.sz1,ec='k', lw=0.5) 
            ax.text(x1+lms.xHop,y1-lms.yHop*3.6*i,g, fontsize=self.fs1,ha='left',va='center') 
        return



    def scatter_sib(self, x, y, i, T): 
        fn = T.name.mini
        if i == 0: 
            self.ax.scatter(x,y, marker = 'v', s = self.sz1, zorder=2,alpha=0.99,color = T.group_color, edgecolor ='k',lw=0.2)
            if T.ti in [30040]: self.ax.text(x, y+0.25,'Mean\nCorpuscular\nVol' , ha='right', va='bottom', color='k',fontweight='bold', fontsize=self.fs2) 
            elif T.ti in [20015]:  self.ax.text(x+0.25, y+0.42, fn, ha='left', va='top', color='k',fontweight='bold', fontsize=self.fs2) 
            elif T.ti in [30020]: self.ax.text(x, y+0.5, "\n".join(fn.split()), ha='center', va='center', color='k',fontweight='bold', fontsize=self.fs3) 
            if self.progress.SAVESRC: self.progress.out3.write('%s,%s,%s,%s,%s\n' % (self.progress.panel,T.ti,'Lower',x,y)) 
        else:
            self.ax.scatter(x,y, marker = '^', s = self.sz1, zorder=2,alpha=0.99,color = T.group_color, edgecolor ='k',lw=0.2)
            if T.ti in [30070]:  self.ax.text(x-1, y-0.25, fn, ha='left', va='top', color='k',fontweight='bold', fontsize=self.fs2) 
            elif T.ti in [20015]:       self.ax.text(x-2, y+0.5, fn, ha='left', va='top', color='k',fontweight='bold', fontsize=self.fs2) 
            elif T.ti in [845]:         self.ax.text(x-5, y+0.5, fn, ha='left', va='top', color='k',fontweight='bold', fontsize=self.fs2) 
            if self.progress.SAVESRC: self.progress.out3.write('%s,%s,%s,%s,%s\n' % (self.progress.panel,T.ti,'Upper',x,y)) 
        return 


    def get_meta_p(self, p_denovo, p_mend): 
        eps = 1e-300
        p_mend = max(min(p_mend, 1.0), eps)
        p_denovo = max(min(p_denovo, 1.0), eps)
        stat = -2.0 * (math.log(p_mend) + math.log(p_denovo))  
        meta_p = stats.chi2.sf(stat, df=4)
        return meta_p
        

