import sys, os 
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path: sys.path.insert(0, HERE)
from Util import *
import drawVarious as DV




class EvoScatter:
    def __init__(self,ax,fig,ti): 
        self.ax, self.fig = ax, fig 
        try: 
            self.VALID, self.NULL, self.T = True, False, fig.traits[ti] 
            self.Y = self.T.pts['lrs'].Y 
            self.X = [stats.norm.ppf((xl+0.5)/100.0) for xl in range(len(self.Y))]
        except KeyError: 
            self.VALID, self.NULL, self.T = False, True, 'NA' 
            self.main_box, self.mini_box = self.null_box, self.null_box 


    def null_box(self, xp=1, yp=1, xlab=None, ylab=None): 
        lms = DV.AxLims(self.ax, xt = [], yt = [], xlab = xlab, ylab = ylab, xstretch = 1.4, ystretch = [1.15,2.0], fs = self.fig.fs4-0.25)
        return lms 


    def main_box(self, xp=1,yp=1,xlab=None,ylab=None): 
        if self.fig.progress.SAVESRC: 
            self.fig.progress.out3.write('%s,%s,%s,%s\n' % (self.fig.progress.panel, self.T.id,'TraitValues',";".join([str(round(x,4)) for x in self.X])))  
            self.fig.progress.out3.write('%s,%s,%s,%s\n' % (self.fig.progress.panel, self.T.id,'LRS',";".join([str(round(x,4)) for x in self.Y])))  
        self.ax.scatter(self.X,self.Y, color = self.T.group_color, s = self.fig.sz1, edgecolor='lightgrey', alpha = 0.75, lw=self.fig.lw3, zorder = 1)
        if self.T.vals['lrs'].model != 'Y~yInt':
            pm = self.T.vals['lrs'].params 
            yDash = [pm[0] + (x*pm[1]) + (x*x*pm[2]) for x in self.X]
            self.ax.plot(self.X, yDash, color='k',linestyle='--',linewidth=self.fig.lw1,zorder=3)
            if self.fig.progress.SAVESRC: 
                self.fig.progress.out3.write('%s,%s,%s,%s\n' % (self.fig.progress.panel, self.T.id,'fitLine',";".join([str(round(x,4)) for x in yDash])))  
        if xp == 0: ylab = 'Lifetime\nReproductive\nSuccess'
        if yp == 3: xlab = 'Trait Value (z)'
        lms = DV.AxLims(self.ax, xt = [], yt = [], xlab = xlab, ylab = ylab, xstretch = 1.4, ystretch = [1.15,2.0], fs = self.fig.fs4-0.25)
        if self.T.ti == 30020: self.ax.text(lms.xMin + lms.xHop, lms.yMax - lms.yStep/3.0, 'Haemoglobin\nConc.', ha = 'left', va ='top',fontsize=self.fig.fs4)
        else:                  self.ax.text(lms.xMin + lms.xRange/2.0, lms.yMax - lms.yStep/3.0, self.T.name.mini, ha = 'center', va ='top',fontsize=self.fig.fs4)
        return lms

    def mini_box(self, fs=5, sz=6, lw=9.6): 
        if self.fig.progress.SAVESRC: 
            self.fig.progress.out3.write('%s,%s,%s,%s\n' % (self.fig.progress.panel, self.T.id,'TraitValues',";".join([str(round(x,4)) for x in self.X])))  
            self.fig.progress.out3.write('%s,%s,%s,%s\n' % (self.fig.progress.panel, self.T.id,'LRS',";".join([str(round(x,4)) for x in self.Y])))  
        self.ax.scatter(self.X,self.Y, color = self.T.group_color, s = sz, edgecolor='lightgrey', alpha = 0.75, lw=lw, zorder = 1)
        if self.T.vals['lrs'].model != 'Y~yInt':
            pm = self.T.vals['lrs'].params 
            yDash = [pm[0] + (x*pm[1]) + (x*x*pm[2]) for x in self.X]
            self.ax.plot(self.X, yDash, color='k',linestyle='--',linewidth=3*lw,zorder=3)
            if self.fig.progress.SAVESRC: self.fig.progress.out3.write('%s,%s,%s,%s\n' % (self.fig.progress.panel, self.T.id,'fitLine',";".join([str(round(x,4)) for x in yDash])))  
        lms = DV.AxLims(self.ax, xt = [], yt = [], xstretch = [0.3,0.3], ystretch = [0.1,3.3], fs = fs)
        xs, yp, fs = lms.xHop, lms.yMax - lms.yHop, 5
        evo = self.T.vals['lrs'].evo.split('-') 
        if 'stabilising' in evo or 'diverging' in evo: 
            if 'diverging' in evo: R1 = 'Disruptive' 
            else:                  R1 = 'Stabilising' 
            if 'pos' in evo:       self.ax.text(lms.xMin + xs, yp, R1+',\nPos', ha='left', va='top', fontsize=fs) 
            elif 'neg' in evo:     self.ax.text(lms.xMax - xs, yp, R1+',\nNeg', ha='right', va='top', fontsize=fs) 
            else:                  self.ax.text(lms.xMid, yp, R1, ha='center', va='top', fontsize=fs) 
        elif 'pos' in evo:         self.ax.text(lms.xMin + xs, yp, 'Positive', ha='left', va='top', fontsize=fs) 
        elif 'neg' in evo:         self.ax.text(lms.xMax - xs, yp, 'Negative', ha='right', va='top', fontsize=fs) 
        else: return lms
        return lms 



        
















