import sys, os                                                                                                                                                                                                                                                                               
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path: sys.path.insert(0, HERE)

from util.Util   import *
from util import drawForest as FP
from util import drawScatter as SP
from util import drawPreds as DP
from util import drawVarious as DV
from util import drawLabels  as DL


# lw




class FigLib: 
    def __init__(self, options, AK={}):
        self.options = options
        self.nullMP = 800
        self.nullVar = 11.5
        self.Xn = np.arange(-40,40,0.05)
        self.Yn = [(y*self.nullMP) for y in stats.norm.pdf(self.Xn, 0, self.nullVar)]
        self.Yn =  [y - min(self.Yn) for y in self.Yn]
        self.distcolor = 'xkcd:dark cream'
        self.distcolor = 'xkcd:pale gold' 
        self.distcolor = 'xkcd:burnt yellow' 
        self.alpha=0.33




    def make_square(self,ax,x1,x2,y1,y2,lw=0.9,ls='--',ap=0.3):
        ax.plot([x1,x2],[y1,y1],clip_on=False,color='k',lw=lw,linestyle=ls,alpha=ap)
        ax.plot([x1,x2],[y2,y2],clip_on=False,color='k',lw=lw,linestyle=ls,alpha=ap)
        ax.plot([x1,x1],[y1,y2],clip_on=False,color='k',lw=lw,linestyle=ls,alpha=ap)
        ax.plot([x2,x2],[y1,y2],clip_on=False,color='k',lw=lw,linestyle=ls,alpha=ap)
    

    def make_human(self, xp, yp, ax, s = 2, bc='k', c = 'red', rc2 = 'lime', risk1=0, risk2=0):
        head1 = matplotlib.patches.Circle((xp + s*0.1, yp+ s*0.8), s*0.4, facecolor='blue', zorder=10)
        head2 = matplotlib.patches.Circle((xp + s*0.4, yp+ s*0.8), s*0.4, facecolor='green', zorder=10)
       	head = matplotlib.patches.Circle((xp + s/4.0, yp+ s), s/2.5, facecolor=c, zorder=10)
        left_arm =  matplotlib.patches.Rectangle((xp+s*0.1, yp+ s*0.6), s*0.2, s*0.95, angle=135, facecolor=c,zorder=10)
        right_arm = matplotlib.patches.Rectangle((xp+s*0.55, yp+ s*0.7), s*0.2, s*0.95, angle=-135, facecolor=c,zorder=10)
        body =      matplotlib.patches.Rectangle((xp, yp), s/2.0, s, facecolor=c, zorder=10)
        left_leg =  matplotlib.patches.Rectangle((xp+s*0.25, yp+s*0.10), s*0.25, s, angle=150,facecolor=c,zorder=10)
        right_leg = matplotlib.patches.Rectangle((xp+s*0.50, yp+s*0.20), s*0.25, s, angle=-150,facecolor=c,zorder=10)
        ax.add_patch(head)
        ax.add_patch(body)
        ax.add_patch(left_arm)
        ax.add_patch(right_arm)
        ax.add_patch(left_leg)
        ax.add_patch(right_leg)
 



    def make_arrow(self, ax, a = (0,8), b = (-8,3), FLIP=False, txt='NA', STYLE='NA'):  

        # Define arrow properties

        arrowstyle = "Simple, tail_width=0.2, head_width=2, head_length=1"
        
        if FLIP: connectionstyle = "arc3,rad=.1"  # Adjust the curvature with 'rad'
        else:    connectionstyle = "arc3,rad=-.1"  # Adjust the curvature with 'rad'
        arrow_properties = {"arrowstyle": arrowstyle,"color": "k",}
        # Define arrow start and end points
        tail_position = a 
        head_position = b 
        # Create the arrowi
        arrowstyle = "Simple,tail_width=0.03,head_width=0.5,head_length=0.5"


        arrow = matplotlib.patches.FancyArrowPatch(tail_position, head_position, connectionstyle=connectionstyle, mutation_scale=1, linewidth=0.5, **arrow_properties)
        # Add the arrow to the plot
        ax.add_patch(arrow)
        if txt != 'NA': ax.text(a[0],b[0]+5,txt,ha='center',va='center',fontsize=5) 



    def add_inset(self, ax, TYPE): 

        self.xi, self.xe = 6, 44 
        self.yi, self.ye = 27, 44 
        self.xm = self.xi + (self.xe-self.xi)/2.0 
        self.make_square(ax, self.xi, self.xe, self.yi, self.ye) 
        self.options = self.options
        self.nullMP = 800
        self.nullVar = 11.5
        self.Xi = np.arange(self.xi,self.xe,0.1)
        self.Yi = [self.yi+(y*200) for y in stats.norm.pdf(self.Xi, self.xm, 6.0)] 
        ax.plot(self.Xi, self.Yi,clip_on=False, lw = 1 , zorder=5, color=self.distcolor)  
        ax.fill(self.Xi, self.Yi, color=self.distcolor, alpha=self.alpha, clip_on=False)  
        if TYPE == 'POLY': 
            Yp = [self.yi+(y*100) for y in stats.norm.pdf(self.Xi, self.xm+self.xm*0.13, 2.6)]  
            ax.fill(self.Xi, Yp, color='grey', alpha=1, zorder=10,clip_on=False)  
        elif TYPE == 'NOVO': 
            Yp = [self.yi+(y*182) for y in stats.norm.pdf(self.Xi, self.xm, 5.8)]  
            #ax.plot(self.Xi, Yp, clip_on=False) 
            ax.fill(self.Xi, Yp, color='red', alpha=1, zorder=10,clip_on=False)  
        else: 
            Yp = [self.yi+(y*85) for y in stats.norm.pdf(self.Xi, self.xm, 5)]  
            ax.fill(self.Xi, Yp, color='purple', alpha=1, zorder=10,clip_on=False)  
            Yp = [self.yi+(y*50) for y in stats.norm.pdf(self.Xi, self.xm+self.xm*0.53, 1.3)]  
            ax.fill(self.Xi, Yp, color='purple', alpha=1, zorder=10,clip_on=False)  



    def make_fake_sibs(self, ax, fs1=6.5, fs2=6, fs3 = 5, TYPE='POLY'): 
       
        Yf = self.Yn
        ax.set_ylim(-0.5,45)
        if TYPE == 'POLY':
            xj = 60 
            ax.set_xlim(-33,37.5) 
            ax.plot([-34,185],[0.1,0.1],color='k', lw=1,zorder=5,clip_on=False)
        else:
            xj = 60 
            ax.set_xlim(-33,37.5)  

        ax.plot(self.Xn[xj::], Yf[xj::], color=self.distcolor, linewidth=1, zorder=5)# clip_on=False) 
        ax.fill(self.Xn[xj::], Yf[xj::], color=self.distcolor, alpha=self.alpha)#, clip_on=False) 
        ax.axis('off') 
        self.add_inset(ax, TYPE)        
        y,sz = 4, 1.45
        xp,xs = 25.5,1.8 
        h1, h2 = 1.3, 3.5 
        for x,y in [[xp,h2],[xp+xs,h1],[xp+xs*2,h2],[xp+xs*3,h1],[xp+xs*4,h2],[xp+xs*5,h1]]: 
            self.make_human(x, y, ax, s=sz,c = 'k')  
        if TYPE=='POLY': 
            for x2,y2 in [[7,1.8],[9.6,3.2],[5.5,6.5],[8.5,8.0],[6.5,12],[9,14]]: 
                ax.plot([xp,x2+0.5],[1.5,y2],linestyle='--', color='k', lw=0.75,zorder=1) 
                self.make_human(x2, y2, ax, s=sz,c = 'grey')  
        elif TYPE=='NOVO': 
            for x2,y2 in [[-20,2],[-4,3.5],[-11,7],[2,7],[-1.5,11.5],[12,10.5]]: 
                ax.plot([xp,x2+0.5],[1.5,y2],linestyle='--', color='k', lw=0.75,zorder=1) 
                self.make_human(x2, y2, ax, s=sz,c = 'red')  
        elif TYPE=='MEND': 
            for x,y in [[xp-2,6],[xp+1.8,6],[xp+6,6]]: 
                self.make_human(x, y, ax, s=sz,c = 'purple')  
                ax.plot([xp,xp-2.5],[1.5,5],linestyle='--', color='k', lw=0.75,zorder=1) 
            for x2,y2 in [[-17,3],[-5,5.5],[4,7.5]]: 
                ax.plot([xp,x2+1],[1.5,y2],linestyle='--', color='k', lw=0.75,zorder=1) 
                self.make_human(x2, y2, ax, s=sz,c = 'purple')  

        ax.text(32.25,-0.35, '(Top 1%)', fontsize=fs3, ha='center', va='top') 
        tx,ty = 0, 14 
        if TYPE=='POLY': 
            ax.text(-2,-0.5, 'Common-Variant\nTail Architecture', fontsize=fs1, ha='center', va='top') 
            txt1 = 'Sibs\nRegress\nTo Mean' 
            self.make_arrow(ax, a = (tx,ty), b = (4,10), FLIP=True) 
            self.make_arrow(ax, a = (tx,ty+7.5), b = (13,34),txt=txt1) 
        elif TYPE=='NOVO': 
            ax.text(0,-0.8, '$De$ $Novo$\nTail Architecture', fontsize=fs1, ha='center', va='top') 
            txt1 = 'Sibs\nNormally\nDistributed' 
            #self.make_arrow(ax, a = (tx,ty), b = (1,14), txt = txt1,FLIP=True) 
            self.make_arrow(ax, a = (tx,ty+7.5), b = (13,34), txt=txt1) 
        elif TYPE == 'MEND': 
            ax.text(0,-0.8, 'Mendelian-like\nTail Architecture', fontsize=fs1, ha='center', va='top') 
            txt1 = 'Sibs\nBimodally\nDistributed' 
            self.make_arrow(ax, a = (tx,ty), b = (-4,11), FLIP=True) 
            self.make_arrow(ax, a = (tx+3,ty), b = (25,10)) 
            self.make_arrow(ax, a = (tx,ty+7.5), b = (13,34), txt=txt1) 
        return







