import sys, os 
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path: sys.path.insert(0, HERE)
from Util import * 
import drawVarious as DV 
import drawScatter as DS

        

class EvoPlot:
    def __init__(self, fig):
        self.fig, self.traits, self.data, self.options, self.progress = fig, fig.traits, fig.data, fig.options, fig.progress 
        self.CI = True 
        self.inherit_settings(fig) 

    def inherit_settings(self, fig): 
        for v in ['fs0','fs1','fs2','fs3','fs4','fs5','lw1','lw2','lw3','sz1','sz2','sz3']: 
            if v in vars(fig): vars(self)[v] = vars(fig)[v] 
            elif v[0:2] == 'lw': vars(self)[v] = 1 
            else:                vars(self)[v] = 10 
    
    def classify(self, ALT=False): 
        self.evo_cnts, self.evo_groups = dd(int), dd(lambda: dd(list)) 
        for ti,T in self.traits.items(): 
            if T.group == 'Questionnaire/Cognitive': grp = 'Cog' 
            else:                                    grp = T.group 
            if ALT == False: n,k = self.classify_top_trait_model(T) 
            else: 
                if str(T.vals['lrs'].altbool) == 'False': n,k = self.classify_top_trait_model(T) 
                else:                                     n,k = self.classify_alt_trait_model(T) 
            self.evo_groups[n][k].append([grp,T]) 
        self.evo_cnts['none'] = len(self.evo_groups[0]['linear']) 
        self.evo_cnts['pos'] = sum([len(V) for V in self.evo_groups[1].values()])
        self.evo_cnts['neg'] = sum([len(V) for V in self.evo_groups[2].values()])
        self.evo_cnts['stabilising']          = len([T for T in self.traits.values() if T.vals['lrs'].evo.split('-')[-1] == 'stabilising']) 
        return
   

    def classify_top_trait_model(self, T): 
        if   T.vals['lrs'].evo.split('-')[0]   == 'neg': n = 2 
        elif T.vals['lrs'].evo.split('-')[0]   == 'pos': n = 1 
        else:                                            n = 0 
        if T.vals['lrs'].evo.split('-')[-1] not in ['stabilising','diverging']: k = 'linear' 
        else:
            if n == 0: k = 'quadratic' 
            elif T.vals['lrs'].evo.split('-')[-1] == 'diverging': k = 'diverging' 
            else:                                                 k = 'stabilising' 
        return n,k 
    
    def classify_alt_trait_model(self,T): 
        model, signs = T.vals['lrs'].altmodel, ['NA','NA'] 
        betas = [T.vals['lrs'].key[b] for b in ['altbeta0','altbeta1','altbeta2']]
        for i,b in enumerate(betas[1::]): 
            if b != 'NA' and b > 0:   signs[i] = '+' 
            elif b != 'NA' and b < 0: signs[i] = '-' 
        if model == 'Y~yInt': 
            return 0,'linear' 
        elif model == 'Y~yInt+X': 
            if signs[0] == '+': return 1, 'linear' 
            else:               return 2, 'linear' 
        elif model == 'Y~yInt+X+X2':
            if signs[0] == '+': n = 1 
            else:               n = 2 
            if signs[1] == '+': k = 'diverging' 
            else:               k = 'stabilising' 
            return n,k 
        else:
            return 0,'quadratic' 



    def plot_boxes(self, mc = 'k',lw=2,lc='blue',fs1=42):         
        my_index, self.axes, keep = self.fig.ax_index, self.fig.axes, [] 
        labels = ['No Selection\n('+str(self.evo_cnts['none'])+' Traits)\n$(\\beta=0,\gamma=0)$']
        labels.append('Stabilising\n('+str(self.evo_cnts['stabilising'])+' Traits)\n$(\\gamma<0)$')  
        labels.append('Positive\nDirectional\n('+str(self.evo_cnts['pos'])+' Traits)\n$(\\beta>0)$') 
        labels.append('Negative\nDirectional\n('+str(self.evo_cnts['neg'])+' Traits)\n$(\\beta<0)$')
        r_data = [[30810, 20016, 3143, 3536], [20015,30770, 3148, 23099], [30070, 20023, 4194, 30740], [30020, 46, 3581, 23105]] 
        t_none = [ti for ti,T in self.traits.items() if T.vals['lrs'].evo == 'none'] 
        for i,rd in enumerate(r_data): 
            t_all = [ti for ti in self.traits.keys()]
            if not all([ti in self.traits for ti in rd]): 
                r_kept = [ti for ti in rd if ti in self.traits] 
                if i == 0: t_cands = [ti for ti,T in self.traits.items() if T.vals['lrs'].evo == 'none'] 
                elif i == 1: t_cands = [ti for ti,T in self.traits.items() if T.vals['lrs'].evo == 'stabilising'] 
                elif i == 2: t_cands = [ti for ti,T in self.traits.items() if T.vals['lrs'].evo[0:3] == 'pos'] 
                else: t_cands = [ti for ti,T in self.traits.items() if T.vals['lrs'].evo[0:3] == 'neg'] 
                rd_tmp = r_kept + [ti for ti in t_cands if ti not in rd] + rd + rd + rd + t_all 
                r_data[i] = rd_tmp[0:4] 
        for j,rpd in enumerate(r_data):
            lms_res =  [DS.draw_evo(self.axes[my_index+i], self.traits[ti], fs=self.fs4,lw=self.lw3,sz=self.sz1,NOTES=[j, i]) for i,ti in enumerate(rpd[0:4])] 
            for i,lms in enumerate(lms_res):  
                ax = self.axes[my_index+i] 
                if i == 0:  
                    if j < 3: ax.set_title(labels[j],zorder=2,fontsize=self.fs4,y=0.98,fontweight='bold') 
                    else:     ax.set_title(labels[j],zorder=2,fontsize=self.fs4,y=0.98,fontweight='bold') 
                ax.plot([lms.xMin, lms.xMin],[lms.yMax, lms.yMin], clip_on=False, color=mc,linewidth=self.lw3,zorder=10) 
                ax.plot([lms.xMax, lms.xMax],[lms.yMax, lms.yMin], clip_on=False, color=mc,linewidth=self.lw3,zorder=10) 
                if i == 0:   ax.plot([lms.xMin, lms.xMax],[lms.yMax, lms.yMax], clip_on=False, color=mc,linewidth=self.lw3,zorder=10) 
                elif i == 3:   ax.plot([lms.xMin, lms.xMax],[lms.yMin, lms.yMin], clip_on=False, color=mc,linewidth=self.lw3,zorder=10) 
                else: 
                    ax.plot([lms.xMin, lms.xMin],[lms.yMin - lms.yStep, lms.yMax+lms.yStep*0.5], clip_on=False, color=mc,linewidth=self.lw3,zorder=2) 
                    ax.plot([lms.xMax, lms.xMax],[lms.yMin - lms.yStep, lms.yMax+lms.yStep*0.5], clip_on=False, color=mc,linewidth=self.lw3,zorder=2) 
                if rpd[i] in self.options.indexTraits: keep.append([ax, lms, i, j]) 
            my_index += 4  
        for ax, lms, i, j in keep: 
            ax.plot([lms.xMin, lms.xMax],[lms.yMin, lms.yMin], clip_on=False, color='blue',linewidth=self.lw2,zorder=33) 
            ax.plot([lms.xMin, lms.xMax],[lms.yMax, lms.yMax], clip_on=False, color='blue',linewidth=self.lw2,zorder=33) 
            ax.plot([lms.xMin, lms.xMin],[lms.yMin, lms.yMax], clip_on=False, color='blue',linewidth=self.lw2,zorder=33) 
            ax.plot([lms.xMax, lms.xMax],[lms.yMax, lms.yMin], clip_on=False, color='blue',linewidth=self.lw2,zorder=33) 
        return 
        


    def quick_add(self, ax, yp, T, ht=0.23, LR=0.015, baf=0.85): 
        clr = T.group_color 
        pop = T.vals['pop']['common-snp'] 
        pLo, pHi, eLo, eHi = pop.p1, pop.p2, pop.e1, pop.e2 
        self.scorekeep['lo'].append(eLo)  
        self.scorekeep['hi'].append(eHi) 
        if eLo < 0:              ax.barh(yp,-0.01,left=-1*LR,height=ht,color=clr,clip_on=False,alpha=baf) 
        else: 
            if pop.f1:  cx, ex = clr, 'k'
            else:       cx, ex = 'white', clr
            ax.barh(yp,-1*eLo,left=-1*LR,height=ht,color=cx, ec=ex,clip_on=False,lw=0.33,alpha=baf) 
            if self.CI:
                z1,z2=eLo-pop.j1, eLo+pop.j1 
                ax.plot([min(-LR,-1*LR-z1),-1*LR-z2],[yp,yp],color='k',lw=0.7,clip_on=False) 
                ax.plot([min(-LR,-1*LR-z1),-1*LR-z2],[yp,yp],color=clr,lw=0.5,clip_on=False) 
        if eHi < 0: 
            ax.barh(yp,0.01,left=LR,height=ht,color=clr,clip_on=False,alpha=baf) 
        else: 
            if pop.f2:  cx, ex = clr, 'k'
            else:       cx, ex = 'white', clr
            ax.barh(yp,eHi,left=LR,height=ht,color=cx,ec=ex,lw=0.33,clip_on=False,alpha=baf) 
            
            if self.CI: 
                z1,z2=eHi-pop.j1, eHi+pop.j1 
                ax.plot([max(LR,LR+z1),LR+z2],[yp,yp],color='k',lw=0.7,clip_on=False) 
                ax.plot([max(LR,LR+z1),LR+z2],[yp,yp],color=clr,lw=0.5,clip_on=False) 
        return yp - 0.3




    def add_arrows(self, ax,yp,INIT=False, END=False): 
         ax.arrow(0.01, yp,   0.51, 0, linewidth=self.lw2, head_width=0.2, head_length=0.03, fc='k', ec='k',clip_on=False,zorder=0)     
         ax.arrow(-0.01, yp,  -0.51, 0, linewidth=self.lw2, head_width=0.2, head_length=0.03, fc='k', ec='k',clip_on=False,zorder=0)     
         for p in [0,-0.5,0.5]: 
             if p == -0.5: ax.text(p,yp-0.2,str(0.5),va='top',ha='center',fontsize=self.fs5) 
             else:         ax.text(p,yp-0.2,str(p),va='top',ha='center',fontsize=self.fs5) 
             ax.text(p,yp-0.03,'I',ha='center',va='center',fontsize=self.fs5) 
         return
     




    def add_group_means(self, ax, yp, label, xj = 0.4, yj = 0.4, BH=0.45, LR=0.015, lw=0.5): 
        ax.text(0,yp-yj/2.0,'Category Means',ha='center',va='center',fontsize=self.fs5,fontweight='bold') 
        ax.plot([-xj,xj],[yp-yj,yp-yj], linestyle='--',color='k', lw=self.lw2) 
        Ts, pv = stats.ttest_ind(self.scorekeep['lo'], self.scorekeep['hi']) 
        
        xL,xLL,xLH = mean_ci(self.scorekeep['lo']) 
        xR,xRL,xRH = mean_ci(self.scorekeep['hi']) 
        yp -= BH * 1.6 
        ax.plot([0,0],[yp-0.2,yp+0.3],color='k',lw=lw)  
        mss = str(round(xL,3))+'/'+str(round(xR,3))  
        res = 'POPout Effect Stratified by '+label.split('\n')[0]+': Lower/Upper Means: '+mss+', pv='+str(pv)  
        if not self.PRINTPV: self.progress.report_result(res)  
        if pv < 0.05:
            if xL > xR:  
                ax.barh(yp,-1*xL,left=-LR,height=BH,color='dimgrey',alpha=0.85,clip_on=False,lw=lw,ec='k') 
                ax.barh(yp,xR,left=LR,height=BH,color='white',clip_on=False,lw=lw,ec='k') 

            else:        
                ax.barh(yp,-1*xL,left=-LR,height=BH,color='white',clip_on=False,lw=lw,ec='k') 
                ax.barh(yp,xR,left=LR,height=BH,color='dimgrey',alpha=0.85,clip_on=False,lw=lw,ec='k') 
            if self.PRINTPV: 
                try: 
                    ptail = '-'+str(int(str(pv).split('e-')[-1]))   
                    pstr = '$P{=}'+str(pv)[0:3]+' \\times 10^{'+ptail+'}$' 
                except: pstr = '$P{=}'+str(round(pv,5))+'$'
                ax.text(0, yp - BH*1.9, pstr, ha='center', va='top', fontsize=self.fs4) 
        else: 
            ax.barh(yp,-1*xL,left=-LR,height=BH,color='white',clip_on=False,lw=lw,ec='k') 
            ax.barh(yp,xR,left=LR,height=BH,color='white',clip_on=False,lw=lw,ec='k') 
        if self.CI:
            ax.plot([(-1*xLL)-LR,(-1*xLH)-LR],[yp,yp],color='k',lw=2*lw,zorder=100) 
            ax.plot([xRL+LR,xRH+LR],[yp,yp],color='k',lw=2*lw,zorder=100) 
        


        yp -= BH/1.5 
        self.add_arrows(ax,yp, INIT=False) 
        return yp        
                

    def add_group_label(self, ax, label, y1, y2): 
        ax.text(0,y1,label,ha='center',va='bottom',fontsize=self.fs3-0.5)  
        x1,x2 = -0.40, 0.40  
        ax.arrow(-0.01, y2,   x1, 0, linewidth=self.lw2, head_width=0.2, head_length=0.03, fc='k', ec='k',clip_on=False,zorder=0)     
        ax.arrow(0.01, y2,   x2, 0, linewidth=self.lw2, head_width=0.2, head_length=0.03, fc='k', ec='k',clip_on=False,zorder=0)     
        ax.text(x2+0.11,y2+0.09,'upper\ntail',ha='center',va='center',fontsize=self.fs5,clip_on=False) 
        ax.text(x1-0.11,y2+0.09,'lower\ntail',ha='center',va='center',fontsize=self.fs5,clip_on=False) 
        return


    def notate_line(self, ax, i, y1, y2, label = None, color='k', TOP=False, yj=0.2, xs=0.03): 
        lw = self.lw3
        if TOP: 
            ax.plot([0,0],[y1+yj,y2],color='k', clip_on=False, lw=lw) 
            ya, yb, fs = y1+yj*1.6, y2 - yj*1.8, self.fs1
        else: 
            ax.plot([0,0],[y1+yj,y2+yj/2.0],color='k', clip_on=False, lw=lw) 
            if y2-y1 < 1: ya, yb, fs = y1+yj*1.1, y2+yj*0.5, self.fs1-5 
            else:         ya, yb, fs = y1+yj, y2+yj*0.5, self.fs1-1
        ymid = ya + (yb - ya) / 2.0 
        if i == 1: 
            x1 = 0.40
            ax.plot([x1,x1],[ya,yb],color=color,clip_on=False,lw=lw) 
            ax.plot([x1-xs,x1],[ya,ya],color=color,clip_on=False,lw=lw) 
            ax.plot([x1-xs,x1],[yb,yb],color=color,clip_on=False,lw=lw) 
            ax.plot([x1,x1+xs*2],[ymid,ymid], color=color,clip_on=False,lw=lw) 
            if y2 - y1 < 1: ax.text(0.65,ymid-yj*2.5,label,ha='center',va='center',rotation=0,fontsize=self.fs5) 
            else:           ax.text(0.65,ymid-yj,label,ha='center',va='center',rotation=0,fontsize=self.fs5) 
        else: 
            x1 = -0.52
            ax.plot([x1,x1],[ya,yb],color=color,clip_on=False,lw=lw) 
            ax.plot([x1,x1+xs],[ya,ya],color=color,clip_on=False,lw=lw) 
            ax.plot([x1,x1+xs],[yb,yb],color=color,clip_on=False,lw=lw) 
            ax.plot([x1,x1-xs*2],[ymid,ymid], color=color,clip_on=False,lw=lw) 
            return







    def plot_scores(self, axes, LR=0.015, PRINTPV=False, INIT=False): 
        self.PRINTPV, yMin = PRINTPV, 10 
        if not self.PRINTPV: axes[0].text(-0.2,11.2,'$POPout$ Effects Stratified by Inferred Selection',fontsize=self.fs2+0.5,clip_on=False) 
        elif INIT:           axes[0].text(1.5,10.2,'$POPout$ Effects Stratified by Inferred Selection\n(Initial Models)',ha='center',fontsize=self.fs2-1,clip_on=False) 
        else:                axes[0].text(1.5,10.2,'$POPout$ Effects Stratified by Inferred Selection\n(Alternate Models)',ha='center',fontsize=self.fs2-1,clip_on=False) 
        labels = ['No Selection\n($\\beta$=0,$\gamma$=0)','Positive Directional\n($\\beta > 0$)','Negative Directional\n($\\beta < 0$)'] 
        for i,ax in enumerate(axes): 
            mL,mQ,mD,mS = [sorted(self.evo_groups[i][k], key = lambda X: X[0]) for k in ['linear','quadratic','diverging','stabilising']] 
            self.add_group_label(ax, labels[i], 9.35, 9.3) 
            yp, self.scorekeep = 9.0, dd(list) 
            for j,(eType, T) in enumerate(mL): yp = self.quick_add(ax, yp, T) 
            if i == 0: 
                ax.plot([0,0],[yp+0.15,9.3],color='k',lw=0.4,clip_on=False) 
                yp = self.add_group_means(ax, yp+0.1, labels[i]) 
                xloc, yp, yp2, clr, self.scorekeep = 0, yp-1.1, yp-1.6, 'k', dd(list) 
                ax.text(0,yp-0.5,'Non-directional Stabilising\n($\\beta=0, \gamma<0$)',ha='center',va='bottom',fontsize=self.fs4) 
                ax.plot([-0.4,0.4],[yp2,yp2], linestyle='-',color='k',zorder=10, lw=self.lw2,clip_on=False) 
                yp -=0.80
                mQ = sorted(self.evo_groups[i]['quadratic'], key = lambda X: X[0]) 
                for j,(eType, T) in enumerate(mQ): yp = self.quick_add(ax, yp, T)  
                ax.plot([0,0],[yp+0.1,yp2],color='k',lw=0.4,clip_on=False)  
                yp = self.add_group_means(ax, yp+0.1, 'Non-Direction Stabilizing') 
            else: 
                self.notate_line(ax, i, yp, 9.3, 'Directional\nOnly\n($\gamma$=0)','k', TOP=True) 
                if len(mD) > 0:
                    y0 = yp 
                    for eType, T in mD: yp = self.quick_add(ax, yp, T)  
                    self.notate_line(ax, i, yp, y0,'Directional\n&\nDisruptive\n($\gamma$>0)',color='dimgrey') 
                if len(mS) > 0: 
                    y0 = yp 
                    for eType, T in mS: yp = self.quick_add(ax, yp, T)  
                    self.notate_line(ax, i, yp, y0, 'Directional\n&\nStabilising\n($\gamma$<0)') 
                yp = self.add_group_means(ax, yp, labels[i]) 
            ax.axis('off') 
            

            if   i == 0: ax.set_xlim(-0.6,0.85) 
            elif i == 1: ax.set_xlim(-0.5,0.9) 
            else:      ax.set_xlim(-0.50,0.70) 
            if yp < yMin: yMin = yp 
        
        for j,ax in enumerate(axes): 
            if j == 0: ax.set_ylim(yMin-0.3,10.5) 
            else:      ax.set_ylim(yMin, 10.5) 
        
        ax = axes[0] 
        y1, y2 = yMin - 0.75, yMin+0.3 
        x1, x2 = -0.5, 0.5
        DV.draw_square(ax,x1,x2,y1,y2) 
        if self.PRINTPV: xclrs, xnames, yLocs = ['k','white'], ['Significant diff.','NS diff.'], [yMin-0.1,yMin-0.55] 
        else:            xclrs, xnames, yLocs = ['k','white'], ['Significant diff.','Non-significant diff.'], [yMin-0.1,yMin-0.55] 
        for i,(c,n,y) in enumerate(zip(xclrs,xnames,yLocs)): 
            ax.bar(x1+0.04,0.3,bottom =y , align='edge', width = 0.1, color= c, edgecolor= 'dimgrey', lw=0.2,clip_on=False) 
            ax.text(x1+0.16,y, n, ha='left', va='bottom', fontsize=self.fs5) 
        


    def plot_health_tails(self, ax, clr = 'xkcd:dusty green',clr2='xkcd:dark sage', baf=0.95): 
        TR, names  = [], ['Children\nFathered', 'Livebirths\n(Maternal)', 'Number of\nIllnesses', 'Miscarriages &\nStill Births', 'Paternal\nAge']
        for k in ['pkid','mkid','ill','msb','page']: 
            X, Y, Z = [], [], [] 
            for ti,T in self.traits.items():
                try:  
                    x1, x2 = T.vals['health'].key[k+'1'], T.vals['health'].key[k+'2'] 
                    e1, e2 = T.vals['pop']['common-snp'].e1  ,T.vals['pop']['common-snp'].e2  
                    X.extend([x1,x2]) 
                    Y.extend([e1,e2])
                    Z.append([e1,x1,ti]) 
                    Z.append([e2,x2,ti]) 
                except KeyError: continue 
            TR.append(spearman_ci(X,Y))
        TK = dd(lambda: dd(list)) 
        xOffset, yOffset = 0, 0.1 
        for i,(S,pv,sL,sH) in enumerate(TR): 
            n = names[i] 
            xp = i + 0.5 + i * 0.25 
            if S > 0: yp = yOffset 
            else:     yp = -yOffset 
            ax.text(xp, 0, names[i], fontsize=self.fs4, ha='center',va='center')  
            if not self.CI: 
                ax.bar(xp, S, bottom=yp, width=0.5, edgecolor='k', color=clr, clip_on=False)  
            else: 
                
                #print(n, pv,sL, sH) 

                ax.bar(xp, S, bottom=yp, width=0.5, edgecolor='k', color=clr, alpha=baf,clip_on=False)  
                if S > 0: ax.plot([xp,xp],[max(yOffset,sL+yOffset), yOffset+sH], lw=0.6,zorder=3,color=clr2,clip_on=False) 
                else:     ax.plot([xp,xp],[min(-yOffset,-yOffset+sH),-yOffset+sL], lw=0.6,zorder=3,color=clr2,clip_on=False) 
            if pv < 0.05: 
                st = '*' 
                if pv < 0.01: st+='*' 
                if pv < 0.001: st+='*' 
                if S > 0: ax.text(xp,yp+S+0.1, st,ha='center',va='top',fontweight='bold',zorder=111,fontsize=self.fs1) 
                else:     ax.text(xp,yp+S-0.03, st,ha='center',va='top',fontweight='bold',zorder=111,fontsize=self.fs1) 
            gzz = str(round(S,3))+','+str(round(pv,5)) 
            self.progress.report_result('Health-Measure/POPout Rank Correlation: ' +"_".join(names[i].split('\n'))+' S,p='+gzz) 
        xEnd =5.5
        xh, yh = -0.2, 0.6 
        xp,yp = 3.2, -0.51
        ax.text(xp-0.5,-0.5,'*$P<0.05$,  **$P<0.01$,  ***$P<0.001$',fontsize=self.fs4,color='k') 
        DV.draw_square(ax, xp-0.6,xp+2.6, yp-0.03,yp+0.13, lw=0.5) 
        s = 1
        ax.set_ylim(-0.37,0.35) 
        ax.set_xlim(1,xEnd+0.1) 
        xh, yh = -0.2, 0.6 

        for s in [-1,1]:  
            ax.plot([xh,xEnd+0.25],[s*yOffset,s*yOffset],color='k',zorder=10,linewidth=1,clip_on=False) 
            for i,xloc in enumerate([xh,xEnd]): 
                if s == -1 and i == 0:  
                    ax.arrow(xloc, 0, 0, 0.38,  linewidth=0.5,  head_width=0.1, head_length=0.05, fc='k', ec='k',clip_on=False,zorder=0)
                    ax.arrow(xloc, 0, 0,-0.40,  linewidth=0.5, head_width=0.1, head_length=0.05, fc='k', ec='k',clip_on=False,zorder=0)
        x1 = -0.22
        ax.text(x1,0.20+yOffset,'-0.25', va='center',fontsize=self.fs5) 
        ax.text(x1,-1*(0.20+yOffset),'--0.25', va='center',fontsize=self.fs5) 
        ax.text(xh-0.25,0,'Correlation\nwith $POPout$', ha = 'center',va='center',rotation = 90, fontsize=self.fs3) 
        ax.axis('off') 
        return self










