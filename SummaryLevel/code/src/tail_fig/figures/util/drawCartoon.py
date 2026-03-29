import sys, os 
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path: sys.path.insert(0, HERE)
from Util import * 
import drawVarious as DV 

class FigLib: 
    def __init__(self, options, AK={}):
        self.options = options
        self.fs1, self.fs2, self.fs3,self.fs4,self.fs5 = 12,10,8,7,5
        self.sz1, self.sz2,self.sz3 = 15,9,8
        self.lw1, self.lw2, self.lw3 = 1, 0.8,0.5

        self.nullMP = 800
        self.nullVar = 11.5
        self.Xn = np.arange(-40,40,0.05)
        self.Yn = [(y*self.nullMP) for y in stats.norm.pdf(self.Xn, 0, self.nullVar)]
        self.Yn = [y - min(self.Yn) for y in self.Yn]
        self.distcolor = 'xkcd:dark cream'
        self.distcolor = 'xkcd:pale gold' 
        self.distcolor = 'xkcd:burnt yellow' 
        self.alpha=0.33



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
                    


    def make_human(self, xp, yp, ax, s = 2, bc='k', c = 'red', rc2 = 'lime', risk1=0, risk2=0):
        head = matplotlib.patches.Circle((xp + s/4.0, yp+ s), s/2.5, facecolor=c, zorder=10,clip_on=False)
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



    def arrow_axes(self, ax, x_info, y_info): 
        y1, y2, yl, YL = y_info  
        x1, x2, xl, XL = x_info 
        ax.arrow(x1, y1, x2-x1, 0,  linewidth=self.lw2,  head_width=0.15, head_length=5, fc='k', ec='k',clip_on=False,zorder=0)
        ax.set_xlabel(xl,fontsize=self.fs3,labelpad=1) 
        ax.arrow(x1, y1, 0, y2-y1-0.4,  linewidth=self.lw2,  head_width=3.3, head_length=0.25, fc='k', ec='k',clip_on=False,zorder=0)
        ax.set_ylabel(yl,fontsize=self.fs3) 


    def make_arrow(self, ax, a = (0,8), b = (-8,3), FLIP=False, txt='NA', STYLE='NA', SHIFT=False):  
        # Define arrow properties
        arrowstyle = "Simple, tail_width=0.2, head_width=2, head_length=1"
        if FLIP: connectionstyle = "arc3,rad=.1"  # Adjust the curvature with 'rad'
        else:    connectionstyle = "arc3,rad=-.1"  # Adjust the curvature with 'rad'
        arrow_properties = {"arrowstyle": arrowstyle,"color": "k",}
        # Define arrow start and end points
        tail_position,head_position = a,b 
        # Create the arrowi
        arrowstyle = "Simple,tail_width=0.03,head_width=0.5,head_length=0.5"
        arrow = matplotlib.patches.FancyArrowPatch(tail_position, head_position, connectionstyle=connectionstyle, mutation_scale=1, linewidth=0.5, **arrow_properties)
        # Add the arrow to the plot
        ax.add_patch(arrow)
        if txt != 'NA': 
            if SHIFT: ax.text(a[0]+2,a[1]+1,txt,ha='center',va='bottom',fontsize=self.fs4-1, zorder=999) 
            else: ax.text(a[0],b[0]+5,txt,ha='center',va='center',fontsize=5) 





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