class SibExtra:
    def __init__(self, size, indexMean, loc): 
        self.size, self.indexMean, self.loc = size, indexMean, loc 







class MyFigure:
    def __init__(self, options, traits, progress, figName=None):         
        self.options, self.data, self.traits, self.figName = options, traits, self.extract_sib_traits(traits.members),figName
        self.progress = progress.update(self) 
    
        self.colors = ['red','green','blue','purple','orange','lime'] 
        self.fs0, self.fs1, self.fs2, self.fs3, self.fs4 = 10, 7, 6, 5, 5 
        self.sz1, self.sz2, self.sz3 = 15,10,8

        self.lib = FigLib(options) 
        self.b_color = 'xkcd:light grey' 

    def extract_sib_traits(self, M): 
        X = {} 
        for ti,T in M.items(): 
            if 'sib' not in T.vals: continue 
            X[ti] = T 
        return X 
        


    def draw(self): 
        self.setup() 
        self.create() 
        self.finish() 


    def load_sib_extra(self, F): 
        
        self.SE = dd(lambda: {}) 
        with open(F) as f: 
            header = f.readline().split(',')
            for line in f: 
                line = line.strip().split(',') 
                ti, tsize, indexMean, test, loc = int(line[0]) , int(line[2]), float(line[3]), line[4], line[5] 
                if loc not in self.SE[ti]: self.SE[ti][loc] = SibExtra(tsize, indexMean, loc) 
                self.SE[ti][loc].add_test(test, line[6::])  


    def draw_sib_schematic(self, axes): 
        ax1, ax2, ax3 = axes 
        self.lib.make_fake_sibs(ax1, TYPE='POLY') 
        self.lib.make_fake_sibs(ax2, TYPE='NOVO') 
        self.lib.make_fake_sibs(ax3, TYPE='MEND') 





    # SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP SETUP #
    def setup(self): 
        self.fig, self.axes = matplotlib.pyplot.gcf(), [] 
        self.rows, self.cols, self.WD, self.HT = 60,73, 38,27
        self.WD, self.HT = 36,25
        
        self.WD, self.HT = 7.1,5 

        rs = 22
        cs1, cs2, cs3 = 12, 17, 24 
        cz3 = 13
        self.axes.append(plt.subplot2grid((self.rows,self.cols), (0,1), rowspan = rs+2, colspan =cz3))                                                                   
        self.axes.append(plt.subplot2grid((self.rows,self.cols), (0,1+cz3), rowspan = rs+2, colspan =cz3))                                                                   
        self.axes.append(plt.subplot2grid((self.rows,self.cols), (0,1+2*cz3), rowspan = rs+2, colspan =cz3))                                                                   
        cx = cz3*3+8
        cs1, rs = 12,15
        self.axes.append(plt.subplot2grid((self.rows,self.cols), (0,cx), rowspan = rs, colspan =cs1))                                                                   
        self.axes.append(plt.subplot2grid((self.rows,self.cols), (0,cx+cs1), rowspan = rs, colspan =cs1))                                                                   
        self.axes.append(plt.subplot2grid((self.rows,self.cols), (rs,cx), rowspan = rs, colspan =cs1))                                                                   
        self.axes.append(plt.subplot2grid((self.rows,self.cols), (rs,cx+cs1), rowspan = rs, colspan =cs1))                                                                   
        rz = 30 
        self.axes.append(plt.subplot2grid((self.rows,self.cols), (rs+15,2), rowspan = rz-1, colspan =(cz3*3)-1))                                                               
        self.axes.append(plt.subplot2grid((self.rows,self.cols), (rs*2+5,cx), rowspan = rs+9, colspan =cs1*2))                                                                   
        self.fig.set_size_inches(self.WD, self.HT)                                                                                                                                  
        self.ax_index, self.xLoc, self.fq1, self.fq2 = 0, 1, 24, 22                


    def finish(self):

        # P-value
        #plt.subplots_adjust(left=0.01, bottom=0.045, right=1.01, top=0.95,wspace=0.5, hspace=0.5) 
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
        return
        if self.figName is not None: figPath = self.options.out+self.figName+'.pdf' 
        else:                        figPath = self.options.out+'Fig3.pdf' 
        plt.savefig(figPath, dpi=self.options.dpi) 
        plt.clf() 
        self.progress.save('(Figure Saved: '+figPath+')')
        return




    def create(self): 
        self.draw_sib_schematic(self.axes[0:3]) 
        self.ax_index = 3 
        for i,ti in enumerate(self.options.indexTraits): sp = SP.SibPlot(self.axes[self.ax_index+i], self, ti).draw_sib_pair(i, LABEL=True) 
        self.add_h2_coord(self.axes[8]) 
        self.add_sib_pairs(self.axes[7]) 
        return 
        






    def add_h2_coord(self, ax, fs1 = 30, fs2 = 24, fs3 = 14): 
        T, X, Y, sk, rule = [], [], [], dd(list) , 'h2'  
        for t in self.traits.values(): 
            T.append(t)
            X.append(vars(t.qc['misc'])[rule])
            Y.append(t.vals['sib'].h2)   
            ax.scatter(X[-1],Y[-1], color=t.group_color, ec='k', s = self.sz2, lw=0.3, zorder=1) 
        lw, ms, sb, D,F,C = 0.5, 1, 0, 'data', 'fancy','black'                                                                                                                                             
        astr = "fancy,head_width=2.5,head_length=2.5,tail_width=0.01"                                                                                                                               
        for t,x,y in zip(T,X,Y): 
            fn = t.name.box 
            if t.ti in [845]: ax.text(x-0.03,y-0.03,fn, ha='left',va='center',fontsize = self.fs3, zorder=3, fontweight='bold') 
            elif t.ti in [20022]: ax.text(x,y+0.02,fn, ha='left',va='bottom',fontsize = self.fs3, zorder=3, fontweight='bold') 
            elif t.ti in [20015]: ax.text(x+0.005,y+0.022,'Sitting\nHeight', ha='center',va='bottom',fontsize = self.fs3, zorder=3, fontweight='bold') 
            elif t.ti in [50]: ax.text(x,y+0.02,fn, ha='right',va='bottom',fontsize = self.fs3, zorder=3, fontweight='bold') 
            elif t.ti in [30070]: 
                ax.text(x+0.0045,y-0.002,fn, ha='left',va='top',fontsize = self.fs2, zorder=3, fontweight='bold')  
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



        




    def scatter_sib(self, x, y, i, T): 
        fn = T.name.mini
        if i == 0: 
            self.ax.scatter(x,y, marker = '^', s = self.sz1, zorder=2,alpha=0.99,color = T.group_color, edgecolor ='k',lw=0.2)
            if T.ti in [30070]:  self.ax.text(x-1, y-0.25, fn, ha='left', va='top', color='k',fontweight='bold', fontsize=self.fs2) 
            elif T.ti in [20015]:       self.ax.text(x-2, y+0.5, fn, ha='left', va='top', color='k',fontweight='bold', fontsize=self.fs2) 
            elif T.ti in [845]:         self.ax.text(x-5, y+0.5, fn, ha='left', va='top', color='k',fontweight='bold', fontsize=self.fs2) 
        else: 
            self.ax.scatter(x,y, marker = 'v', s = self.sz1, zorder=2,alpha=0.99,color = T.group_color, edgecolor ='k',lw=0.2)
            if T.ti in [30040]: self.ax.text(x, y+0.25,'Mean\nCorpuscular\nVol' , ha='right', va='bottom', color='k',fontweight='bold', fontsize=self.fs2) 
            elif T.ti in [20015]:  self.ax.text(x+0.25, y+0.42, fn, ha='left', va='top', color='k',fontweight='bold', fontsize=self.fs2) 
            elif T.ti in [30020]: self.ax.text(x, y+0.5, "\n".join(fn.split()), ha='center', va='center', color='k',fontweight='bold', fontsize=self.fs3) 
        return 


    def get_meta_p(self, p_denovo, p_mend): 
        eps = 1e-300
        p_mend = max(min(p_mend, 1.0), eps)
        p_denovo = max(min(p_denovo, 1.0), eps)
        stat = -2.0 * (math.log(p_mend) + math.log(p_denovo))  # ~ chi2(df=4) under null
        meta_p = stats.chi2.sf(stat, df=4)  # survival function = 1 - CDF, numerically stable
        return meta_p
        

    def add_sib_pairs(self, ax): 
        self.ax, X,Y,cnt = ax, [],[],0 
        for ti,T in self.traits.items(): 
            cnt += 1 
            p1, p2  =  [-math.log(T.vals['pop']['common-snp'].key[k],10) for k in ['p1','p2']]
            sd = T.vals['sib'].key 
            d1,d2 = [T.vals['sib'].key[k] for k in ['novo1','novo2']] 
            m1,m2 = [T.vals['sib'].key[k] for k in ['mend1','mend2']]
            b1,b2 = [T.vals['sib'].key[k] for k in ['meta1','meta2']]
            meta1, meta2 = -math.log(self.get_meta_p(d1,m1),10), -math.log(self.get_meta_p(d2,m2),10)
            for i,(x,y) in enumerate([[p2,meta2],[p1,meta1]]):  
                self.scatter_sib(x, y, i, T) 
                X.append(x) 
                Y.append(y) 
                

        xLab, yLab = '$POPout$ $P$-value ($-log_{10}P$)', '$STANDout$ $P$-value ($-log_{10}P$)'
        lms = DV.AxLims(self.ax,xlab=xLab,ylab=yLab,xLim=[min(X)-3,max(X)+5],yLim=[min(Y)-0.5,max(Y)+1],fs = self.fs2,COMMANDS=['nospines']) 
        R, pv = DV.add_scatter_corr(ax,X,Y, fs=7, INTERCEPT=False) 
        self.progress.report_result('POPout/Standout Correlation: '+str(round(R,3))+', pv='+str(pv)) 
        x1, y1 = lms.xMax - lms.xStep * 3.6, lms.yMin + lms.yStep * 2 
        for i,(g,c) in enumerate(zip(self.data.group_names, self.data.group_colors)): 
            ax.scatter(x1,y1-lms.yHop*3.6*i,marker='s',color=c,s=self.sz1,ec='k', lw=0.5) 
            ax.text(x1+lms.xHop,y1-lms.yHop*3.6*i,g, fontsize=self.fs1,ha='left',va='center') 
        return