class POPplot:
    def __init__(self,ax,fig,ti,xLab=None,yLab=None,alp=0.5,lw1=1,lw2=0.8,lw3=0.3,sz1=13,sz2=10,sz3=8,fs1=7.5,fs2=6,fs3=5,INIT=False): 
        self.ax, self.fig, self.xLab, self.yLab, self.alp, self.INIT = ax, fig, xLab, yLab, alp, INIT 
        self.lw1,self.lw2,self.lw3 =lw1,lw2,lw3
        self.sz1,self.sz2,self.sz3 =sz1,sz2,sz3 
        self.fs1,self.fs2,self.fs3 =fs1,fs2,fs3    
        self.swap_key = {'poc': 'mlt', 'rep': 'rpt', 'aou': 'aou', 'ukb': 'ukb', 'UKB': 'UKB','A+B+burden': 'RarePRS'}
        self.X, self.markers = [x for x in range(100)], [] 
        self.zrp1, self.zrp2 = 'NA', 'NA'  
        if ti in fig.traits: self.VALID, self.NULL, self.T = True, False, fig.traits[ti] 
        else:                self.VALID, self.NULL, self.T = False, True, 'NA' 



    def draw_rep_popout(self, k, rc1='blue', yc1='blue', yc2='blue', TITLE=False): 
        self.rc1, self.yc1, self.yc2 = rc1, yc1, yc2 
        if self.VALID:  
            self.draw_body(k, rc1=self.rc1, yc1=self.yc1, yc2=self.yc2, ALLOW_MISSING=False) 
            self.draw_tail()
            self.label_reps() 
            if TITLE:  self.ax.set_title(self.T.name.cornerStyle, fontsize = self.fs1-1, loc='left', x=0.012, y= 0.908,va='top')
        else:  
            DV.draw_blank(self.ax) 
            self.lms = DV.AxLims(self.ax, xt=[], yt=[], xLim=[0,1],yLim=[0,1]) 




    def draw_common_popout(self, BRIEF = False, MINI=False):  
        if self.VALID: 
            self.draw_body('common') 
            self.draw_tail()
            if MINI: 
                self.lms = DV.AxLims(self.ax, xt = [], yt = [], xlab = None, ylab = None, xstretch = [1.1,1.3], ystretch = [1.1,1.0], fs = 8)
                #if self.T.qc['misc'].r2 > 0.01:  
                self.label_popout_by_fdr(MINI=True, lw=0.4,fs=5)  
                return self 
            if not BRIEF: 
                self.label_popout()  
                self.ax.set_title(self.T.name.cornerStyle, fontsize = self.fs1, loc='left', x=0.015, y= 0.875,va='top')
        else: 
            DV.draw_blank(self.ax) 
            self.lms = DV.AxLims(self.ax, xt=[], yt=[], xLim=[0,1],yLim=[0,1]) 
        return self 


    def draw_common_recovery(self, BRIEF = False): 
        if self.VALID: 
            self.draw_body('common')
            self.draw_tail(RECOVERY=True)
            self.label_recovery()
            self.set_subtitle('COMMON_RECOVERY')
            return self 
        else:  
            DV.draw_blank(self.ax) 
            self.lms = DV.AxLims(self.ax, xt=[], yt=[], xLim=[0,1],yLim=[0,1]) 
        return self 

    def draw_extreme_recovery(self): 
        if self.VALID: 
            self.draw_body('common')
            self.draw_tail(RECOVERY=True)
            self.draw_extreme_tail(eclr = 'cyan', rclr='lime',RECOVERY=True, prs_type='common')
            self.label_recovery(EXTREME=True)
            self.set_subtitle('EXTREME_RECOVERY')
        else:  
            DV.draw_blank(self.ax) 
            self.lms = DV.AxLims(self.ax, xt=[], yt=[], xLim=[0,1],yLim=[0,1]) 
        return self 
        
    
    def draw_extreme_rares(self, k, yc1='gold', yc2='gold', yc3='xkcd:bright yellow', ec1='k', ec2='k'):  
        self.yc1, self.yc2, self.yc3, self.ec1, self.ec2 = yc1, yc2, yc3, ec1, ec2 
        if self.VALID: 
            self.draw_body('A+B+burden', yc1=self.yc1,yc2=self.yc2,ec1=self.ec1,ec2=self.ec2)
            self.draw_tail(HIDE_EXPECTED=True) 
            self.draw_extreme_tail(eclr = self.yc3, prs_type=k) 
            self.set_subtitle() 
        else:  
            DV.draw_blank(self.ax) 
            self.lms = DV.AxLims(self.ax, xt=[], yt=[], xLim=[0,1],yLim=[0,1]) 
        return self 
  
    

    def draw_body(self,p_type,yc1='blue',yc2='blue',ec1='orange',ec2='darkorange',rc1='xkcd:shamrock green',rc2='lime',tailType='STANDARD', ALLOW_MISSING=True):  
        self.type, self.tailType, self.yc1, self.yc2, self.ec1, self.ec2, self.rc1, self.rc2 = p_type, tailType, yc1, yc2, ec1, ec2, rc1, rc2 
        try: 
            P = self.T.pts['pop'][p_type] 
            self.Y, self.Ye = P.yObs, P.yExp   
            self.X, self.markers = [x for x in range(len(self.Y))], []  
            self.ax.plot(self.X, self.Ye, linestyle='-', color = ec1, linewidth=self.lw2, zorder=0)
            try: 
                self.S, self.Se = P.sObs, P.sExp 
                self.ax.plot(self.X[1:99], [ye+(se*5.5) for ye,se in zip(self.Ye[1:99],self.Se[1:99])], color=ec1,zorder=1,linestyle='--',lw=self.lw/2.0) 
                self.ax.plot(self.X[1:99], [ye-(se*5.5) for ye,se in zip(self.Ye[1:99],self.Se[1:99])], color=ec1,zorder=1,linestyle='--',lw=self.lw/2.0) 
            except AttributeError: pass 
            self.ax.scatter(self.X[1:99], self.Y[1:99],color=yc1,edgecolor=yc1,  alpha=self.alp,  zorder=1, lw=0.1, s = self.sz3) 
        except: 
            self.Y, self.Ye = [0 for x in self.X], [0 for x in self.X] 
            if ALLOW_MISSING:
                xp = [x for x in self.X if x in [0,2,4,95,97,99] or x % 4 == 0] 
                self.ax.scatter(xp, [0 for x in xp],color=yc1,edgecolor=yc1,alpha=0.5,zorder=1, s = self.sz3-1, lw=0.3) 
            else:
                self.lms = DV.AxLims(self.ax, xt = [], yt = [], xlab = self.xLab, ylab = self.yLab, ystretch=0.5, xstretch=0.75,fs = 45 ) 
                self.NULL, self.VALID = True, False 
        
        if self.fig.progress.SAVESRC: self.save_body(p_type) 
        return self 


    def save_body(self,p_type): 
        Xs = ";".join([str(x) for x in self.X]) 
        Ys = ";".join([str(x) for x in self.Y]) 
        Ye = ";".join([str(x) for x in self.Ye]) 
        w = self.fig.progress.out3
        if self.INIT: w.write('%s,%s,%s,%s,%s\n' % ('Panel', 'Trait-ID','PRS-Type','Data','Values')) 
        if p_type in self.swap_key: p_type = self.swap_key[p_type] 

        w.write('%s,%s,%s,%s,%s\n' % (self.fig.progress.panel,self.T.id,p_type,'Trait-Centiles',Xs)) 
        w.write('%s,%s,%s,%s,%s\n' % (self.fig.progress.panel,self.T.id,p_type,'Observed-PRS',Ys)) 
        w.write('%s,%s,%s,%s,%s\n' % (self.fig.progress.panel,self.T.id,p_type,'Expected-PRS',Ye)) 
        return






    def draw_alt(self,p_type,yc1='blue',yc2='blue',ec1='orange',ec2='darkorange',rc1='xkcd:shamrock green',rc2='lime',alp=1,tailType='STANDARD', ALLOW_MISSING=False):  
        self.type, self.tailType, self.yc1, self.yc2, self.ec1, self.ec2, self.rc1, self.rc2 = p_type, tailType, yc1, yc2, ec1, ec2, rc1, rc2 
        try: 
            P = self.T.pts['apop'][p_type] 
            self.Y, self.Ye = P.yObs, P.yExp   
            self.X, self.markers = P.X, []
            self.ax.plot(self.X, self.Ye, linestyle='-', color = ec1, linewidth=self.lw1, zorder=0)
            if len(self.X) > 500: mp   = 0.01 
            elif len(self.X) > 150: mp = 0.05 
            elif len(self.X) < 50:  mp = 0.5 
            else:                   mp = 1 
            self.ax.scatter(self.X[1:-1], self.Y[1:-1],color=yc1,edgecolor=yc1,alpha=0.50,zorder=1, s = self.sz1*mp) 
        except: 
            if ALLOW_MISSING: 
                self.Y, self.Ye = [0 for x in self.X], [0 for x in self.X] 
                self.ax.scatter(self.X, [0 for x in self.X],color=yc1,edgecolor=yc1,alpha=0.50,zorder=1, s = self.sz1) 
            else: 
                self.NULL, self.VALID = True, False 
                self.lms = DV.AxLims(self.ax, xt = [], yt = [], xlab = self.xLab, ylab = self.yLab, ystretch=0.5, xstretch=0.75,fs = 6 ) 
            return self

        self.lms = DV.AxLims(self.ax, xt = [], yt = [], xlab = self.xLab, ylab = self.yLab, ystretch=0.5, xstretch=0.75,fs = 6 ) 
        d1, d2 = self.Y[0] - self.Ye[0], self.Ye[-1] - self.Y[-1] 
        s1, s2 = self.lms.yStep*1.2, self.lms.yStep 
        if d1 > s1:
            self.ax.scatter(self.X[0], self.Y[0], marker='^', color=yc2, ec='k', zorder=4, s=self.sz1 * mp, lw=0.5) 
            self.ax.scatter(self.X[0]-self.lms.xStep/2.0, self.Y[0], marker='*',color='gold', edgecolor='k', alpha=0.9, lw=0.5, zorder=2, s = 1.5*self.sz1) 
        else: self.ax.scatter(self.X[0], self.Y[0], marker='v', color=yc2, ec='k', zorder=4, s=self.sz1 * mp, lw=0.5) 
        if d2 > s2: 
            self.ax.scatter(self.X[-1], self.Y[-1], marker='v', color=yc2, ec='k', zorder=4, s=self.sz1 * mp, lw=0.5) 
            self.ax.scatter(self.X[-1]+self.lms.xStep/2.0, self.Y[-1]+self.lms.yStep, marker='*',color='gold', lw=0.5, edgecolor='k', alpha=0.9, zorder=2, s = 1.5*self.sz1) 
        else: self.ax.scatter(self.X[-1], self.Y[-1], marker='^', color=yc2, ec='k', zorder=4, s=self.sz1 * mp, lw=0.5) 
        

        if self.fig.progress.SAVESRC: self.save_body(p_type) 
        return self 
    










    
    def draw_tail(self, tailType = 'common', rc1='xkcd:shamrock green', HIDE_EXPECTED=False, RECOVERY=False, jump=1):  
        if self.NULL or not self.VALID: return 
        for j,(x1,x2,clr,Z) in enumerate([[0,1,self.ec2,self.Ye],[-1,-2,self.ec2,self.Ye],[0,1,self.yc2,self.Y],[-1,-2,self.yc2,self.Y]]): 
            if Z[x1] > Z[x2]: self.markers.append('^') 
            else:             self.markers.append('v') 
            if j < 2: 
                if not HIDE_EXPECTED: self.ax.scatter(self.X[x1], Z[x1], marker=self.markers[-1], color=clr, ec='k', lw = 0.1, zorder=0, s= self.sz2) 
            else: self.ax.scatter(self.X[x1], Z[x1], marker=self.markers[-1], color=clr, ec ='k', zorder=4, s= self.sz1, lw=0.2) 

        if RECOVERY and 'combo' in self.T.vals['recovery'] and 'combo' in self.T.vals['pop']: 
            j1, j2, rD, rK = self.Y[0]-self.Ye[0], self.Ye[-1]-self.Y[-1], [], self.T.vals['recovery']['combo'] 
            if j1>0 and rK.total1 != 'NA': 
                rD.append([self.X[0], self.Y[0]-j1*rK.total1]) 
                self.ax.scatter(rD[-1][0],  rD[-1][1], marker = self.markers[-2],color = rc1, ec = 'k', zorder = 5, s = self.sz1, lw=0.2)
            if j1>0 and rK.total2 != 'NA': 
                rD.append([self.X[-1], self.Y[-1]+j2*rK.total2]) 
                self.ax.scatter(rD[-1][0],  rD[-1][1], marker = self.markers[-1],color = rc1, ec = 'k', zorder = 5, s = self.sz1, lw=0.2)
            if self.fig.progress.SAVESRC: 
                Xs = ";".join([str(rd[0]) for rd in rD]) 
                Ys = ";".join([str(rd[1]) for rd in rD])
                self.fig.progress.out3.write('%s,%s,%s,%s,%s\n' % (self.fig.progress.panel,self.T.id,'Common+Rare-1%-Recovery','Trait-Centiles',Xs)) 
                self.fig.progress.out3.write('%s,%s,%s,%s,%s\n' % (self.fig.progress.panel,self.T.id,'Common+Rare-1%-Recovery','Relative-PRS',Ys)) 
        return self  























    def draw_extreme_tail(self,eclr='k',rclr='lime',RECOVERY=None,hop=3,jump=3.6, prs_type='common'): 
        Y = self.T.pts['epop'][self.type].yObs 
        yL, yM, yH = Y[0:9], Y[9:109], Y[109::] 
        mL, mH = yL[0] / yM[0] , yH[-1]/ yM[-1] 
        self.z1, self.z2 = self.Y[0]*mL, self.Y[-1]*mH      
        Xs, Zs = '0.1;99.9', str(self.z1)+';'+str(self.z2) 
        self.ax.scatter(self.X[0]-hop,self.z1, color=eclr, s = self.sz2+3, ec ='k', marker=self.markers[-2],lw=0.5)
        self.ax.scatter(self.X[-1]+hop,self.z2, color=eclr, s = self.sz2+3, ec = 'k', marker=self.markers[-1],lw=0.5)  
        if self.fig.progress.SAVESRC: 
            if prs_type != 'common': 
                self.fig.progress.out3.write('%s,%s,%s,%s,%s\n' % (self.fig.progress.panel,self.T.id,'RarePRS-0.1%','Trait-Centiles',Xs)) 
                self.fig.progress.out3.write('%s,%s,%s,%s,%s\n' % (self.fig.progress.panel,self.T.id,'RarePRS-0.1%','Relative-PRS',Zs)) 
            else: 
                self.fig.progress.out3.write('%s,%s,%s,%s,%s\n' % (self.fig.progress.panel,self.T.id,'CommonPRS-0.1%','Trait-Centiles',Xs)) 
                self.fig.progress.out3.write('%s,%s,%s,%s,%s\n' % (self.fig.progress.panel,self.T.id,'CommonPRS-0.1%','Relative-PRS',Zs)) 




        y1, y2 = self.ax.get_ylim() 
        if self.z1 < y1 or self.z2 > y2: 
            yMin,yMax = min(self.z1,y1), max(self.z2,y2) 
            ys = (yMax - yMin)/20.0
            self.lms = DV.AxLims(self.ax, xt = [], yt = [], yLim = [yMin -ys, yMax + ys], xlab = self.xLab, ylab = self.yLab, ystretch=0.5, xstretch=0.95,fs = 45 ) 
        if RECOVERY: 
            if self.type == 'common':
                r1, r2 = self.T.vals['recovery']['combo@0.1'].total1, self.T.vals['recovery']['combo@0.1'].total2
                pop = self.T.vals['pop']['common-snp'] 
                dist1, dist2 = self.z1 - self.Ye[0], self.Ye[-1] - self.z2 
                
                rp1, rp2 = self.z1, self.z2 
                if pop.e1 > 0 and pop.f1: rp1 = self.z1 - (dist1*r1) 
                if pop.e2 > 0 and pop.f2: rp2 = self.z2 - (dist2*r2) 
                self.ax.scatter(self.X[0]-jump,  rp1, color=rclr,  s= self.sz2+3, marker=self.markers[-2],lw=0.5,ec='k') 
                self.ax.scatter(self.X[-1]+jump, rp2, color=rclr,  s= self.sz2+3, marker=self.markers[-1],lw=0.5,ec='k') 
                

                if self.fig.progress.SAVESRC: 
                    self.fig.progress.out3.write('%s,%s,%s,%s,%s\n' % (self.fig.progress.panel,self.T.id,'Common+Rare-0.1%-Recovery','Trait-Centiles',Xs)) 
                    self.fig.progress.out3.write('%s,%s,%s,%s,%s\n' % (self.fig.progress.panel,self.T.id,'Common+Rare-0.1%-Recovery','Relative-PRS',str(rp1)+';'+str(rp2))) 
                
            self.lms = DV.AxLims(self.ax, xt = [], yt = [], xlab = self.xLab, ylab = self.yLab, ystretch=0.5, xstretch=0.95,fs = 45 ) 
        return self







    def set_subtitle(self, COMMAND='NA', fs = 29): 

        self.lms = DV.AxLims(self.ax, xt = [], yt = [], xlab = self.xLab, ylab = self.yLab, ystretch=[0,2], xstretch=1,fs = self.fs2 ) 
        xp = [self.lms.xMin + 3+self.lms.xStep*0.3*j for j in [0,10,12,14]]
        yl = self.lms.yMax - self.lms.yStep*0.6
        if COMMAND in ['COMMON_RECOVERY','EXTREME_RECOVERY']: 
            self.ax.text(self.lms.xMin+self.lms.xHop, self.lms.yMax - self.lms.yHop, 'Common PRS,\nCommon+Rare Tails', va='top', fontsize = self.fs3)  
            return self
        elif self.type =='rareA': self.ax.text(self.lms.xMin+self.lms.xHop, self.lms.yMax - self.lms.yHop, 'Rare PRS:\n1%>MAF>0.1%', va='top', fontsize = self.fs3)  
        elif self.type == 'rareB': self.ax.text(self.lms.xMin+self.lms.xHop, self.lms.yMax - self.lms.yHop, 'Rare PRS:\n0.1%>MAF>0.01%', va='top', fontsize = self.fs3)  
        elif self.type == 'burden': self.ax.text(self.lms.xMin+self.lms.xHop, self.lms.yMax - self.lms.yHop, 'Burden PRS', va='top', fontsize = self.fs3)  
        elif self.type in ['A+B+burden']:  self.ax.text(self.lms.xMin+self.lms.xHop, self.lms.yMax - self.lms.yHop, 'Rare PRS', va='top', fontsize = self.fs3)  
        else: return self  
        return self 
   


        


    def title_recovery(self, fs=29): 
        xp = [self.lms.xMin + 3+self.lms.xStep*0.3*j for j in [0,10,12,14]]
        yl = self.lms.yMax - self.lms.yStep*0.6
        self.ax.text(xp[0]-1.5,yl, 'Common PRS  (', ha='left', va='center',fontsize=fs)
        self.ax.scatter(xp[1],yl, marker='v', color=self.yc1, ec= 'k', s=555, zorder=5, clip_on=False)
        self.ax.scatter(xp[2],yl, marker='o', color=self.yc1, ec= 'k', s=555, zorder=5, clip_on=False)
        self.ax.scatter(xp[3],yl, marker='^', color=self.yc1, ec= 'k', s=555, zorder=5, clip_on=False)
        self.ax.text(xp[3]+2.5,yl, ')', ha='left', va='center',fontsize=fs+5)
        yl -= self.lms.yStep*1.1
        xp = [self.lms.xMin + 3+self.lms.xStep*0.3*j for j in [0,9.25,11.0,11.8]]
        self.ax.text(xp[0]-1.5,yl, 'Rare+Common PRS  (', ha='left', va='center',fontsize=fs)
        self.ax.scatter(xp[1]+16.7,yl, marker='v', color=self.rc1, ec= 'k', s=555, zorder=5, clip_on=False)
        self.ax.scatter(xp[2]+16.25,yl, marker='^', color=self.rc1, ec= 'k', s=555, zorder=5, clip_on=False)
        self.ax.text(xp[3]+17.5,yl, ')', ha='left', va='center',fontsize=fs)
        return







 
    def label_recovery(self, CUTOFF=0.13, COMMAND='NA', EXTREME=False):   
        self.lms = DV.AxLims(self.ax, xt = [], yt = [], xlab = self.xLab, ylab = self.yLab, ystretch=0.5, xLim=[-1,101],fs = 45 )  
        pop, rec = self.T.vals['pop']['common-snp'], self.T.vals['recovery'] 
        R1, R2 = False, False 
        try: 
            if EXTREME: r1,r2= self.T.vals['recovery']['combo@0.1'].total1 , self.T.vals['recovery']['combo@0.1'].total2
            else:       r1,r2= self.T.vals['recovery']['combo'].total1 , self.T.vals['recovery']['combo'].total2
            if pop.e1 > 0 and pop.f1 and r1 > CUTOFF: R1 = True 
            if pop.e2 > 0 and pop.f2 and r2 > CUTOFF: R2 = True 
        except: pass 
        
        if not R1 and not R2: return 
        x1, x2 = self.X[0] - self.lms.xStep/2, self.X[-1] + self.lms.xStep/2
        yLo, yHi = self.lms.yMin + self.lms.yStep, self.lms.yMax - self.lms.yStep*5
        xLo, xHi = self.lms.xMid + self.lms.xStep, self.lms.xMid + self.lms.xStep * 3 
        
        if self.fs3 > 25:  astr = "fancy,head_width=20,head_length=20,tail_width=2"
        else:              astr = "fancy,head_width=1,head_length=1,tail_width=0.01"
        cs1,cs2 = "arc3,rad=-0.02", "arc3,rad=0.02"
        el = matplotlib.patches.Ellipse((50, yLo), 0, 0, angle=0, alpha=0.0,fc=None,ec='black',zorder=0,linewidth=0.1,fill=False)
        if R1: 
            if EXTREME:
                el2 = matplotlib.patches.Ellipse((-3, (self.z1+self.Ye[0])/2.0), 10, 4.5*self.lms.yStep, angle=0, alpha=1,fc='red',ec='black',linestyle='--',zorder=10,linewidth=self.lw3,fill=False)
                self.ax.add_patch(el2)
                AP=dict(arrowstyle=astr,linewidth=self.lw3,mutation_scale=2.0,color='k',patchB=el,shrinkB=0,connectionstyle=cs1)
                self.ax.annotate("",xy=(5, yLo+self.lms.yHop*2), xycoords='data',xytext=(55,yLo+self.lms.yHop),textcoords='data',arrowprops=AP)
            else: 
                el2 = matplotlib.patches.Ellipse((x1+self.lms.xStep*0.5, yLo+self.lms.yStep*2.0), 10,3.0*self.lms.yStep, angle=0, alpha=1,fc='red',ec='black',linestyle='--',zorder=10,linewidth=0.2,fill=False)
                self.ax.add_patch(el2)
                AP=dict(arrowstyle=astr,linewidth=self.lw3,mutation_scale=1.5,color='k',patchB=el,shrinkB=0,connectionstyle=cs1)
                self.ax.annotate("",xy=(xLo-self.lms.xStep*4.65, yLo+self.lms.yHop*4), xycoords='data',xytext=(xLo-self.lms.xStep,yLo+self.lms.yHop),textcoords='data',arrowprops=AP)
        if R2: 
            if EXTREME:
                el2 = matplotlib.patches.Ellipse((99+3, (self.z2+self.Ye[-1])/2.0), 10, self.lms.yStep + (self.Ye[-1]-self.z2), angle=0, alpha=1,fc='red',ec='black',linestyle='--',zorder=10,linewidth=self.lw3,fill=False)
                self.ax.add_patch(el2)
                AP=dict(arrowstyle=astr,linewidth=self.lw3,mutation_scale=2.0,color='k',patchB=el,shrinkB=0,connectionstyle=cs2)
                self.ax.annotate("",xy=(105, yHi-self.lms.yHop*2.5), xycoords='data',xytext=(97,yHi-3.3*self.lms.yStep),textcoords='data',arrowprops=AP)
            else: 
                el2 = matplotlib.patches.Ellipse((x2-self.lms.xStep*0.5, yLo+self.lms.yStep*5.5), 13, 3.5*self.lms.yStep, angle=0, alpha=1,fc='red',ec='black',linestyle='--',zorder=10,linewidth=0.2,fill=False)
                self.ax.add_patch(el2)
                AP=dict(arrowstyle=astr,linewidth=self.lw3,mutation_scale=1.5,color='k',patchB=el,shrinkB=0,connectionstyle=cs2)
                self.ax.annotate("",xy=(xHi+self.lms.xStep*1.8, yHi-self.lms.yHop*0.9), xycoords='data',xytext=(xHi+self.lms.xStep*1.35,yHi-2.6*self.lms.yStep),textcoords='data',arrowprops=AP)
        
        if not EXTREME: self.ax.text(xLo+self.lms.xStep*1.75,yLo+self.lms.yStep*0.75,'POPout\nReduction',fontsize=self.fs3,ha='center',va='center')
        elif not R1: self.ax.text(xLo+self.lms.xStep*1.75,yLo+self.lms.yStep*0.75,'POPout\nReduction\n(Upper 0.1%)',fontsize=self.fs3,ha='center',va='center')
        elif not R2: self.ax.text(xLo+self.lms.xStep*1.75,yLo+self.lms.yStep*0.75,'POPout\nReduction\n(Lower 0.1%)',fontsize=self.fs3,ha='center',va='center')
        else:        self.ax.text(xLo+self.lms.xStep*1.75,yLo+self.lms.yStep*0.75,'POPout\nReduction',fontsize=self.fs3,ha='center',va='center')
        return self



    def mark_significance(self, lw=1, fs=5): 
        
        self.lms = DV.AxLims(self.ax, xt = [], yt = [], xlab = self.xLab, ylab = self.yLab, ystretch=0.5, xstretch=0.75,fs = 6) 
        if self.type == 'common': 
            P = self.T.vals['pop']['common-snp'] 
            if P.p1 < 0.05 and P.e1 > 0: self.ax.scatter(self.X[0]-3, self.Y[0], color='gold', s= self.sz1, lw=0.4, marker='*', ec='k', zorder=15) 
            if P.p2 < 0.05 and P.e2 > 0: self.ax.scatter(self.X[-1]+3, self.Y[-1], color='gold', s= self.sz1, lw=0.4, marker='*', ec='k', zorder=15) 
        return self


    def label_popout(self): 
        self.lms = DV.AxLims(self.ax, xt = [], yt = [], xlab = self.xLab, ylab = self.yLab, ystretch=0.5, xstretch=0.75,fs = 8 ) 
        marks= "".join(self.markers[-2::]) 
        if marks == 'v^': return 
        x1, x2 = self.X[0] - self.lms.xStep/2, self.X[-1] + self.lms.xStep/2
        x1a, x1b, x2a, x2b = x1 - self.lms.xHop, x1 + self.lms.xHop, x2 - self.lms.xHop, x2 + self.lms.xHop 
        yLo, yHi = self.lms.yMin + self.lms.yStep, self.lms.yMax - self.lms.yStep*5
        xLo, xHi = self.lms.xMid + self.lms.xStep, self.lms.xMid + self.lms.xStep * 3 
        astr = "fancy,head_width=9.75,head_length=10"
        cs1 = "arc3,rad=-0.02"
        cs2 = "arc3,rad=0.02"
        el = matplotlib.patches.Ellipse((50, yLo), 0, 0, angle=0, alpha=0.0,fc=None,ec='black',zorder=0,linewidth=1,fill=False)
        if marks[0] == '^': 
            self.ax.plot([x1, x1], [self.Ye[0], self.Y[0]], lw = self.lw2, linestyle='--', color='gray') 
            self.ax.plot([x1a, x1b], [self.Ye[0], self.Ye[0]], lw =  self.lw2, linestyle='--', color='gray') 
            self.ax.plot([x1a, x1b], [self.Y[0], self.Y[0]], lw =  self.lw2, linestyle='--', color='gray') 
            AP=dict(arrowstyle=astr,linewidth=self.lw2,mutation_scale=0.20,color='k',patchB=el,shrinkB=0,connectionstyle=cs1)
            self.ax.annotate("",xy=(xLo-self.lms.xStep*2.5, yLo+self.lms.yHop*2.5), xycoords='data',xytext=(xLo+self.lms.xHop,yLo+1.5*self.lms.yHop),textcoords='data',arrowprops=AP)
        if marks[-1] == 'v': 
            self.ax.plot([x2, x2], [self.Ye[-1], self.Y[-1]], lw =  self.lw2, linestyle='--', color='gray') 
            self.ax.plot([x2a, x2b], [self.Ye[-1], self.Ye[-1]], lw =  self.lw2, linestyle='--', color='gray') 
            self.ax.plot([x2a, x2b], [self.Y[-1], self.Y[-1]], lw =  self.lw2, linestyle='--', color='gray') 
            AP=dict(arrowstyle=astr,linewidth=self.lw2,mutation_scale=0.20,color='k',patchB=el,shrinkB=0,connectionstyle=cs2)
            self.ax.annotate("",xy=(xHi+self.lms.xStep*1.0, yHi+self.lms.yHop*1.25), xycoords='data',xytext=(xHi+self.lms.xStep*0.5,yHi-2.5*self.lms.yStep),textcoords='data',arrowprops=AP)
        if marks == '^v':    self.ax.text(xLo+self.lms.xStep*1.5,yLo+self.lms.yStep*0.5,'Dual Tail\n$POPout$',fontsize=self.fs3,ha='center',va='center')
        elif marks == '^^': self.ax.text(xLo+self.lms.xStep*1.5,yLo+self.lms.yStep*0.5,'Lower Tail\n$POPout$',fontsize=self.fs3,ha='center',va='center')
        elif marks == 'vv': self.ax.text(xLo+self.lms.xStep*1.5,yLo+self.lms.yStep*0.5,'Upper Tail\n$POPout$',fontsize=self.fs3,ha='center',va='center')
        return self

    
    def label_popout_by_fdr(self,lw=1, fs=9, MINI=False): 
        try:    f1, f2 = self.T.vals['pop']['common-snp'].f1, self.T.vals['pop']['common-snp'].f2  
        except: return 
        if not f1 and not f2: return
        x1, x2 = self.X[0] - self.lms.xStep/2, self.X[-1] + self.lms.xStep/2
        x1a, x1b, x2a, x2b = x1 - self.lms.xHop, x1 + self.lms.xHop, x2 - self.lms.xHop, x2 + self.lms.xHop 
        yLo, yHi = self.lms.yMin + self.lms.yStep, self.lms.yMax - self.lms.yStep*5
        xLo, xHi = self.lms.xMid + self.lms.xStep, self.lms.xMid + self.lms.xStep * 3 
        cs1 = "arc3,rad=-0.02"
        cs2 = "arc3,rad=0.02"
        el = matplotlib.patches.Ellipse((50, yLo), 0, 0, angle=0, alpha=0.0,fc=None,ec='black',zorder=0,linewidth=1,fill=False)
        if MINI: 
            astr = "fancy,head_width=2,head_length=1"
            if f1 or f2: 
                self.ax.text(xLo+self.lms.xStep*0.9,yLo+self.lms.yStep*0.85,'Tail\n$POPout$',fontsize=5,ha='center',va='center')
            if f1:  
                AP=dict(arrowstyle=astr,linewidth=0.3,mutation_scale=0.5,color='k',patchB=el,shrinkB=0,connectionstyle=cs1)
                self.ax.annotate("",xy=(xLo-self.lms.xStep*3.8, yLo+self.lms.yHop*2), xycoords='data',xytext=(xLo-8*self.lms.xHop,yLo),textcoords='data',arrowprops=AP)
            if f2:  
                AP=dict(arrowstyle=astr,linewidth=0.3,mutation_scale=0.5,color='k',patchB=el,shrinkB=0,connectionstyle=cs2)
                self.ax.annotate("",xy=(xHi+self.lms.xStep*0.9, yHi+self.lms.yHop*3.3), xycoords='data',xytext=(xHi+self.lms.xStep*0.50,yHi-2.6*self.lms.yStep),textcoords='data',arrowprops=AP)
            return self 
        astr = "fancy,head_width=9.75,head_length=10"
        if f1:  
            self.ax.plot([x1, x1], [self.Ye[0], self.Y[0]], lw =  lw, linestyle='--', color='gray') 
            self.ax.plot([x1a, x1b], [self.Ye[0], self.Ye[0]], lw =  lw, linestyle='--', color='gray') 
            self.ax.plot([x1a, x1b], [self.Y[0], self.Y[0]], lw =  lw, linestyle='--', color='gray') 
            AP=dict(arrowstyle=astr,linewidth=lw,mutation_scale=0.5,color='k',patchB=el,shrinkB=0,connectionstyle=cs1)
            self.ax.annotate("",xy=(xLo-self.lms.xStep*3.5, yLo+self.lms.yHop), xycoords='data',xytext=(xLo-8*self.lms.xHop,yLo),textcoords='data',arrowprops=AP)
        if f2:  
            self.ax.plot([x2, x2], [self.Ye[-1], self.Y[-1]], lw =  lw, linestyle='--', color='gray') 
            self.ax.plot([x2a, x2b], [self.Ye[-1], self.Ye[-1]], lw =  lw, linestyle='--', color='gray') 
            self.ax.plot([x2a, x2b], [self.Y[-1], self.Y[-1]], lw =  lw, linestyle='--', color='gray') 
            AP=dict(arrowstyle=astr,linewidth=lw,mutation_scale=0.5,color='k',patchB=el,shrinkB=0,connectionstyle=cs2)
            self.ax.annotate("",xy=(xHi+self.lms.xStep*1.2, yHi+self.lms.yHop*3), xycoords='data',xytext=(xHi+self.lms.xStep*0.8,yHi-1.5*self.lms.yStep),textcoords='data',arrowprops=AP)
        if f1 and f2:    self.ax.text(xLo+self.lms.xStep*1.5,yLo+self.lms.yStep*0.5,'Dual Tail\n$POPout$',fontsize=fs+3,ha='center',va='center')
        elif f1: self.ax.text(xLo+self.lms.xStep*1.5,yLo+self.lms.yStep*0.5,'Lower Tail\n$POPout$',fontsize=fs+3,ha='center',va='center')
        elif f2: self.ax.text(xLo+self.lms.xStep*1.5,yLo+self.lms.yStep*0.5,'Upper Tail\n$POPout$',fontsize=fs+3,ha='center',va='center')
        return self

    


    def label_reps(self, lw=0.4, fs=5): 
        if self.NULL or not self.VALID: 
            self.lms = DV.AxLims(self.ax, xt = [], yt = [], xlab = self.xLab, ylab = self.yLab, ystretch=0.5, xstretch=0.75,fs = 45 ) 
            return 
        self.lms = DV.AxLims(self.ax, xt = [], yt = [], xlab = self.xLab, ylab = self.yLab, ystretch=0.5, xstretch=0.75,fs = 45 ) 
        p1, p2 = self.T.vals['pop']['common-snp'].p1,self.T.vals['pop']['common-snp'].p2 
        e1, e2 = self.T.vals['pop']['common-snp'].e1,self.T.vals['pop']['common-snp'].e2 
        
        if (e1 > 0 and p1 < 0.03) and (e2 >0 and p2 < 0.03): TYPE = 'Dual' 
        elif p1 < 0.00005:             TYPE = 'Lower' 
        elif p2 < 0.00005:             TYPE = 'Upper'
        else:                       return 

        if min(p1,p2)*100000000000  > 0.05:  SCALE='Moderate\n$POPout$' 
        else:                                SCALE=TYPE+' Tail\n$POPout$' 

        x1, x2 = self.X[0] - self.lms.xStep/2, self.X[-1] + self.lms.xStep/2
        x1a, x1b, x2a, x2b = x1 - self.lms.xHop, x1 + self.lms.xHop, x2 - self.lms.xHop, x2 + self.lms.xHop 
        yLo, yHi = self.lms.yMin + self.lms.yStep, self.lms.yMax - self.lms.yStep*5
        xLo, xHi = self.lms.xMid + self.lms.xStep, self.lms.xMid + self.lms.xStep * 3 
        astr = "fancy,head_width=2,head_length=1.3"
        cs1 = "arc3,rad=-0.02"
        cs2 = "arc3,rad=0.02"
        el = matplotlib.patches.Ellipse((50, yLo), 0, 0, angle=0, alpha=0.0,fc=None,ec='black',zorder=0,linewidth=1,fill=False)
        if TYPE in ['Dual','Lower']: 
            AP=dict(arrowstyle=astr,linewidth=lw,mutation_scale=1.3,color='k',patchB=el,shrinkB=0,connectionstyle=cs1)
            self.ax.annotate("",xy=(xLo-self.lms.xStep*3.5, yLo+self.lms.yHop*2.5), xycoords='data',xytext=(xLo-self.lms.xHop,yLo+1.5*self.lms.yHop),textcoords='data',arrowprops=AP)
        if TYPE in ['Dual','Upper']: 
            AP=dict(arrowstyle=astr,linewidth=lw,mutation_scale=1.3,color='k',patchB=el,shrinkB=0,connectionstyle=cs2)
            self.ax.annotate("",xy=(xHi+self.lms.xStep*1.0, yHi+self.lms.yHop*1.25), xycoords='data',xytext=(xHi+self.lms.xStep*0.5,yHi-2.5*self.lms.yStep),textcoords='data',arrowprops=AP)
        self.ax.text(xLo+self.lms.xStep*1.5,yLo+self.lms.yStep*0.5,SCALE,fontsize=fs,ha='center',va='center')
        return





























