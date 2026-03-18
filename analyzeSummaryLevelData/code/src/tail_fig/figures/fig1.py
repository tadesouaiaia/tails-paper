import sys, os                                                                                                                                                                                                                                                                               
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path: sys.path.insert(0, HERE)

from util.Util   import *
from util import drawScatter as DS
from util import drawVarious as DV
from util import drawLabels  as DL
np.random.seed(43)  

# Common
# Quantiles
# Trait
# Sibling
# Tail
# Cause



class FigLib: 
    def __init__(self, options, AK={}):
        self.options = options
        self.fs1, self.fs2, self.fs3,self.fs4,self.fs5 = 12,10,8,7,5
        self.sz1, self.sz2,self.sz3 = 15,9,8
        self.lw1, self.lw2, self.lw3 = 1, 0.8,0.5


    def make_square(self,ax,x1,x2,y1,y2,lw=1,ls='--',ap=0.3,color='k'):
        ax.plot([x1,x2],[y1,y1],clip_on=False,color=color,lw=lw,linestyle=ls,alpha=ap)
        ax.plot([x1,x2],[y2,y2],clip_on=False,color=color,lw=lw,linestyle=ls,alpha=ap)
        ax.plot([x1,x1],[y1,y2],clip_on=False,color=color,lw=lw,linestyle=ls,alpha=ap)
        ax.plot([x2,x2],[y1,y2],clip_on=False,color=color,lw=lw,linestyle=ls,alpha=ap)
    

    def make_dots(self, ax, x, YR, y_var = 1, c='red', stepsize=0.25, MAX=5):
        y1, y2, y3, y4 = YR 
        MS = MAX*MAX
        for i,(a,b) in enumerate([[y1,y2],[y3,y4]]): 
            while a <= b: 
                yp = a + np.random.normal(0,y_var*0.02)     
                a+= stepsize 
                if yp*yp > MS: continue
                elif yp > y2 and yp < y3: continue 
                else: 
                    xp = max(x + np.random.normal(0,0.05),-3.02)    
                    sz = self.sz2 
                    
                    if xp < -1.5: ax.scatter(xp,yp, s=sz,alpha=0.65,color=c,lw=0.001,ec='red',clip_on=False) 
                    else:         ax.scatter(xp,yp, s=sz,alpha=0.65,color='grey',lw=0.001,ec='grey',clip_on=False) 
                    


    #def draw_one_human(self, xp, yp, ax, s = 2, bc='k', c = 'red', rc2 = 'lime', risk1=0, risk2=0):
    def make_human(self, xp, yp, ax, s = 2, bc='k', c = 'red', rc2 = 'lime', risk1=0, risk2=0):
        #c = 'cyan'    
        #c = bc 
        head = matplotlib.patches.Circle((xp + s/4.0, yp+ s), s/2.5, facecolor=c, zorder=10,clip_on=False)
        #left_arm = mpatches.Rectangle((xp+s*0.1, yp+ s*0.6), s*0.2, s, angle=120, facecolor=c,zorder=10)
        #right_arm = mpatches.Rectangle((xp+s/2.0, yp+ s*0.7), s*0.2, s, angle=-120, facecolor=c,zorder=10)
        left_arm = matplotlib.patches.Rectangle((xp+s*0.1, yp+ s*0.6), s*0.2, s*0.95, angle=135, facecolor=c,zorder=10,clip_on=False)
        right_arm = matplotlib.patches.Rectangle((xp+s*0.55, yp+ s*0.7), s*0.2, s*0.95, angle=-135, facecolor=c,zorder=10,clip_on=False)
        body = matplotlib.patches.Rectangle((xp, yp), s/2.0, s, facecolor=c, zorder=10,clip_on=False)
        left_leg = matplotlib.patches.Rectangle((xp+s*0.25, yp+s*0.10), s*0.25, s, angle=150,facecolor=c,zorder=10,clip_on=False)
        right_leg = matplotlib.patches.Rectangle((xp+s*0.50, yp+s*0.20), s*0.25, s, angle=-150,facecolor=c,zorder=10,clip_on=False)
        ax.add_patch(head)
        ax.add_patch(body)
        ax.add_patch(left_arm)
        ax.add_patch(right_arm)
        ax.add_patch(left_leg)
        ax.add_patch(right_leg)


    def make_arrow(self, ax, a = (0,8), b = (-8,3), FLIP=False, txt='NA', STYLE='NA', SHIFT=False):  

        # Define arrow properties
        if STYLE in ['PEND']: arrowstyle = "Simple, tail_width=0.3, head_width=3, head_length=3"
        else:                 arrowstyle = "Simple, tail_width=0.5, head_width=3, head_length=3"
        
        if FLIP: connectionstyle = "arc3,rad=.125"  # Adjust the curvature with 'rad'
        else:    connectionstyle = "arc3,rad=-.125"  # Adjust the curvature with 'rad'



        arrow_properties = {"arrowstyle": arrowstyle,"color": "k",}

        # Define arrow start and end points
        tail_position = a 
        head_position = b 

        # Create the arrow
        arrow = matplotlib.patches.FancyArrowPatch(tail_position, head_position, linewidth=0.5, connectionstyle=connectionstyle, **arrow_properties)
        # Add the arrow to the plot
        ax.add_patch(arrow)
        if txt != 'NA': 
            if SHIFT: ax.text(a[0]+2,a[1]+1,txt,ha='center',va='bottom',fontsize=self.fs4-1, fontweight='bold',zorder=999) 
            else: ax.text(a[0],a[1]+1,txt,ha='center',va='bottom',fontsize=self.fs4, zorder=999) 


    def arrow_axes(self, ax, x_info, y_info): 

        y1, y2, yl, YL = y_info  
        x1, x2, xl, XL = x_info 
        ax.arrow(x1, y1, x2-x1, 0,  linewidth=self.lw2,  head_width=0.15, head_length=5, fc='k', ec='k',clip_on=False,zorder=0)
        ax.set_xlabel(xl,fontsize=self.fs3,labelpad=1) 
        ax.arrow(x1, y1, 0, y2-y1-0.4,  linewidth=self.lw2,  head_width=3.3, head_length=0.25, fc='k', ec='k',clip_on=False,zorder=0)
        ax.set_ylabel(yl,fontsize=self.fs3) 






