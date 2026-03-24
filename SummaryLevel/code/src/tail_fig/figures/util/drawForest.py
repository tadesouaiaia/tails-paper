import sys, os 
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path: sys.path.insert(0, HERE)
from Util import * 
import drawVarious as DV 



        




class ForestPlot:
    def __init__(self, axes, fig):
        self.axes, self.traits, self.data, self.options = axes, fig.traits, fig.data, fig.options 



    def draw_up_to_three(self): 
        self.prs_types, self.pad = dd(list), 0.5 
        for ti,T in self.traits.items(): self.prs_types[T.group].append([T.vals['pop']['common-snp'], T]) 
        g_srt = sorted([[len(self.prs_types[k]),k] for k in self.prs_types], reverse=True)
        self.set_forests(self.axes[0], [g_srt[0][1]])  
        next_two = [x[1] for x in g_srt[1::]][0:2]  
        self.set_forests(self.axes[-1],next_two) 
        return self


    def set_forests(self, ax, grps, fs1=7,fs2=5): 
        self.ax, self.yj, self.yp = ax, 2, 0 
        for i,g in enumerate(grps):  self.draw_forest_dots(g, len(grps), i, sorted(self.prs_types[g], key = lambda X: X[-1].name.mini)) 
        self.ax.axis('off') 
        if len(grps) == 1: 
            y1, y2 = self.yp, self.yp - 1.8*self.yj  
            x1, x2 = -0.2, 0.2 
            self.ax.text(x1,y2, 'Lower Tail $POPout$',ha='right',fontsize=fs2) 
            self.ax.text(x2,y2, 'Upper Tail $POPout$',ha='left',fontsize=fs2) 
            x1, x2, x3 = -0.89, -0.275, 0.43
            self.yp -= 1 
            y1,y2,ys = self.yp,-4.0, self.yp/-10.0
            yt = y1 - ys * 0.9 
            ax.scatter(x1+0.03,yt,marker='o',color='k',s=12,clip_on=False) 
            ax.plot([x1-0.05,x1+0.11],[yt,yt],color='k',lw=1,clip_on=False) 
            ax.text(x1+0.14,yt,'$POPout$ Effect (95% CI)',va='center',fontsize=fs2,clip_on=False) 
            ax.scatter(x3+0.02,yt,marker='o',color='white',ec='k',lw=0.9,s=12,clip_on=False) 
            ax.text(x3+0.085,yt,'FDR > 5%',fontsize=fs2,va='center',clip_on=False) 
            x1, x2 = -1.20, 1.22 
            self.ax.set_ylim(y1-ys*0.1,y2+1) 
            self.ax.set_xlim(x1,x2)
            DV.draw_square(ax,-1,1,y1-1.1*ys,y1-(ys/1.5)) 
        else:        
            x1, x2 = -0.95, 1.40 
            y1, y2 = self.yp+1.0, -8.5 
            self.ax.set_ylim(y1,y2+1) 
            self.ax.set_xlim(x1,x2)
            return



    def draw_forest_dots(self, name, group_members, group_idx, grp, lc1='whitesmoke',fs1=7,fs2=6,fs3=5,lw1=1,lw2=0.25): 
       

        if group_members == 1 and len(grp) > 40:                       grp, name = grp[0:40], 'Selected '+name 
        elif group_members > 1 and group_idx == 0 and len(grp) > 30:   grp, name = grp[0:30], 'Selected '+name
        elif group_members > 1 and group_idx == 1 and len(grp) > 15:   grp, name = grp[0:15], 'Selected '+name
        
        
        yTop = self.yp - self.yj*2 - self.yj*group_idx*0.65 
         


        self.ax.text(0,yTop+0.2,name,ha='center',va='bottom',fontweight='bold',fontsize=fs1,zorder=2)  
        self.yp = yTop -0.8
        if len(grp) == 1: self.yp -= 10 
        for i,(p,T) in enumerate(grp):
            e1 = [p.e1, p.e1 - p.j1, p.e1 + p.j1] 
            e2 = [p.e2, p.e2 - p.j2, p.e2 + p.j2] 
            self.make_whisky(e1, p.f1, p.QC == 'PASS', T, -1)   
            self.make_whisky(e2, p.f2, p.QC == 'PASS', T, 1)
            if len(T.name.mini) > 18:  self.ax.text(0,self.yp,T.name.mini[0:17]+'.',ha='center',va='center',fontsize=5) 
            else:                      self.ax.text(0,self.yp,T.name.mini,ha='center',va='center',fontsize=5) 
            RT = matplotlib.patches.Rectangle((-1.0, self.yp-0.65),2.0, 1.4, color=lc1, ec = lc1, lw = 0, alpha=0.9, zorder=0,clip_on=False)                                                                
            self.ax.add_patch(RT)     
            self.yp -= self.yj*0.9 
        
        self.yp += self.yj * 0.35 
        self.ax.plot([0-(self.pad+0.5),self.pad+0.5],[yTop, yTop], linestyle = '-', linewidth=lw2,color='k',clip_on=False) 
        
        self.ax.arrow(0, self.yp,  -1.02, 0, linewidth=1, head_width=0.8, head_length=0.05, fc='k', ec='k',clip_on=False,zorder=0)
        self.ax.arrow(0, self.yp,   1.02, 0, linewidth=1, head_width=0.8, head_length=0.05, fc='k', ec='k',clip_on=False,zorder=0)
        self.ax.plot([0,0],[self.yp,self.yp-0.9], clip_on=False, linewidth=1,color='k') 
        for a in [0.5,0.25,0,-0.25]:
            
            for m in [-1,1]: 
                self.ax.text(m*(self.pad+a), self.yp-0.8, a, va='top',ha = 'center', fontsize=fs3)
                self.ax.plot([m*(self.pad+a),m*(self.pad+a)],[self.yp-0.3,self.yp+0.3], linestyle = '--', color = 'k', zorder=10, linewidth=lw1, clip_on=False) 
                if a == 0.5: self.ax.plot([m*(self.pad+a),m*(self.pad+a)],[self.yp,yTop], linestyle = '-', color = 'k', zorder=0, linewidth=lw2, clip_on=False) 
                elif a == 0: self.ax.plot([m*(self.pad+a),m*(self.pad+a)],[self.yp,yTop], linestyle = '-', color = 'k', zorder=1, linewidth=lw2, alpha=1, clip_on=False) 
                else:        self.ax.plot([m*(self.pad+a),m*(self.pad+a)],[self.yp,yTop], linestyle = '-', color = 'k', zorder=0, linewidth=0.1, alpha=0.1, clip_on=False) 
        return





    def make_whisky(self, pts, FDR, QC, T, mp, TYPE = 'UKB', sz=9, LW=0.8):  
        
        if T.ti == 845:  pts = [p for p in pts]
        else:            pts = [-0.25 if p < -0.25 else p for p in pts]
        locs = [(self.pad + p)*mp for p in pts]
        if FDR and QC: 
            self.ax.plot([locs[1],locs[2]],[self.yp,self.yp], color = T.group_color, clip_on=False, zorder=2, lw = LW) 
            self.ax.scatter(locs[0], self.yp, color = T.group_color, ec = T.group_color, clip_on=False, zorder=3, s=sz) 
        else: self.ax.scatter(locs[0], self.yp, color = 'white', ec = T.group_color, lw=LW,clip_on=False, zorder=3, s=sz) 
        return


    




























