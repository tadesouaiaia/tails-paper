import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))                                                                                                                                                                                                                                            
if HERE not in sys.path: sys.path.insert(0, HERE)                                                                                                                                                                                                                                            
from util.Util   import *
from util import drawScatter as SP
from util import drawVarious as DV
from util import drawForest  as DF

# Extended Data Figure: Detailed Replication # 


class MyFigure:
    def __init__(self, options, traits, progress, figName=None): 
        self.options, self.data, self.traits, self.figName = options, traits, traits.members, figName
        self.exampleTraits = self.get_valid_examples() 
        self.progress = progress.update(self) 
        self.fs0, self.fs1, self.fs2, self.fs3, self.fs4, self.fs5 = 20, 15, 10, 7, 6, 5
        self.sz1, self.sz2, self.sz3 = 15,10,8
        self.lw1, self.lw2, self.lw3 = 1, 0.7, 0.5

    def get_valid_examples(self): 
        X, cands = [], [] 
        for c in [50,21002,30020,30070,30870]: 
            if c in self.traits and 'pop' in self.traits[c].pts and 'aou' in self.traits[c].pts['pop']: cands.append(c) 
        
        for i,ti in enumerate(self.options.indexTraits): 
            if ti in self.traits and 'pop' in self.traits[ti].pts and 'aou' in self.traits[ti].pts['pop']: X.append(ti) 
            else: 
                opts = [c for c in cands if c not in self.options.indexTraits + X] 
                if len(opts) > 0: X.append(opts[0])
                else:             X.append(ti) 
        return X 

    
    def draw(self): 
        self.setup() 
        self.create(self.exampleTraits) 
        self.finish() 

    def add_square(self,x,y, s=10): 
        self.axes.append(plt.subplot2grid((self.rows,self.cols), (x,y), rowspan = s-1, colspan =s)) 
        self.axes.append(plt.subplot2grid((self.rows,self.cols), (x,y+s), rowspan = s-1, colspan =s)) 
        self.axes.append(plt.subplot2grid((self.rows,self.cols), (x+s-1,y), rowspan = s-1, colspan =s)) 
        self.axes.append(plt.subplot2grid((self.rows,self.cols), (x+s-1,y+s), rowspan = s-1, colspan =s)) 
        return 


    def setup(self): 
        self.POP_SIM=False
        if 'popout_sim.txt' in os.listdir(self.options.simPath):
            with open(self.options.simPath+'/popout_sim.txt') as f: X = [line.split() for line in f.readlines()] 
            self.sim_key = {X[0][j]: [float(x[j]) for x in X[1::]] for j in range(0,len(X[0]))} 
            self.POP_SIM = True 
        self.rep_color, self.poc_color, self.aou_color  = 'xkcd:purpley', 'xkcd:barney','xkcd:leaf green' 
        self.my_colors = [self.rep_color,self.poc_color,self.aou_color]
        self.ax_index, self.base  = 0, 20 
        self.fig, self.axes = plt.gcf(), [] 
        self.rows, self.cols, self.WD, self.HT = 85, 80, 45, 50
        self.rows, self.cols, self.WD, self.HT = 85, 80, 7.2, 9.7 
        s = 10
        self.add_square(0,0,s) 
        self.add_square(0,2*s+1,s) 
        self.add_square(2*s,0,s) 
        self.add_square(2*s,2*s+1,s)
        self.axes.append(plt.subplot2grid((self.rows,self.cols), (0,4*s+8), rowspan = 80, colspan =s*3))  
        ci=1
        r1, rs = s*4+8 , 14 
        if self.POP_SIM: 
            self.axes.append(plt.subplot2grid((self.rows,self.cols), (r1+2,ci), rowspan = rs, colspan =s+9)) 
            self.axes.append(plt.subplot2grid((self.rows,self.cols), (r1+2,2+s+12), rowspan = rs, colspan =s+8)) 
            self.axes.append(plt.subplot2grid((self.rows,self.cols), (r1+rs+8,ci), rowspan = rs, colspan =s+9)) 
            self.axes.append(plt.subplot2grid((self.rows,self.cols), (r1+rs+8,2+s+12), rowspan = rs, colspan =s+8)) 
        else: 
            self.axes.append(plt.subplot2grid((self.rows,self.cols), (r1+3,ci), rowspan = rs, colspan =s+9)) 
            self.axes.append(plt.subplot2grid((self.rows,self.cols), (r1+3,2+s+12), rowspan = rs, colspan =s+8)) 
            self.axes.append(plt.subplot2grid((self.rows,self.cols), (r1+rs+8,ci), rowspan = rs, colspan =s+9)) 
            self.axes.append(plt.subplot2grid((self.rows,self.cols), (r1+rs+8,2+s+12), rowspan = rs, colspan =s+8)) 
        

        self.fig.set_size_inches(self.WD, self.HT) 
        return





    def finish(self,fs=20):
        letters = ['$a$','$b$','$c$','$d$','$e$','$f$','$g$','$h$'] 
        for i,ax in enumerate([self.axes[0], self.axes[16],self.axes[17],self.axes[18],self.axes[19],self.axes[20]]): #,self.axes[16]]): # self.axes[6], self.axes[10], self.axes[12],self.axes[13]]): 
            lms = DV.AxLims(ax) 
            xs, ys = lms.xHop*0.5, lms.yHop*0.5
            xp = lms.xMin - xs * 10 
            yp = lms.yMax 
            if i == 0: ax.text(xp-xs*8,yp, letters[i], fontsize=fs, clip_on=False) 
            elif i == 1: ax.text(xp-xs*3,yp, letters[i], fontsize=fs, clip_on=False) 
            elif i == 2: ax.text(xp-xs*3,yp, letters[i], fontsize=fs, clip_on=False) 
            elif i == 3: ax.text(xp,yp, letters[i], fontsize=fs, clip_on=False) 
            elif i == 4: ax.text(xp-xs*3,yp, letters[i], fontsize=fs, clip_on=False) 
            elif i == 5: ax.text(xp,yp, letters[i], fontsize=fs, clip_on=False) 
            else:        ax.text(xp,yp, letters[i], fontsize=fs, clip_on=False) 
            continue


        plt.subplots_adjust(left=0.03, bottom=0.033, right=0.975, top=0.975,wspace=0.01, hspace=0.03) 
        
        self.progress.save() 
        return

        if self.figName is not None: figPath = self.options.out+self.figName+'.pdf' 
        else:                        figPath = self.options.out+'Sup1.pdf' 
        plt.savefig(figPath, dpi=self.options.dpi) 
        plt.clf() 
        self.progress.save('(Figure Saved: '+figPath+')')
        return


    def create(self,choices):  
        self.choices = choices 
        tk = ['Dual Tail Regression', 'Lower Tail Regression', 'Upper Tail Regression', 'No Tail Regression'] 
        self.rep_color, self.poc_color, self.aou_color  = 'xkcd:purpley', 'xkcd:barney','xkcd:leaf green'
        my_reps, my_colors = ['common','rep','poc','aou'], ['blue',self.rep_color, self.poc_color, self.aou_color] 
        self.progress.set_panel('a') 
        for i,ti in enumerate(self.choices): 
            axes = self.axes[i*4:i*4+4]
            for j,(k,clr,ax) in enumerate(zip(my_reps, my_colors, axes)): 
                sp = SP.POPplot(ax, self, ti, sz1=15,sz2=10,sz3=8,lw1=1,lw2=0.5, INIT=(i+j==0)) 
                sp.draw_rep_popout(k, rc1=clr, yc1=clr, yc2=clr, TITLE=(j==0)) 
            self.ax_index += 4
        
        self.progress.set_panel('b') 
        self.ax_index = 16 
        self.corr_key, self.discovery_key = DF.ForestReps(self.axes[self.ax_index], self).create()         
        self.ax_index += 1 

        if self.POP_SIM: 
            self.draw_sims(self.axes[self.ax_index], self.axes[self.ax_index+2]) 
            if self.progress.SAVESRC: self.save_sim_src() 
            rep_result = self.draw_reps(self.axes[self.ax_index+1], self.axes[self.ax_index+3]) 
            if self.progress.SAVESRC: self.save_rep_src(rep_result) 
        else: 
            #if self.progress.SAVESRC: self.save_rep_src() 
            rep_result = self.draw_reps(self.axes[self.ax_index], self.axes[self.ax_index+1]) 
        self.draw_key(self.axes[self.ax_index]) 



    def draw_key(self, ax, sz=35, fs=7.33): 
        lms = DV.AxLims(ax) 
        y1, y2, ys, xs = lms.yMax + 5*lms.yStep, lms.yMax + 6*lms.yStep, lms.yStep, lms.xStep 
        x1,x2,x3,x4 = [lms.xMin + lms.xStep * i for i in [-0.05,5.65,12.25,17.8]]
        DV.draw_square(ax,x1-xs*0.5,x4+xs*3.3,y1-ys*1.2,y2+ys*0.7)
        c1,c2,c3,c4 = 'blue', self.rep_color, self.poc_color, self.aou_color
        
        ax.scatter(x1,y1,marker='o', color=c1,ec = 'k',s=sz,clip_on=False,zorder=10,lw=1,alpha=0.7)
        ax.text(x1+xs*0.3,y1,'UKB-European',fontsize=fs,va='center',ha='left')
        ax.scatter(x2,y1,marker='o', color=c2,ec = 'k',s=sz,clip_on=False,zorder=10,lw=1,alpha=0.7)
        ax.text(x2+xs*0.3,y1,'Repeat Measures\n(UKB-EUR)',fontsize=fs,va='center',ha='left')

        ax.scatter(x3,y1,marker='o', color=c3,ec = 'k',s=sz,clip_on=False,zorder=10,lw=1,alpha=0.7)
        ax.text(x3+xs*0.3,y1,'Multi-Ancestry\n(UKB)',fontsize=fs,va='center',ha='left')

        ax.scatter(x4,y1,marker='o', color=c4,ec = 'k',s=sz,clip_on=False,zorder=10,lw=1,alpha=0.7)
        ax.text(x4+xs*0.3,y1,'All Of Us',fontsize=fs,va='center',ha='left')
        ax.set_xlim(lms.xMin, lms.xMax) 
        ax.set_ylim(lms.yMin, lms.yMax) 
        return


    def save_sim_src(self): 
        X, Cy, Ce, Ry, Re  = [self.sim_key[k] for k in ['---', 'repRate', 'repErr', 'pearsonR', 'pearsonErr']]
        self.progress.set_panel('c') 
        w = self.progress.out3    
        w.write('%s,%s,%s,%s\n' % ('Panel', 'Target Bootstrap Size','Percent Replicated','95% Confidence Interval')) 
        for x,y,e in zip(X,Cy,Ce): w.write('%s,%s,%s,%s\n' % (self.progress.panel,int(x),y,str(round(y-e,3))+'-'+str(round(y+e,3)))) 
        self.progress.set_panel('e') 
        w = self.progress.out3    
        w.write('%s,%s,%s,%s\n' % ('Panel', 'Target Bootstrap Size','Pearson R','95% Confidence Interval')) 
        for x,y,e in zip(X,Ry,Re): w.write('%s,%s,%s,%s\n' % (self.progress.panel,int(x),y,str(round(y-e,3))+'-'+str(round(y+e,3)))) 
        return



    def draw_sims(self, ax1, ax2, fs = 7): 
        X, Cy, Ce, Ry, Re  = [self.sim_key[k] for k in ['---', 'repRate', 'repErr', 'pearsonR', 'pearsonErr']]
        for j,(ax,Y,E) in enumerate(zip([ax1,ax2],[Cy,Ry],[Ce,Re])):  
            ax.plot(X,Y,lw=2, color='k') 
            for i,x in enumerate(X): 
                ax.scatter(x, Y[i], marker='s', color='k',s=13) 
                ax.plot([x,x],[Y[i] - E[i], Y[i] + E[i]], color = 'k', lw=1) 
            ax.set_xlabel('Target Bootstrap Size (k)',fontsize=fs) 
            ax.set_xticks(X)  
            ax.set_xticklabels([str(int(x/1000)) for x in X]) 
            ax.set_yticks([0,0.2,0.4,0.6,0.8,1]) 
            ax.set_yticklabels(['0',0.2,0.4,0.6,0.8,'']) 
            if j == 0: 
                ax.set_title('$POPout$ Bootstrap Rediscovery',fontsize=fs) 
                ax.set_ylabel('Percent Replicated',fontsize=fs) 
            else:      
                ax.set_title('$POPout$ Bootstraped Replication',fontsize=fs) 
                ax.set_ylabel('Pearson Correlation',fontsize=fs)  
        return

    def save_rep_src(self, rep_result): 
        for i,panel in enumerate(['d','f']): 
            self.progress.set_panel(panel) 
            w = self.progress.out3    
            if i == 0: 
                w.write('%s,%s,%s\n' % ('Panel', 'ReplicationType','Percent Replicated')) 
                for k,v in rep_result[panel].items(): w.write('%s,%s,%s\n' % (panel, k, v)) 
            else: 
                w.write('%s,%s,%s,%s\n' % ('Panel', 'ReplicationType','Pearson Correlation','95% Confidence Interval')) 
                for k,v in rep_result[panel].items(): w.write('%s,%s,%s,%s\n' % (panel, k, v[0], v[1])) 
        return

    def draw_reps(self, ax1, ax2, fs = 8, fs2=7, CI=True): 
        
        rep_result = dd(lambda: {}) 
        for i,(k,c) in enumerate(zip(['rep','poc','aou'],self.my_colors)): 
            if i == 0: self.progress.set_panel('d') 
            else:      self.progress.set_panel('f') 
            
            yF, yT, yS = self.discovery_key[k] 
            yp, mSize = yF/yT, 'n~'+str(int(np.mean(yS) / 1000.0))+'k' 
            ax1.bar(i,yp, color=c, ec='k',lw=0.5,alpha=0.8,width=0.7) 
            ax1.text(i, yp, mSize, ha='center', va='bottom',fontsize=fs2, fontweight='bold') 
            X,Y = self.corr_key[k]
            
            R,pv,rL,rH = pearson_ci(X,Y) 
            
            rep_result['d'][k] = yp 
            rep_result['f'][k] = [round(R,3),str(round(rL,3))+'-'+str(round(rH,3))] 


    def draw_reps(self, ax1, ax2, fs = 8, fs2=7, CI=True): 
        
        rep_result = dd(lambda: {}) 
        for i,(k,c) in enumerate(zip(['rep','poc','aou'],self.my_colors)): 
            if i == 0: self.progress.set_panel('d') 
            else:      self.progress.set_panel('f') 
            
            yF, yT, yS = self.discovery_key[k] 
            yp, mSize = yF/yT, 'n~'+str(int(np.mean(yS) / 1000.0))+'k' 
            ax1.bar(i,yp, color=c, ec='k',lw=0.5,alpha=0.8,width=0.7) 
            ax1.text(i, yp, mSize, ha='center', va='bottom',fontsize=fs2, fontweight='bold') 
            X,Y = self.corr_key[k]
            
            R,pv,rL,rH = pearson_ci(X,Y) 
            
            rep_result['d'][k] = yp 
            rep_result['f'][k] = [round(R,3),str(round(rL,3))+'-'+str(round(rH,3))] 

            ax2.bar(i,R, color=c, ec='k',lw=0.5,alpha=0.8,width=0.7) 
            CI = True 
            if CI: ax2.plot([i,i],[rL,rH], color=c, zorder=99) 
            else: 
                try: 
                    p_start = str(int(str(pv).split('.')[0]))
                    p_end = str(int(str(pv).split('e-')[-1]))
                    rpv = 'P=\n'+'$'+p_start+'{\\times}$'+'$10^{-'+p_end+'}$'
                except ValueError: rpv = 'P=\n'+'$'+str(round(pv,5))+'$' 
                ax2.text(i+0.06, R*1.01, rpv, ha='center', va='bottom',fontsize=fs2) 

        for i,ax in enumerate([ax1, ax2]): 
            if i == 0: 
                ax.set_title('$POPout$ Discovery',fontsize=fs) 
                ax.set_ylabel('Percent Replicated', fontsize=fs) 
            else:      
                ax.set_title('$POPout$ Replication',fontsize=fs) 
                ax.set_ylabel('Pearson Correlation', fontsize=fs) 
            ax.set_xticks([0,1,2]) 
            ax.set_xticklabels(['Repeated','Multi\nAncestry','All Of\nUs'],fontsize=fs) 
            ax.set_yticks([0,0.2,0.4,0.6,0.8,1]) 
            ax.set_yticklabels(['0',0.2,0.4,0.6,0.8,'']) 
        return rep_result 