class MyFigure:
    def __init__(self, options, traits, progress, figName=None):
        self.options, self.progress, self.lib, self.fig = options, progress, FigLib(options), matplotlib.pyplot.gcf() 
        self.common_color, self.rare_color = 'xkcd:ultramarine blue', 'xkcd:neon blue' 
        self.figName = figName
        self.fs1, self.fs2, self.fs3, self.fs4, self.fs5,self.fs6 = 11,9,8,7,6,5
        self.sz1, self.sz2, self.sz3 = 20, 15, 10 
        self.lw1, self.lw2, self.lw3 = 1, 0.8,0.5


    def draw(self):  
        self.setup() 
        self.create() 
        self.finish() 


    def setup(self): 

        self.fig, self.axes = matplotlib.pyplot.gcf(), [] 
        jj = 7
        cs1 = 10 
        cs2 = 13
        r1 = 0 
        self.rows, self.cols, RS, RS2, RZ, self.WD, self.HT = 28,24, 8, 16, 5, 43,47                                                            
        
        self.WD, self.HT = 50, 24.7 
        self.WD, self.HT = 7.1, 4.2 
        self.rows = 13 
        self.cols = 50 
        for c in [0,26]: 
            self.axes.append(plt.subplot2grid((self.rows,self.cols), (r1,c), rowspan =5, colspan =cs1))                                                             
            self.axes.append(plt.subplot2grid((self.rows,self.cols), (r1+jj,c), rowspan =5, colspan =cs1))                                                             
            self.axes.append(plt.subplot2grid((self.rows,self.cols), (r1,c+11), rowspan =5, colspan =cs2))                                                             
            self.axes.append(plt.subplot2grid((self.rows,self.cols), (r1+jj,c+11), rowspan =5, colspan =cs2))                                                             
        self.fig.set_size_inches(self.WD, self.HT) 
        self.ax_index, self.xLoc, self.fq1, self.fq2 = 0, 1, 24, 22 
        return 

        


        self.axes.append(plt.subplot2grid((self.rows,self.cols), (r1,0), rowspan =5, colspan =cs1)) 
        self.axes.append(plt.subplot2grid((self.rows,self.cols), (r1+jj,0), rowspan =5, colspan =cs1)) 
        self.axes.append(plt.subplot2grid((self.rows,self.cols), (r1,11), rowspan =5, colspan =cs2))                                                             
        self.axes.append(plt.subplot2grid((self.rows,self.cols), (r1+jj,11), rowspan =5, colspan =cs2))                                                             
        r2 = 16
         


        self.axes.append(plt.subplot2grid((self.rows,self.cols), (r2,0), rowspan =5, colspan =cs1))                                                             
        self.axes.append(plt.subplot2grid((self.rows,self.cols), (r2+jj,0), rowspan =5, colspan =cs1))                                                             
        self.axes.append(plt.subplot2grid((self.rows,self.cols), (r2,11), rowspan =5, colspan =cs2))                                                             
        self.axes.append(plt.subplot2grid((self.rows,self.cols), (r2+jj,11), rowspan =5, colspan =cs2))                                                             
        self.fig.set_size_inches(self.WD, self.HT) 
        self.ax_index, self.xLoc, self.fq1, self.fq2 = 0, 1, 24, 22 


    def finish(self):
        plt.subplots_adjust(left=0.04, bottom=0.005, right=0.999, top=0.88,wspace=0.6, hspace=0.02) 
        if self.figName is not None: figPath = self.options.out+self.figName+'.pdf'
        else:                        figPath = self.options.out+'Fig1.pdf'
        plt.savefig(figPath, dpi=self.options.dpi)
        plt.clf()
        self.progress.save('(Figure Saved: '+figPath+')')





   


    
    
    def create(self): 
        self.nullMP = 1300 
        self.nullVar = 22 
        self.nullVar = 23 
        self.selVar  = 12.2 
        self.selVar  = 12.7 
        self.selVar  = 13 
        self.selMP   = 900 
        
        self.Xn = np.arange(0,100,0.05)
        self.Yn = [(y*self.nullMP) for y in stats.norm.pdf(self.Xn, 50, self.nullVar)]
        self.Ys = [(y*self.selMP) for y in stats.norm.pdf(self.Xn, 50, self.selVar)]

        self.Ys =  [y - min(self.Ys) for y in self.Ys] 
        self.Yn =  [y - min(self.Yn) for y in self.Yn] 
        # set colors # 
        self.c1 = 'blue' 
        self.c2 = 'red' 
        self.distcolor = 'xkcd:burnt yellow' 
        self.alpha=0.39
        # 
        self.make_fake_trumpet(self.axes[0], NOGO=False, PLOTZONES=False,NULL=True) 
        self.make_fake_popout(self.axes[1],NULL=True) 
        self.make_fake_variant_dist(self.axes[2],NULL=True) 
        self.make_fake_sibs(self.axes[3],NULL=True) 
        self.make_fake_trumpet(self.axes[4], NOGO=False, PLOTZONES=False) 
        self.make_fake_popout(self.axes[5]) 
        self.make_fake_variant_dist(self.axes[6]) 
        self.make_fake_sibs(self.axes[7]) 
        # ADD LABELS # 
        letters = ['$a$','$c$','$b$','$d$','$e$','$g$','$f$','$h$'] 
        for i,ax in enumerate(self.axes):
            x1,x2 = ax.get_xlim() 
            y1,y2 = ax.get_ylim() 
            xs = (x2-x1)/20.0
            ys = (y2-y1)/20.0
           
            if i in [0,4]: 
                x1-=xs*0.5 
            elif i in [1,5]: 
                x1-=xs*0.5
                y2+=ys*0.5
            else: 
                x1+=xs*1.2
                if i in [3,7]: 
                    y2+=ys*0.5

            ax.text(x1-xs*1.5,y2,letters[i],fontsize=17,clip_on=False) 
            if i == 1: 
                a1,a2 = x1-xs*2.7, x2 + xs*29.5
                b1,b2 = y2+ys*31.25, y1-ys*2.8 
                self.lib.make_square(ax,a1,a2,b1,b2,color='k') 
                ax.text(x2+2.65*xs,b1+ys*0.4,'Polygenic Model + No Selection',ha='center',va='bottom',fontsize=self.fs1,clip_on=False) 
            elif i == 5:  
                a1,a2 = x1-xs*2.5, x2 + xs*28.5
                b1,b2 = y2+ys*31.25, y1-ys*2.8 
                self.lib.make_square(ax,a1,a2,b1,b2,color='k') 
                ax.text(x2+2.65*xs,b1+ys*0.1,'Polygenic Model + Strong Selection',ha='center',va='bottom',fontsize=self.fs1,clip_on=False) 
                
                










    def make_fake_trumpet(self, ax,NOGO=False, PLOTZONES=False, NULL=False): 
        X  = [x for x in np.arange(-3,2.5, 0.1)]
        X2 = [x for x in np.arange(-3,2.5, 0.05)]
        # CREATE ZONES # 
        
        Y_N = [0.6 + 0.1*np.exp(-x*1.1) for x in X2][0:len(X)]
        Y_T = [0 + 0.1*np.exp(-x*1.1) for x in X]

        Y_NN = [-1*y for y in Y_N] 
        Y_TN = [-1*y for y in Y_T] 
        

        if NULL: YP = [0.6 + 0.1*np.exp(-x*1.1) for x in X2][0:len(X)]
        else:    YP = [0 + 0.1*np.exp(-x*1.1) for x in X]
        
        
        YN = [-1*y for y in YP] 
        for i,x in enumerate(X): 

            if i < 15: clr = 'red' 
            else:      clr = 'grey' 
            
            n_pts = [Y_NN[i], 0, 0, Y_N[i]]
            t_pts = [Y_TN[i], 0, 0, Y_T[i]]

            pts = [YN[i], 0, 0, YP[i]] 
            

            if NULL:     
                SD, ss, mm = 5, 0.3, 3.2
                self.lib.make_dots(ax, x, t_pts, c = clr, y_var = 10,stepsize=ss,MAX=5.5) 
                self.lib.make_dots(ax, x, n_pts, c = clr, y_var = 45,stepsize=0.5,MAX=4) 
                
                #self.lib.make_dots(ax, x, n_pts, c = clr, y_var = 50,stepsize=1,MAX=3.5) 
                #self.lib.make_dots(ax, x, pts, c = clr, y_var = 40,stepsize=0.8,MAX=3.5) 
            else: 
                SD = 2*(100-i)/100 
                if i < 1: ss, SD = 0.05, 50 
                elif i < 10:  ss = 0.19 
                elif i < 20:  ss = 0.13
                elif i < 30:  ss = 0.07
                else:         ss = 0.04
                if i < 15:   self.lib.make_dots(ax, x, pts, c = clr, y_var = SD,stepsize=ss*2,MAX=3.5) 
                else:        self.lib.make_dots(ax, x, pts, c = clr, y_var = SD,stepsize=ss*2,MAX=3.5) 
        if NULL: self.lib.make_dots(ax,-3.5, [-4,0,0,4], y_var = 5, c = 'red', stepsize = 0.8, MAX = 4.5) 
        else:    self.lib.make_dots(ax,-3.6, [-5,0,0,5], y_var = 5, c = 'red', stepsize = 0.5, MAX = 4.75) 
        ax.spines[['top','right','left']].set_visible(False)          
        ax.set_xticks([]) 
        ax.set_yticks([-4,-2,0,2,4]) 
        ax.set_ylim(-5,5)  
        ax.set_xlim(-3.11,2.5) 
        ax.set_xlabel('Allele Frequency',fontsize=self.fs3,labelpad=0) 
        ax.set_ylabel('Effect Size',fontsize=self.fs3-0.5, labelpad=-2.75) 

        ax.plot([-3.1,-3.1],[-5,5], color='k',lw=self.lw2, clip_on=False)  
        ax.arrow(-3.1, -5, 5.5, 0,  linewidth=self.lw2,  head_width=0.4, head_length=0.2, fc='k', ec='k',clip_on=False,zorder=0)
        # Heritability 
        x1,x2, y1, y2 = -2.4, -0.2, -4.6, 1.7
        for i,(x,c,txt) in enumerate(zip([x1,x2],['red','grey'],['Rare Alleles','Common Alleles'])): 
            ax.scatter(x,y1, marker='o',ec='k',color=c,clip_on=False,s=self.sz2)
            ax.text(x+0.13,y1-0.1, txt, va='center',ha='left',fontsize=self.fs6,clip_on=False)
        return


        










    def make_fake_variant_dist(self, ax,NULL=False): 
        # CREATE CURVES 
        X = [x for x in range(100)]
        Y_NULL = [random.random()*random.random() for x in X]
        Y_SELECT_1 = [random.random()-0.5 + (random.random()/4.0+max((abs(x-49.5)-30)/2.0,0))**1.65 for x in X]
        # ADD HUMANS # 
        if NULL: 
            ax.plot(X,[8+y for y in Y_NULL], color='grey', lw=self.lw1, alpha=1.0,zorder=10)
            ax.plot(X,[3+y for y in Y_NULL], color='red', lw=self.lw1, alpha=1.0,zorder=10)
            Yf = self.Yn 
            for x in [2,15,25,32,39,45,50,55,61,68,75,85,97]: self.lib.make_human(x, -2.6, ax, s = 1.6, c = 'black') 
        else:    
            ax.plot(X[8:92],[5.5+y for y in Y_NULL[8:92]], color='grey', lw=self.lw1, alpha=1.0,zorder=10)
            ax.plot(X[10:90],[3+y for y in Y_SELECT_1[10:90]], color='red', lw=self.lw1, alpha=1.0,zorder=10) 
            Yf = self.Ys 
            for x in [14,26,34,41,46,50,54,59,66,73,85]:  self.lib.make_human(x, -2.6, ax, s = 1.6, c = 'black') 

        ax.plot(self.Xn, Yf, color=self.distcolor, linewidth=0.5, clip_on=False,zorder=8) 
        ax.fill(self.Xn, Yf,color=self.distcolor,clip_on=False, alpha=self.alpha) 
        
        # ADD LABELS # 
        #names = ['Lower Tail', 'Average', 'Upper Tail'] 
        y0,y1,y2 = -5.5,-12,-7.5
        ax.arrow(20, y0, -7, 0,  linewidth=self.lw3,  head_width=1.1, head_length=1.3, fc='k', ec='k',clip_on=False,zorder=0)
        ax.arrow(80, y0,  7, 0,  linewidth=self.lw3,  head_width=1.1, head_length=1.3, fc='k', ec='k',clip_on=False,zorder=0)
        ax.text(50, y0, 'Trait Distribution', ha='center', va='center', fontsize = self.fs4)




        ax.plot([-2,101],[-0.12,-0.12], color='k',lw=self.lw2)
        ax.plot([-2,101],[-3.95,-3.95],lw=self.lw3,color='k') 


        ax.arrow(-2, 0,  0, 24,  linewidth=self.lw2,  head_width=1.5, head_length=1.3, fc='k', ec='k',clip_on=False,zorder=0)
        ax.text(-9.5,12,'Heritability',fontsize=self.fs3,rotation=90,ha='left',va='center') 
        ax.set_xlim(-9,109)
        ax.set_ylim(-4,27)
        ax.axis('off') 
        
        
        if NULL: x1,x2, y1, y2 = 75, 90, 30, 27.5
        else:    x1,x2, y1, y2 = 75, 90, 31, 28.5
        for i,(y,c,txt) in enumerate(zip([y1,y2],['grey','red'],['Common Alleles','Rare Alleles'])): 
            ax.plot([x1-15,x1-10],[y,y], color=c,clip_on=False,lw=self.lw2)
            ax.text(x1-9,y-0.1, txt, va='center',ha='left',fontsize=self.fs6,clip_on=False)
        return








    
    def make_fake_popout(self, ax, fs1 = 29, fs2= 25, c1 = 'blue', c2 = 'gray',NULL=False):
        X = [x for x in range(100)] 
        Xe = [stats.norm.ppf((x+0.5)/100.0) for x in X] 
        # Plot Expectation # 
        ax.plot(X,Xe, color='darkorange',lw=self.lw3,zorder=1) 
        ax.scatter(X[0],Xe[0],marker='v',color='darkorange',s=self.sz2,zorder=1) 
        ax.scatter(X[-1],Xe[-1],marker='^',color='darkorange',s=self.sz2,zorder=1) 
        Xobs = [x+np.random.normal(0,0.020) for x in Xe] 
        if not NULL:  
            for i,p in enumerate([1.6,0.9,0.55,0.3,0.2,0.1,0.05]): 
                Xobs[i] += p 
                Xobs[-1*(i+1)] -= p 
            for i,loc in enumerate([0,-1]): 
                
                x,y1,y2 = X[loc], Xobs[loc], Xe[loc] 
                
                if i == 0: x -= 5 
                else:      x += 5 
                ax.plot([x,x],[y1,y2],color='dimgrey', linestyle='--', lw=self.lw2) 
                ax.plot([x-1,x+1],[y2,y2],color='dimgrey', lw=self.lw2) 
                ax.plot([x-1,x+1],[y1,y1],color='dimgrey', lw=self.lw2) 
            
            #self.lib.make_arrow(ax, a = (99,-0.1), b = (103,0.8),FLIP=True, STYLE='PEND') 
            self.lib.make_arrow(ax, a = (90,-0.4), b = (100,0.75),FLIP=True, STYLE='PEND') 
            #ax.text(91,-0.7,'Rare Alleles in Tail\nReduce Common\nPolygenic Signal', fontsize=self.fs5,ha='center',va='center')  
            ax.text(77,-1.2,'Rare Alleles in Tail\nReduce Common\nPolygenic Signal', fontsize=self.fs5,ha='center',va='center',fontweight='bold')  

        ax.scatter(X, Xobs, color='blue', s = self.sz2, ec='k', alpha=0.9, lw=0.1) 
        ax.spines[['top','right']].set_visible(False) 
        xa,xb = -10,110
        ax.set_xlim(xa,xb) 
        ax.set_ylim(-2.9,2.9) 
        ax.set_xticks([]) 
        ax.set_yticks([]) 
        self.lib.arrow_axes(ax, [xa,xb,'Trait Quantiles',True],[-2.9,2.9,'Polygenic Score',True])  

        x1,x2, y1, y2 = -2, 90, 2.5, 2
        for i,(y,c,txt) in enumerate(zip([y1,y2],['darkorange','blue'],['Expected','Observed'])): 
            if i == 0: ax.plot([x1-2.5,x1+1.5],[y,y], color=c,clip_on=False,lw=self.lw2)
            else:      ax.scatter(x1,y+0.02, color=c, s = self.sz1) 
            ax.text(x1+3,y, txt, va='center',ha='left',fontsize=self.fs4,clip_on=False)
        return











    def make_fake_sibs(self, ax, fs1=29, fs2=25, rc = 'red', NULL=False): 
       
        ax.set_xlim(-9,109)
        ax.set_ylim(-0.5,30)
        
        
        if NULL: Yf = self.Yn 
        else:    Yf = self.Ys 
        
        ax.plot(self.Xn, Yf, color=self.distcolor, linewidth=0.5, clip_on=False,zorder=8) 
        ax.fill(self.Xn, Yf, color=self.distcolor, linewidth= 2, zorder=0, alpha=self.alpha,clip_on=False) 
        ax.set_xticks([]) 
        ax.set_yticks([]) 
        ax.axis('off') 
        self.sib_color = 'dimgrey'
        ## DRAW SOME POLYGENIC SIBS ## 
        #for x,y in [[-5,1],[-3,3],[-1,1],[1,3],[3,1]]: 
        y,sz = 4, 1.5 
        for x,y in [[-3,1],[-1,3],[1,1],[3,3]]: 
            if NULL: 
                self.lib.make_human(x+1, y, ax, s=sz,c = self.sib_color)  
                self.lib.make_human((99-x)-1, y, ax, s=sz,c = self.sib_color)  
                #for x2,y2 in [[24,1.5],[20,3],[27,6],[24,8]]: 
            else: 
                self.lib.make_human(x+12, y, ax, s=sz,c = self.sib_color)  
                self.lib.make_human((99-x)-12, y, ax, s=sz,c = self.sib_color)  

        if NULL:
            for x2,y2 in [[25,1.25],[21,3],[28,6],[25,8]]: 
                ax.plot([4,x2-0.5],[1.1,y2],linestyle='--', color='k', lw=self.lw3,zorder=5) 
                self.lib.make_human(x2, y2, ax, s=sz,c = self.sib_color)  
            for x2,y2 in [[73,1.25],[80,3],[71,6],[76,7]]: 
                ax.plot([96,x2+1.5],[1.1,y2],linestyle='--', color='k', lw=self.lw3,zorder=5) 
                self.lib.make_human(x2, y2, ax, s=sz,c = self.sib_color)  
       
        else: 
            for x2,y2 in [[48,1.9],[58,9.1],[37,8],[43,3.65]]: 
                ax.plot([16,x2-0.5],[1.1,y2],linestyle='--', color='k', lw=self.lw3,zorder=5) 
                self.lib.make_human(x2, y2, ax, s=sz,c = self.sib_color)  
            for x2,y2 in [[54,1.5],[51,5],[64,7.5],[44,9.3]]: 
                ax.plot([84,x2+1.5],[1.1,y2],linestyle='--', color='k', lw=self.lw3,zorder=5) 
                self.lib.make_human(x2, y2, ax, s=sz,c = self.sib_color)  

        a,b,c = 80,99,22
        self.lib.make_human(a, c, ax, s=sz*1.0,c = self.sib_color)  
        self.lib.make_human(b, c, ax, s=sz*1.0,c = self.sib_color)  
        ax.plot([a+2.2,b-1],[c,c],linestyle='--', color='k', lw=self.lw3,zorder=5) 
        ax.text(a+(b-a)/2, c+0.3, 'Sibling\nPairs', ha='center',fontsize=self.fs6) 



        if NULL: ax.plot([-4,104],[-0.12,-0.12],color='k', lw=self.lw2,zorder=5,clip_on=False)
        else:    ax.plot([-1,102],[-0.12,-0.12],color='k', lw=self.lw2,zorder=5,clip_on=False)
        names = ['Lower Tail', 'Upper Tail'] 
        if NULL: locs = [3,96] 
        else:    locs = [11,89] 
        for x,n in zip(locs, names): 
            ax.text(x, -1, n, ha='center', va='top', fontsize= self.fs4-0.5) 

        # Expected
        if NULL: 
            txt1 = 'Common-Variant\nTail\nArchitecture\nCauses\nRegression\nto Mean' 
            self.lib.make_arrow(ax, a = (9,10), b = (13,6), txt = txt1,FLIP=True, SHIFT=True) 
        else: 
            txt1 = '$De\,\,Novo$\nTail Architecture\nCauses Sibling\nDiscordance'
            txt1 = 'De Novo\nTail Architecture\nCauses Sibling\nDiscordance'
            self.lib.make_arrow(ax, a = (19,11), b = (23,6.5), txt = txt1,FLIP=True, SHIFT=True) 
        return
















