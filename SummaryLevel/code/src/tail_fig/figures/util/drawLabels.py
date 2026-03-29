import sys, os 
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path: sys.path.insert(0, HERE)
from Util import *
import drawVarious as DV









class BoxKeys:
    def __init__(self,ax,lw1=1,lw2=0.8,lw3=0.3,sz1=15,sz2=10,sz3=5,fs1=7.5,fs2=6,fs3=5):
        self.ax, self.lms = ax, DV.AxLims(ax) 
        self.lw1,self.lw2,self.lw3 =lw1,lw2,lw3
        self.sz1,self.sz2,self.sz3 =sz1,sz2,sz3
        self.fs1,self.fs2,self.fs3 =fs1,fs2,fs3
        self.xd  = [self.lms.xMin, self.lms.xMax, self.lms.xStep, self.lms.xHop]
        self.yd = [self.lms.yMin, self.lms.yMax, self.lms.yStep, self.lms.yHop]



    def get_points(self,loc, n, x_buffers=[1,3], y_buffers=[1,1]): 
        xa,xb,xs,xh  = [self.lms.xMin, self.lms.xMax, self.lms.xStep, self.lms.xHop]
        ya,yb,ys,yh  = [self.lms.yMin, self.lms.yMax, self.lms.yStep, self.lms.yHop]
        spot, span = loc.split('-')[0].upper(), loc.split('-')[-1] 
        try:    span = float(loc.split('-')[-1]) 
        except: span =1 
        if spot in ['BOTTOM','TOP']:
            if spot == 'TOP':    y1, y2 = [yb+ys*y_buffers[0], yb+ys*y_buffers[0] + ys*y_buffers[1]] 
            else:                y1, y2 = [ya-ys*y_buffers[0] - ys*y_buffers[1], ya-ys*y_buffers[0]] 
            yl = y1+(y2 - y1)/2.0 
            xL, xR = xa + xs * x_buffers[0], xb - (xs*x_buffers[0])+((span-1)*self.lms.xRange) 
            jp = ((xR - xL))/n 
            xp = [xL + x_buffers[1]*xh + (jp*i) for i in range(n)] 
            DV.draw_square(self.ax, xL, xR, y1, y2, clr='k', lw=0.5) 
            return xp,yl  
        else: 
            print('unsupported') 
            sys.exit() 


    def add_group_key(self, loc, data): 
        xs,xh  = self.lms.xStep, self.lms.xHop
        ys,yh  = self.lms.yStep, self.lms.yHop
        xp,yl = self.get_points(loc, 3, y_buffers=[3.5,2.6], x_buffers=[0.2,6]) 
        names = ['Exome (Single Variant)','Exome (Burden Variant)','GWAS Hits'] 
        for i,(x,g,c) in enumerate(zip(xp,data.group_names, data.group_colors)): 
            if i == 1: x -= i*xs*3.3
            else:      x -= i*xs*1.6 
            self.ax.scatter(x,yl-yh,marker='o',color=c,edgecolor='grey',lw=0.2,s=self.sz1*2,clip_on=False,zorder=10) 
            self.ax.text(x+3*xh,yl-yh,g, ha='left',va='center',fontsize=self.fs2-0.25,clip_on=False) 
        x1,y = xp[0], yl + yh 
        return






    def add_popout_key(self,loc):
        xs,xh  = self.lms.xStep, self.lms.xHop
        ys,yh  = self.lms.yStep, self.lms.yHop
        xp,yl = self.get_points(loc, 3, y_buffers=[1.35,1.45]) 
        clrs = ['blue','darkorange','dimgrey'] 
        names = ['Observed $\overline{PRS}$','Expected PRS','$POPout Effect'] 
        for i,(x,c,n) in enumerate(zip(xp, clrs, names)): 
            if i == 0: 
                self.ax.scatter(x,yl, color=c, marker='v',s=self.sz2,clip_on=False)
                self.ax.scatter(x+xh*2,yl, color=c, s=self.sz2,clip_on=False)
                self.ax.scatter(x+xh*4,yl, color=c, marker='^',s=self.sz2,clip_on=False)
                self.ax.text(x+xh*6,yl,'Observed $\overline{PRS}$',ha='left',va='center',fontsize=self.fs3)
            elif i == 1: 
                x += 2.75*xh 
                self.ax.scatter(x,yl, color=c, marker='v',s=self.sz2,clip_on=False)
                self.ax.scatter(x+xh*4,yl, color=c, marker='^',s=self.sz2,clip_on=False)
                self.ax.plot([x,x+xh*4],[yl,yl], clip_on=False,color=c,linestyle='-',lw=self.lw2) 
                self.ax.text(x+xh*6,yl,'Expected PRS',ha='left',va='center',fontsize=self.fs3)
            else: 
                x += 4.25*xh 
                self.ax.plot([x,x],[yl-2.8*yh,yl+2.8*yh], clip_on=False,color='dimgrey',linestyle='--',lw=1)
                self.ax.plot([x-xh*0.9,x+xh*0.9],[yl-2.8*yh,yl-2.8*yh], clip_on=False,color='dimgrey',linestyle='-',lw=1)
                self.ax.plot([x-xh*0.9,x+xh*0.9],[yl+2.8*yh,yl+2.8*yh], clip_on=False,color='dimgrey',linestyle='-',lw=1)
                self.ax.text(x+xs*0.5,yl,'$POPout$ Effect',ha='left',va='center',fontsize=self.fs3)
        return



    def add_prediction_key(self, loc): 
        xs,xh  = self.lms.xStep, self.lms.xHop
        ys,yh  = self.lms.yStep, self.lms.yHop
        clrs = ['blue','darkorange']  
        names = ['Observed Performance','Expected Performance'] 

        xp,yl = self.get_points(loc, 2, y_buffers=[4,3.0], x_buffers=[3,5]) 
        for i,(x,c,n) in enumerate(zip(xp, clrs, names)): 

            if i == 0: 
                x += 2.75*xh 
                self.ax.scatter(x,yl, color=c, marker='o',s=self.sz2,clip_on=False)
                self.ax.scatter(x+xh*4,yl, color=c, marker='o',s=self.sz2,clip_on=False)
                self.ax.plot([x,x+xh*4],[yl,yl], clip_on=False,color=c,linestyle='-',lw=self.lw2) 
                self.ax.text(x+xh*6,yl,'Observed $\overline{PRS}$',ha='left',va='center',fontsize=self.fs3)
            else: 
                x -= 2.75*xh 
                self.ax.plot([x,x+xh*7],[yl,yl], clip_on=False,color=c,linestyle='--',lw=self.lw2) 
                self.ax.text(x+xh*8,yl,'Expected PRS',ha='left',va='center',fontsize=self.fs3)
        return







    def add_trumpet_key(self, loc, c1 = 'xkcd:cherry red', c2 = 'grey', c3 = 'green', fs = 45, sz = 1200): 
        xs,xh  = self.lms.xStep, self.lms.xHop
        ys,yh  = self.lms.yStep, self.lms.yHop
        xp,yl = self.get_points(loc, 3, y_buffers=[2.3,1.4], x_buffers=[0.3,3]) 
        clrs = [[c1,c1],['white',c1],[c2,c2]] 
        names = ['Exome (Single Variant)','Exome (Burden Variant)','GWAS Hits'] 
        for i,(x,c,n) in enumerate(zip(xp, clrs, names)): 
            x+= xh*5*i 
            self.ax.scatter(x, yl, marker='o', edgecolor=c[1], color=c[0], lw=0.2, clip_on=False, zorder=10, s = self.sz1+5) 
            self.ax.text(x+ xh*1.5, yl, n, fontsize=self.fs3, va='center') #fontweight='bold')  
            x+= xh*10
        return


    def add_rare_key(self, loc, data): 
        xs,xh  = self.lms.xStep, self.lms.xHop
        ys,yh  = self.lms.yStep, self.lms.yHop
        xp,yl = self.get_points(loc, 3, y_buffers=[1.5,1.6], x_buffers=[0.2,2]) 
        names = ['Exome (Single Variant)','Exome (Burden Variant)','GWAS Hits'] 
        for i,(x,g,c) in enumerate(zip(xp,data.group_names, data.group_colors)): 
            if i == 1: x -= i*xs*0.8
            else:      x -= i*xs*0.4 
            self.ax.scatter(x,yl-yh*2,marker='s',color=c,s=self.sz1,clip_on=False,zorder=10) 
            self.ax.text(x+xh*0.9,yl-yh*2,g, ha='left',va='center',fontsize=self.fs2,clip_on=False) 
        x1,y = xp[0], yl + yh 
        self.ax.text(xp[0],yl+yh*2,'Genome Wide Significant Exome Hits:', ha='left',va='center',fontsize=self.fs2,clip_on=False)
        for x,m,n in zip([xp[2]-xs+xh,xp[2]+xs],['v','^'],['Lower Tail','Upper Tail']): 
            self.ax.scatter(x,yl+yh*2,marker=m,color='k',s=self.sz1,clip_on=False,zorder=10) 
            self.ax.text(x+xh*0.7,yl+yh*2,n, ha='left',va='center',fontsize=self.fs2,clip_on=False)
        return

    def add_multi_key(self, loc, clrs): 

        xs,xh  = self.lms.xStep, self.lms.xHop
        ys,yh  = self.lms.yStep, self.lms.yHop
        xp,yl = self.get_points(loc, 5, y_buffers=[0.60,2.6], x_buffers=[0.1,2]) 
        names = ['Rare PRS (<1%)','Rare PRS (<0.1%)','Burden PRS','Common PRS','Common+Rare PRS (Tails)'] 
        for i,(x,c,n) in enumerate(zip(xp, clrs, names)): 
            if i == 1:   x -= 2*xh 
            elif i == 2: x += 0.5*xh 
            elif i == 3: x -= 10*xh 
            elif i == 4: x -= 17*xh
            self.ax.scatter(x, yl, marker='o', edgecolor='k', color=c, lw=0.2, clip_on=False, zorder=10, s = self.sz1) 
            self.ax.text(x+ xh*1.8, yl, n, fontsize=self.fs3, va='center') #fontweight='bold')  
        return





   
    def add_odds_key(self, fs = 30, fs2=24, c1='yellow', c2='yellow', RULE='NA'): 
        xs,xh  = self.lms.xStep, self.lms.xHop
        ys,yh  = self.lms.yStep, self.lms.yHop
        x1, x2 = self.lms.xMax - 11*xh, self.lms.xMax - 0.5*xh 
        y1,y2 = self.lms.yMin + ys, self.lms.yMin+2.5*ys
        RT = matplotlib.patches.Rectangle((x1, y1),x2-x1, y2-y1, color='white', ec = 'k', lw = self.lw3, alpha=0.9, zorder=10,clip_on=False)
        self.ax.add_patch(RT)
        x = x1 + xh*1.3
        clrs = [c1,c2] 
        for i in range(2): 
            yp = y2 - yh*1.5 - 0.7*ys*i  
            self.ax.scatter(x,yp,color=clrs[i], ec ='k', s=self.sz2, lw=self.lw3, zorder=10) 
            self.ax.plot([x-xh,x+xh],[yp,yp],color=clrs[i], lw=self.lw2, zorder=10) 
            if i == 0: self.ax.text(x+xh*5,yp,'Common PRS',zorder=20, ha='center', va='center',clip_on=False,fontsize=self.fs3) 
            else:      self.ax.text(x+xh*5.2,yp,'Common+Rare\nPRS',zorder=20, ha='center', va='center',clip_on=False,fontsize=self.fs3) 
        return  


    def add_recovery_key(self, fs = 35, fs2=29, c1='yellow', c2='yellow', c3 = 'dodgerblue', c4='xkcd:shamrock green', RULE='NA'): 
        xs,xh  = self.lms.xStep, self.lms.xHop
        ys,yh  = self.lms.yStep, self.lms.yHop
        x1, x2 = self.lms.xMin + 2.6*xs, self.lms.xMin + 5.5*xs
        y1, y2 = self.lms.yMin + ys, self.lms.yMin + 3*ys
        yb,yl = self.lms.yMin + ys*1.5, self.lms.yMin + ys*2         
        clrs = ['grey',c2,c3,c4]  
        RT = matplotlib.patches.Rectangle((x1, y1),x2-x1, y2-y1, color='white', ec = 'k', lw = self.lw3, alpha=0.9, zorder=10,clip_on=False)
        self.ax.add_patch(RT)
        x, ya = x1 + 3.0*xh, y1 + ys*1.35
        self.ax.barh(ya,0.16,left=x,height=10,color=c1, alpha=0.99, lw=0.1, ec='k', zorder=11,clip_on=False) 
        self.ax.barh(ya,0.16,left=x+0.16,height=10,color=c2, alpha=0.99, lw=0.1, ec='k', zorder=11,clip_on=False) 
        self.ax.barh(ya,0.16,left=x+0.32,height=10,color=c3, alpha=0.99, lw=0.1, ec='k', zorder=11,clip_on=False) 
        self.ax.arrow(x+xh*0.5, ya+10,  0, -7, linewidth=0.5, head_width=0.01, head_length=3.5, fc='k', ec='k',clip_on=False,zorder=12)
        self.ax.text(x+xh*2, ya+12,  '1%${>}MAF{>}0.1$%', ha='center', fontsize=self.fs3, zorder=13) 

        
        self.ax.arrow(x+xh*4.2, ya-10,  0, 7, linewidth=0.5, head_width=0.01, head_length=3.5, fc='k', ec='k',clip_on=False,zorder=12)
        self.ax.text(x+xh*4.7, ya-12,  '0.1%$>MAF>0.01$%', ha='center', va='top', fontsize=self.fs3, zorder=13) 
        

        self.ax.arrow(x+xh*8, ya+10,  0, -7, linewidth=0.5, head_width=0.01, head_length=3.5, fc='k', ec='k',clip_on=False,zorder=12)
        self.ax.text(x+xh*9.25, ya+12,  'Burdens', ha='center', fontsize=self.fs3, zorder=13) 
        
        self.ax.scatter(x+xs*0.13,y1+ys*0.4,marker='*',color='k',s=self.sz1,lw=self.lw3,zorder=11,clip_on=False) 
        self.ax.text(x+xh+xs*0.75,y1+ys*0.34,'Sig Reduction\nP-val<0.05',va='center',zorder=11,ha='center',fontsize=self.fs3)
        return  








