class ForestReps:
    def __init__(self, ax, fig): 
        self.ax, self.fig, self.traits, self.data, self.options, self.progress = ax, fig, fig.traits, fig.data, fig.options, fig.progress 
        
                



    def rep_whisky(self, pts, T, mp, marker = 'o', color='k', TYPE='UKB', QC=True, SIZE=9999, MIN = -0.24, MAX=0.58): 
        if TYPE == 'UKB': 
            pts = [-0.15 if p < -0.15 else p for p in pts]                                                                                                                                                                      
            locs = [(self.pad + p)*mp for p in pts]                                                                                                                                                                             
            self.ax.plot([locs[1],locs[2]],[self.yp,self.yp], color = color, clip_on=False, zorder=5, lw = 1)                                                                                                           
            self.ax.scatter(locs[0], self.yp, color = color, ec = color, lw=0.7, clip_on=False, zorder=6, s=10) 
        else:
            MIN = -0.23 
            M1, M2, locs = False, False, [] 
            for p in pts: 
                if p >= MIN and p <= MAX: locs.append((self.pad+p)*mp) 
                elif p < MIN: 
                    M1 = True
                    locs.append((self.pad+MIN)*mp) 
                else: 
                    M2 = True 
                    locs.append((self.pad+MAX)*mp) 
            CLASH = False
            if locs[0] == locs[1]: CLASH=True 
            self.ax.plot([locs[1],locs[2]],[self.yp,self.yp], color = color, clip_on=False, zorder=2, lw = 1)       
            if QC and SIZE > 5000:  mark, c1, c2, c3 = 'o', color, color, color
            else:   mark, c1, c2, c3 = 's', 'white', color, color
            


            if not CLASH: self.ax.scatter(locs[0], self.yp, marker = mark, color = c1, ec = c2, lw =0.7, clip_on=False, zorder=3, s=10) 
            else:         c3 = 'white' 
            if mp == 1: 
                if M1: self.ax.scatter(locs[1], self.yp, marker= '<', color=c3, ec=color, zorder=4, lw=0.7, s = 10, clip_on=False) 
                if M2: self.ax.scatter(locs[2], self.yp, marker= '>', color=color, ec = color, zorder=4, lw=0.7,s = 10, clip_on=False) 
            else: 
                if M1: self.ax.scatter(locs[1], self.yp, marker= '>', color=c3, ec=color, zorder=4, lw=0.7, s = 10, clip_on=False) 
                if M2: self.ax.scatter(locs[2], self.yp, marker= '<', color=color, ec = color, zorder=4, lw=0.7, s = 10, clip_on=False) 
                
            return



    def prepare_forest(self): 
        compList = [] 
        self.comp_key = {}  
        self.discovery_key = dd(lambda: [0,0,[]]) 
        self.all_size_key = dd(list) 
        self.corr_key = dd(lambda: [[],[]]) 
        for ti,T in self.traits.items(): 
            P, pd = T.vals['pop'], T.vals['pop']['common-snp'] 
            p1, p2, QC = pd.p1, pd.p2, pd.QC 
            x1 = [pd.e1, pd.e1 - pd.j1, pd.e1 + pd.j1] 
            x2 = [pd.e2, pd.e2 - pd.j2, pd.e2 + pd.j2] 
            finds = [False, False] 
            if pd.e1 > 0 and pd.f1: finds[0] = True  
            if pd.e2 > 0 and pd.f2: finds[0] = True  
            rep_data = [] 
            for k in ['rep','poc','aou']: 
                if k in P: 
                    e1 = [P[k].e1, P[k].e1 - P[k].j1, P[k].e1 + P[k].j1] 
                    e2 = [P[k].e2, P[k].e2 - P[k].j2, P[k].e2 + P[k].j2]
                    
                    e1, e2 = [round(e,3) for e in e1], [round(e,3) for e in e2] 
                    size = P[k].size 
                    self.all_size_key[k].append(size) 
                    rep_data.append([e1,e2,k, (P[k].QC=='PASS'), P[k].size]) 
                    QC = (P[k].QC == 'PASS')
                    tests = [[P[k].p1, P[k].e1, pd.e1],[P[k].p2, P[k].e2, pd.e2]]
                    for i,(FIND,(pv,eV,uV)) in enumerate(zip(finds,tests)):
                        if FIND: 
                            self.discovery_key[k][1] += 1 
                            self.discovery_key[k][2].append(P[k].size) 
                            if (pv < 0.05 and eV > 0): self.discovery_key[k][0] += 1 
                        if QC and size > 5000:  
                            self.corr_key[k][0].append(eV) 
                            self.corr_key[k][1].append(uV) 
            if len(rep_data) == 3:
                rep_data = [[x1,x2,'UKB',True,'NA']]+rep_data 
                compList.append([T.name.mini, T] + [rep_data]) 
        return compList 


    def create(self, fs1 = 10, fs2 = 9, fs3=8, fs4=7, fs5=6, apad=0.05): 
        
        self.mvals, self.pad = [0,0.5], 0.5 
        lc1 = 'whitesmoke' 
        self.yp, yTop = 0.25, 1  
        mList = sorted(self.prepare_forest()) 
        for tname,T,comps in mList: 
            if len(tname.split()) == 1: 
                if len(tname) > 10:   self.ax.text(0,self.yp, tname,ha='center',va='center',fontweight='bold',fontsize=fs4-0.25) 
                elif len(tname) > 8: self.ax.text(0,self.yp, tname,ha='center',va='center',fontweight='bold',fontsize=fs4+0.25)                                                                                                                     
                else:                  self.ax.text(0,self.yp, tname,ha='center',va='center',fontweight='bold',fontsize=fs4+0.75)                                                                                                                     
            else: 
                tsp = tname.split() 
                zname = " ".join(tsp[0:-1])+'\n'+tsp[-1]  
                self.ax.text(0,self.yp, zname,ha='center',va='center',fontweight='bold',fontsize=fs4)                                                                                                                     
            RT = matplotlib.patches.Rectangle((-1.05, self.yp-0.6),2.1, 1.2, color=lc1, ec = lc1, lw = 0, alpha=0.5, zorder=0,clip_on=False)                                                                                                   
            self.ax.add_patch(RT)  
            self.yp += 0.35 
            for j,(pd,c) in enumerate(zip(comps,['blue']+self.fig.my_colors)): 
                e1,e2,k,QC,size = pd 
                self.rep_whisky(e1, T, -1, 'o', c, TYPE=k, QC=QC, SIZE=size)
                self.rep_whisky(e2, T,  1, 'o', c, TYPE=k, QC=QC, SIZE=size)  
                self.yp -= 0.25 
            self.yp -= 0.9
        self.yp += 1 * 0.79                                                                                                                                                                                           
        self.ax.plot([0-(self.pad+0.5),self.pad+0.5],[yTop, yTop], linestyle = '-', linewidth=1,color='k',clip_on=False)                                                                                                                  
        self.ax.arrow(0, self.yp,  -1*(self.mvals[-1]+self.pad + apad), 0, linewidth=1, head_width=0.5, head_length=0.05, fc='k', ec='k',clip_on=False,zorder=0)                                                             
        self.ax.arrow(0, self.yp,  (self.mvals[-1]+self.pad + apad), 0, linewidth=1, head_width=0.5, head_length=0.05, fc='k', ec='k',clip_on=False,zorder=0)                                                                
        for a in [0.5,0.25,0,-0.25]:                                                                                                                                                                                        
            for m in [-1,1]:                                                                                                                                                                                                
                self.ax.text(m*(self.pad+a), self.yp-0.4, a, va='top',ha = 'center', fontsize=5.5)                                                                                                                           
                self.ax.plot([m*(self.pad+a),m*(self.pad+a)],[self.yp-0.15,self.yp+0.1], linestyle = '--', color = 'k', zorder=10, linewidth=1, clip_on=False)                                                               
                if a == 0.5: self.ax.plot([m*(self.pad+a),m*(self.pad+a)],[self.yp,yTop], linestyle = '-', color = 'k', zorder=0, linewidth=0.5, clip_on=False)                                                                        
                elif a == 0: self.ax.plot([m*(self.pad+a),m*(self.pad+a)],[self.yp,yTop], linestyle = '--', color = 'k', zorder=0, linewidth=0.5, alpha=0.74, clip_on=False)                                                                        
                else:        self.ax.plot([m*(self.pad+a),m*(self.pad+a)],[self.yp,yTop], linestyle = '-', color = 'gray', zorder=0, linewidth=0.01, alpha=0.1, clip_on=False)  
        
        self.ax.axis('off')
        self.ax.set_xlim(-0.9,1.0) 
        x1, x2 = -0.5, 0.5 
        y1, y2, y3 = -48.5,-49.5, -51.75
        y0, y1, y2, y3 = self.yp + 0.5, self.yp-0.5, self.yp - 2.5, self.yp -3 
        self.ax.set_ylim(y0,1) 
        self.ax.plot([0,0],[y1+0.5,y1-0.25], color='k', linewidth=1, clip_on=False) 
        self.ax.text(x1+0.25,y1-1,'Lower Tail $POPout$',fontsize=fs2,va='center',ha='right')                                    
        self.ax.text(x2-0.25,y1-1,'Upper Tail $POPout$',fontsize=fs2,va='center',ha='left')                                    
        sz = 20 
        x1,x2, x3 = -0.85, -0.2, 0.3
        self.ax.scatter(x1,y3,marker='o', color='k',ec = 'k',s=sz,clip_on=False,zorder=10,lw=1,alpha=1)    
        self.ax.text(x1+0.05,y3,'Effect Size',fontsize=fs3,va='center',ha='left')                                    
        self.ax.scatter(x2,y3,marker='s', color='white',ec = 'k',s=sz,clip_on=False,zorder=10,lw=1,alpha=1)    
        self.ax.text(x2+0.05,y3,'QC Fail',fontsize=fs3,va='center',ha='left')                                    
        self.ax.scatter(x3-0.05,y3,marker='>', color='k',ec = 'k',s=sz,clip_on=False,zorder=10,lw=1,alpha=0.7)    
        self.ax.text(x3,y3,'Exceeds Range',fontsize=fs3,va='center',ha='left')                                    
        DV.draw_square(self.ax,x1-0.08,x3+0.65,y3-0.6,y3+0.7) 
        return self.corr_key, self.discovery_key  






