class SibPlot:
    def __init__(self,ax,fig,ti,xLab=None,yLab=None,alp=0.5,lw1=1,lw2=0.5,lw3=0.2,sz1=16,sz2=10,sz3=6,fs1=7.5,fs2=6,fs3=5,INIT=False): 
        self.ax, self.fig, self.xLab, self.yLab, self.alp, self.INIT = ax, fig, xLab, yLab, alp, INIT 
        self.lw1,self.lw2,self.lw3 =lw1,lw2,lw3
        self.sz1,self.sz2,self.sz3 =sz1,sz2,sz3 
        self.fs1,self.fs2,self.fs3 =fs1,fs2,fs3    
        if ti in fig.traits: 
            self.T, self.VALID = fig.traits[ti], True 
            if 'sib' in self.T.pts and 'sib' in self.T.vals: self.NULL = False 
            else:                                             self.NULL = True 
        else:            
            self.VALID, self.NULL, self.T =  False, True, 'NA' 


    def draw_sib_pair(self,idx=9, clr1 = 'mediumblue', clr2='darkorange', clr3='mediumblue',LABEL=False, MINI=False): 
        if self.NULL: 
            DV.draw_blank(self.ax) 
            return 
        P = self.T.pts['sib'] 
        self.X, Y1, self.Y, self.se = P.X, P.sib1, P.sib2, P.se 
        self.Ye = [y*self.T.vals['sib'].h2_bod/2.0 for y in Y1] 
        #self.ax.plot(self.X[1:99], self.Ye[1:99], color=clr2, lw = self.lw1, zorder=0)
        self.ax.plot(self.X, self.Ye, color=clr2, lw = self.lw1, zorder=0)
        self.ax.scatter(self.X[1:99], self.Y[1:99], color=clr1, edgecolor = clr1, zorder=1,alpha=self.alp, s = self.sz2, lw=0.3) 
        self.markers = [] 
        for j,(x1,x2,clr,Z,sz) in enumerate([[0,1,clr2,self.Ye,100],[-1,-2,clr2,self.Ye,100],[0,1,clr3,self.Y,300],[-1,-2,clr3,self.Y,300]]): 
            if Z[x1] > Z[x2]: self.markers.append('^') 
            else:             self.markers.append('v') 
            if j < 2: self.ax.scatter(self.X[x1], Z[x1], marker=self.markers[-1], color=clr, zorder=0, s= self.sz3) 
            else:     self.ax.scatter(self.X[x1], Z[x1], marker=self.markers[-1], color=clr, zorder=4, ec = 'k', lw=0.2, s= self.sz1) 
        xLab, yLab = None, None 
        

        self.ax.set_title(self.T.name.cornerStyle, fontsize = self.fs1, loc='left', x=0.012, y= 0.90,va='top')  
        if idx in [0,2]: yLab = 'Cond. Sibling Trait (z)' 
        if idx in [2,3]: xLab = 'Index Sibling Centile' 
        self.lms = DV.AxLims(self.ax, xt = [], yt = [], xlab = xLab, ylab = yLab, ystretch=0.5, xstretch=0.75,fs = self.fs2) 
        if LABEL: self.label_sibs("".join(self.markers[-2::])) 
        if self.fig.progress.SAVESRC: self.save_sib() 
        return


    def save_sib(self): 
        w = self.fig.progress.out3
        if self.INIT: w.write('%s,%s,%s,%s\n' % ('Panel', 'Trait-ID','Data','Values')) 
        Xs = ";".join([str(x) for x in self.X]) 
        Ys = ";".join([str(x) for x in self.Y]) 
        Ye = ";".join([str(x) for x in self.Ye]) 
        w = self.fig.progress.out3
        w.write('%s,%s,%s,%s\n' % (self.fig.progress.panel,self.T.id,'Index-Sib-Centiles',Xs)) 
        w.write('%s,%s,%s,%s\n' % (self.fig.progress.panel,self.T.id,'Observed-Conditional-Sib',Ys)) 
        w.write('%s,%s,%s,%s\n' % (self.fig.progress.panel,self.T.id,'Expected-Conditional-Sib',Ye)) 
        return






    def draw_alt(self,p_type,yc1='blue',yc2='blue',ec1='orange',ec2='darkorange',rc1='xkcd:shamrock green',rc2='lime',alp=1,tailType='STANDARD', ALLOW_MISSING=False):  
        self.type, self.tailType, self.yc1, self.yc2, self.ec1, self.ec2, self.rc1, self.rc2 = p_type, tailType, yc1, yc2, ec1, ec2, rc1, rc2 




    
    def label_sibs(self, marks): 
        if marks == 'v^': return 
        x1, x2 = self.X[0] - self.lms.xStep/2, self.X[-1] + self.lms.xStep/2
        x1a, x1b, x2a, x2b = x1 - self.lms.xHop*1.2, x1 + self.lms.xHop*1.2, x2 - self.lms.xHop*1.2, x2 + self.lms.xHop*1.2
        yLo, yHi = self.lms.yMin + self.lms.yStep, self.lms.yMax - self.lms.yStep*5
        xLo, xHi = self.lms.xMid + self.lms.xStep, self.lms.xMid + self.lms.xStep * 3 
        astr = "fancy,head_width=2.75,head_length=2,tail_width=0.5"
        cs1 = "arc3,rad=-0.02"
        cs2 = "arc3,rad=0.02"
        el = matplotlib.patches.Ellipse((50, yLo), 0, 0, angle=0, alpha=0.0,fc=None,ec='black',zorder=0,linewidth=1,fill=False)
        if marks[0] == '^': 
            self.ax.plot([x1, x1], [self.Ye[0], self.Y[0]], lw =  self.lw2, linestyle='--', color='gray') 
            self.ax.plot([x1a, x1b], [self.Ye[0], self.Ye[0]], lw =  self.lw2, linestyle='--', color='gray') 
            self.ax.plot([x1a, x1b], [self.Y[0], self.Y[0]], lw =  self.lw2, linestyle='--', color='gray') 
            AP=dict(arrowstyle=astr,linewidth=self.lw3,mutation_scale=1.0,color='k',patchB=el,shrinkB=0,connectionstyle=cs1)
            self.ax.annotate("",xy=(xLo-self.lms.xStep*3.9, yLo+self.lms.yHop*2), xycoords='data',xytext=(xLo-3*self.lms.xHop,yLo+2.5*self.lms.yHop),textcoords='data',arrowprops=AP)
        if marks[-1] == 'v': 
            self.ax.plot([x2, x2], [self.Ye[-1], self.Y[-1]], lw =  self.lw2, linestyle='--', color='gray') 
            self.ax.plot([x2a, x2b], [self.Ye[-1], self.Ye[-1]], lw =  self.lw2, linestyle='--', color='gray') 
            self.ax.plot([x2a, x2b], [self.Y[-1], self.Y[-1]], lw =  self.lw2, linestyle='--', color='gray') 
            AP=dict(arrowstyle=astr,linewidth=self.lw3,mutation_scale=1.0,color='k',patchB=el,shrinkB=0,connectionstyle=cs2)
            self.ax.annotate("",xy=(xHi+self.lms.xStep*1.2, yHi+self.lms.yHop*7), xycoords='data',xytext=(xHi+self.lms.xStep*0.5,yHi-2.1*self.lms.yStep),textcoords='data',arrowprops=AP)
        if marks == '^v':    self.ax.text(xLo+self.lms.xStep*1.5,yLo+self.lms.yStep*0.75,'Dual Tail\n$STANDout$',fontsize=self.fs2,ha='center',va='center')
        elif marks == '^^': self.ax.text(xLo+self.lms.xStep*1.5,yLo+self.lms.yStep*0.75,'Lower Tail\n$STANDout$',fontsize=self.fs2,ha='center',va='center')
        elif marks == 'vv': self.ax.text(xLo+self.lms.xStep*1.5,yLo+self.lms.yStep*0.75,'Upper Tail\n$STANDout$',fontsize=self.fs2,ha='center',va='center')
        return

    def smart_sib_labels(self, meta1, meta2, fs=20, lw=2): 
        x1, x2 = self.X[0] - self.lms.xStep/2, self.X[-1] + self.lms.xStep/2
        x1a, x1b, x2a, x2b = x1 - self.lms.xHop, x1 + self.lms.xHop, x2 - self.lms.xHop, x2 + self.lms.xHop 
        yLo, yHi = self.lms.yMin + self.lms.yStep, self.lms.yMax - self.lms.yStep*5
        xLo, xHi = self.lms.xMid + self.lms.xStep*0.5, self.lms.xMid + self.lms.xStep * 3 
        astr = "fancy,head_width=9.75,head_length=10"
        cs1 = "arc3,rad=-0.02"
        cs2 = "arc3,rad=0.02"
        el = matplotlib.patches.Ellipse((50, yLo), 0, 0, angle=0, alpha=0.0,fc=None,ec='black',zorder=0,linewidth=1,fill=False)
        if meta1 < 0.05: 
            self.ax.plot([x1, x1], [self.Ye[0], self.Y[0]], lw =  self.lw2, linestyle='--', color='gray') 
            self.ax.plot([x1a, x1b], [self.Ye[0], self.Ye[0]], lw =  self.lw2, linestyle='--', color='gray') 
            self.ax.plot([x1a, x1b], [self.Y[0], self.Y[0]], lw =  self.lw2, linestyle='--', color='gray') 
            AP=dict(arrowstyle=astr,linewidth=self.lw2,mutation_scale=0.5,color='k',patchB=el,shrinkB=0,connectionstyle=cs1)
            self.ax.annotate("",xy=(xLo-self.lms.xStep*3.86, yLo+self.lms.yHop*2), xycoords='data',xytext=(xLo-self.lms.xStep*1.9,yLo+self.lms.yHop),textcoords='data',arrowprops=AP)
        if meta2 < 0.05: 
            self.ax.plot([x2, x2], [self.Ye[-1], self.Y[-1]], lw =  self.lw2, linestyle='--', color='gray') 
            self.ax.plot([x2a, x2b], [self.Ye[-1], self.Ye[-1]], lw =  self.lw2, linestyle='--', color='gray') 
            self.ax.plot([x2a, x2b], [self.Y[-1], self.Y[-1]], lw =  self.lw2, linestyle='--', color='gray') 
            AP=dict(arrowstyle=astr,linewidth=self.lw2,mutation_scale=0.5,color='k',patchB=el,shrinkB=0,connectionstyle=cs2)
            self.ax.annotate("",xy=(xHi+self.lms.xStep*1.3, yHi+self.lms.yHop*5), xycoords='data',xytext=(xHi+self.lms.xStep*1.0,yHi-1.75*self.lms.yStep),textcoords='data',arrowprops=AP)
        self.ax.text(xLo+self.lms.xStep*1.5,yLo+self.lms.yStep*0.75,'Sibling\n$STANDout$',fontsize=self.fs2,ha='center',va='center')
        return
    



    

    def draw_mini_sib_pair(self,idx=9, clr1 = 'mediumblue', clr2='xkcd:sunflower', clr3='mediumblue',LABEL=False, MINI=False): 
        if self.NULL: 
            DV.draw_blank(self.ax) 
            return 
        P = self.T.pts['sib'] 
        self.X, Y1, self.Y, self.se = P.X, P.sib1, P.sib2, P.se 
        self.Ye = [y*self.T.vals['sib'].h2_bod/2.0 for y in Y1] 
        self.ax.plot(self.X[1:99], self.Ye[1:99], color=clr2, lw = self.lw1, zorder=0)

        self.ax.scatter(self.X[1:99], self.Y[1:99], color=clr1, edgecolor = clr1, zorder=1,alpha=0.5, s = self.sz3-0.5, lw=0.2) 
        self.markers = [] 
        for j,(x1,x2,clr,Z,sz) in enumerate([[0,1,clr2,self.Ye,100],[-1,-2,clr2,self.Ye,100],[0,1,clr3,self.Y,300],[-1,-2,clr3,self.Y,300]]): 
            if Z[x1] > Z[x2]: self.markers.append('^') 
            else:             self.markers.append('v') 
            if j < 2: self.ax.scatter(self.X[x1], Z[x1], marker=self.markers[-1], color=clr, zorder=0, ec = 'k', lw=0.2, s= self.sz3) 
            else:     self.ax.scatter(self.X[x1], Z[x1], marker=self.markers[-1], color=clr, zorder=4, ec = 'k', lw=0.2, s= self.sz2) 
        xLab, yLab = None, None 
        
        
        self.lms = DV.AxLims(self.ax, xt = [], yt = [], xlab = xLab, ylab = yLab, xstretch = [0.5,1.1], ystretch = [1.5,0.5], fs = 10)
        f1, f2 = self.T.vals['pop']['common-snp'].f1, self.T.vals['pop']['common-snp'].f2  
        m1, m2 = self.T.vals['sib'].meta1, self.T.vals['sib'].meta2 
        if self.fig.progress.SAVESRC: self.save_sib() 
        if self.T.vals['sib'].h2_bod > 0.45 and self.T.qc['sampleSize'].sibs > 5500 and (m1 < 0.005 or m2 < 0.005): STAND = True 
        elif (f1 and m1 < 0.05) or (f2 and m2<0.05): STAND = True  
        else: return 
        x1, x2 = self.X[0] - self.lms.xStep/2, self.X[-1] + self.lms.xStep/2
        x1a, x1b, x2a, x2b = x1 - self.lms.xHop, x1 + self.lms.xHop, x2 - self.lms.xHop, x2 + self.lms.xHop 
        yLo, yHi = self.lms.yMin + self.lms.yStep, self.lms.yMax - self.lms.yStep*5
        xLo, xHi = self.lms.xMid + self.lms.xStep*0.5, self.lms.xMid + self.lms.xStep * 3 
        astr = "fancy,head_width=1.5,head_length=2"
        cs1 = "arc3,rad=-0.02"
        cs2 = "arc3,rad=0.02"
        el = matplotlib.patches.Ellipse((50, yLo), 0, 0, angle=0, alpha=0.0,fc=None,ec='black',zorder=0,linewidth=1,fill=False)
        if m1 < 0.05: 
            AP=dict(arrowstyle=astr,linewidth=0.4,mutation_scale=0.5,color='k',patchB=el,shrinkB=0,connectionstyle=cs1)
            self.ax.annotate("",xy=(xLo-self.lms.xStep*3.86, yLo+self.lms.yHop*2), xycoords='data',xytext=(xLo-self.lms.xStep*1.9,yLo+self.lms.yHop),textcoords='data',arrowprops=AP)
        if m2 < 0.05: 
            AP=dict(arrowstyle=astr,linewidth=0.4,mutation_scale=0.5,color='k',patchB=el,shrinkB=0,connectionstyle=cs2)
            self.ax.annotate("",xy=(xHi+self.lms.xStep*1.3, yHi+self.lms.yHop*5), xycoords='data',xytext=(xHi+self.lms.xStep*1.0,yHi-1.75*self.lms.yStep),textcoords='data',arrowprops=AP)
        
        

        self.ax.text(self.lms.xMax-self.lms.xHop/2.0,self.lms.yMin+self.lms.yHop/10.0,'Sibling\n$STANDout$',fontsize=4.5,ha='right',va='bottom')
        return
    







    def smart_sib_labels(self, meta1, meta2, fs=20, lw=2): 
        x1, x2 = self.X[0] - self.lms.xStep/2, self.X[-1] + self.lms.xStep/2
        x1a, x1b, x2a, x2b = x1 - self.lms.xHop, x1 + self.lms.xHop, x2 - self.lms.xHop, x2 + self.lms.xHop 
        yLo, yHi = self.lms.yMin + self.lms.yStep, self.lms.yMax - self.lms.yStep*5
        xLo, xHi = self.lms.xMid + self.lms.xStep*0.5, self.lms.xMid + self.lms.xStep * 3 
        astr = "fancy,head_width=9.75,head_length=10"
        cs1 = "arc3,rad=-0.02"
        cs2 = "arc3,rad=0.02"
        el = matplotlib.patches.Ellipse((50, yLo), 0, 0, angle=0, alpha=0.0,fc=None,ec='black',zorder=0,linewidth=1,fill=False)
        if meta1 < 0.05: 
            self.ax.plot([x1, x1], [self.Ye[0], self.Y[0]], lw =  self.lw2, linestyle='--', color='gray') 
            self.ax.plot([x1a, x1b], [self.Ye[0], self.Ye[0]], lw =  self.lw2, linestyle='--', color='gray') 
            self.ax.plot([x1a, x1b], [self.Y[0], self.Y[0]], lw =  self.lw2, linestyle='--', color='gray') 
            AP=dict(arrowstyle=astr,linewidth=self.lw2,mutation_scale=0.5,color='k',patchB=el,shrinkB=0,connectionstyle=cs1)
            self.ax.annotate("",xy=(xLo-self.lms.xStep*3.86, yLo+self.lms.yHop*2), xycoords='data',xytext=(xLo-self.lms.xStep*1.9,yLo+self.lms.yHop),textcoords='data',arrowprops=AP)
        if meta2 < 0.05: 
            self.ax.plot([x2, x2], [self.Ye[-1], self.Y[-1]], lw =  self.lw2, linestyle='--', color='gray') 
            self.ax.plot([x2a, x2b], [self.Ye[-1], self.Ye[-1]], lw =  self.lw2, linestyle='--', color='gray') 
            self.ax.plot([x2a, x2b], [self.Y[-1], self.Y[-1]], lw =  self.lw2, linestyle='--', color='gray') 
            AP=dict(arrowstyle=astr,linewidth=self.lw2,mutation_scale=0.5,color='k',patchB=el,shrinkB=0,connectionstyle=cs2)
            self.ax.annotate("",xy=(xHi+self.lms.xStep*1.3, yHi+self.lms.yHop*5), xycoords='data',xytext=(xHi+self.lms.xStep*1.0,yHi-1.75*self.lms.yStep),textcoords='data',arrowprops=AP)
        self.ax.text(xLo+self.lms.xStep*1.5,yLo+self.lms.yStep*0.75,'Sibling\n$STANDout$',fontsize=self.fs2,ha='center',va='center')
        return
    






###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################
###############################################################################################################################################
        