class TailLabels:
    def __init__(self, options): #trait_key, DRAW=True): 
        self.options = options 

    def add_indiv_key(self, ax, ck, RULE='LOWER',fs =8, fs2=6, fs3=5): 
        xMin, xMax = ax.get_xlim() 
        yMin, yMax = ax.get_ylim()
        xs, ys = (xMax-xMin)/100.0, (yMax-yMin)/100.0
        x1, x2 = xMin +3*xs, xMin + 95*xs
        y1, yl, y2 = yMax - 20*ys, yMax - 20*ys, yMax +13*ys
        clrs = [ck.c1, ck.c2, ck.rc, ck.rce,ck.c1,ck.c2,ck.c1e,ck.c2e] 
        maps = [ck.map1, ck.map2, ck.map3] 
        DV.draw_square(ax, x1, x2, y1, y2) 
        sz = 19
        yjj = 21.5
        if RULE == 'LOWER': ax.text(x1+xs*29, y2-ys*1.5, 'Lower Tail Bins',ha='center',va='top',fontsize=fs2) 
        else:               ax.text(x1+xs*29, y2-ys*1.5, 'Upper Tail Bins',ha='center',va='top',fontsize=fs2) 
        for i,xj in enumerate([1, 25, 47,67]): 
            x = x1+xs*xj
            if i < 3: 
                xp, yp = x, y2-ys*yjj
                for j,cm in enumerate(maps[i]): 
                    rt = matplotlib.patches.Rectangle((xp+j*0.16,yp),0.16,0.02,color=cm)
                    ax.add_patch(rt) 
                if i == 0: ax.text(x+0.16*5, y2-ys*(yjj+2), 'Common PRS',ha='center',va='top',fontsize=fs3) 
                elif i == 1: ax.text(x+0.16*5, y2-ys*(yjj+2), 'Rare${+}$Common PRS',ha='center',va='top',fontsize=fs3) 
                elif i == 2: ax.text(x+0.16*5, y2-ys*(yjj+2), 'Rare PRS',ha='center',va='top',fontsize=fs3) 
            else: 
                ax.scatter(x,y2-ys*17, marker='*', color='k', ec= 'k', s=sz, zorder=5, clip_on=False) 
                ax.text(x+xs*2.1, y2-ys*8.5, 'Sig. Dif (P$<$0.05)\nRelative to Common',ha='left',va='top',fontsize=fs3) 
        return


    def make_extreme_index_key(self, pp, ck, fs = 6): 
        ax, lms = pp.ax, pp.lms 
        xMin, yMin, xs, ys = lms.xMin, lms.yMin, lms.xStep, lms.yStep
        x1, x2 = xMin - 33.2*xs, xMin + 9.6*xs
        y1, yl, y2 = yMin - 4.35*ys, yMin - 3.25*ys, yMin - 2.1*ys
        clrs = [ck.rc, ck.rce, ck.c1, ck.c1e,ck.c2, ck.c2e,ck.c2e] 
        sz = 22
        for i,xj in enumerate([0.15, 5.0, 11.33, 17.15,24.9,34.4]): 
            x = x1+xs*xj
            if i in [0,2]: 
                ax.scatter(x,yl, marker='v', color=clrs[i], ec= 'k', lw=0.5,s=sz, zorder=5, clip_on=False) 
                ax.scatter(x+0.5*xs,yl, marker='o', color=clrs[i], ec= 'k', lw=0.5,s=sz, zorder=5, clip_on=False) 
                ax.scatter(x+1*xs,yl, marker='^', color=clrs[i], ec= 'k', lw=0.5,s=sz, zorder=5, clip_on=False) 
            else: 
                ax.scatter(x,yl, marker='v', color=clrs[i], ec= 'k', s=sz, lw=0.5,zorder=5, clip_on=False) 
                ax.scatter(x+0.5*xs,yl, marker='^', color=clrs[i], ec= 'k', lw=0.5,s=sz, zorder=5, clip_on=False) 
            if i == 0: ax.text(x+1.30*xs,yl,'Rare PRS',va='center',ha='left',fontsize=fs)
            elif i == 1: ax.text(x+0.88*xs,yl,'Rare Tails (0.1%)',va='center',ha='left',fontsize=fs)
            elif i == 2: ax.text(x+1.30*xs,yl,'Common PRS',va='center',ha='left',fontsize=fs)
            elif i == 3: ax.text(x+0.8*xs,yl,'Common Tails (0.1%)',va='center',ha='left',fontsize=fs)
            elif i == 4: ax.text(x+1.03*xs,yl,'Rare${+}$Common Tails (1%)',va='center',ha='left',fontsize=fs)
            else: ax.text(x+0.9*xs,yl,'Rare${+}$Common Tails (0.1%)',va='center',ha='left',fontsize=fs)
        DV.draw_square(ax, x1-5, x2+5, y1-ys*0.3, y2+ys*0.2) 
        return  





















