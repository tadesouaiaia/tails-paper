import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))                                                                                                                                                                                                                                            
if HERE not in sys.path: sys.path.insert(0, HERE)                                                                                                                                                                                                                                            
from util.Util   import *
from util import drawScatter as SP
from util import drawVarious as DV
from util import drawLabels  as DL

# Extended Data Figure: Analysis of the Tail and Extreme Tail 0.1% # 




class MyFigure:
    def __init__(self, options, traits, progress, figName=None):
        self.options, self.data, self.traits, self.figName = options, traits, traits.members, figName
        self.progress = progress.update(self) 
        self.fs0, self.fs1, self.fs2, self.fs3, self.fs4, self.fs5 = 20, 15, 10, 7, 6, 5
        self.sz1, self.sz2, self.sz3 = 15,10,8
        self.lw1, self.lw2, self.lw3 = 1, 0.7, 0.5





    def draw(self): 
        self.test_tails() 
        self.setup() 
        self.create() 
        self.finish() 

    def setup(self): 
        self.ax_index, self.base = 0, 20   
        self.fig, self.axes = matplotlib.pyplot.gcf(), [] 
        self.rows, self.cols, self.WD, self.HT = 57, 27,  43, 45
        self.rows, self.cols, self.WD, self.HT = 57, 27,  7.2, 7.4
        rs1, cs1 = 8, 9 
        xn, rs1, cs1 = 0, 8,6 
        for rx in [xn,xn+9]: 
            for cx in [0, cs1*2+2]: 
                self.axes.append(plt.subplot2grid((self.rows,self.cols), (rx,cx), rowspan = rs1, colspan =cs1))
                self.axes.append(plt.subplot2grid((self.rows,self.cols), (rx,cx+cs1), rowspan = rs1, colspan =cs1))
        if self.TAIL_INDIVS: 
            xn,rs,cs = xn+16+rs1, 7,12 
            for rx in [xn,xn+rs+4]: 
                for cx in [1, cs+2]: 
                    self.axes.append(plt.subplot2grid((self.rows,self.cols), (rx,cx), rowspan = rs, colspan =cs))
            xn, rs, cs  = xn+rs*2+8, rs1*2-6, cs1*2-1
            self.axes.append(plt.subplot2grid((self.rows,self.cols), (xn,1), rowspan = rs, colspan =cs)) 
            self.axes.append(plt.subplot2grid((self.rows,self.cols), (xn,cs+4), rowspan = rs, colspan =cs)) 
        else:
            self.WD, self.HT = 60, 40 
            self.rows, xn, rs, cs = 30, 8 + rs1, rs1*2-6, cs1*2-1
            self.axes.append(plt.subplot2grid((self.rows,self.cols), (xn,1), rowspan = rs, colspan =cs)) 
            self.axes.append(plt.subplot2grid((self.rows,self.cols), (xn,cs+4), rowspan = rs, colspan =cs)) 
        self.fig.set_size_inches(self.WD, self.HT) 
        return         


    


    
    def create(self, fs=33): 
        
        self.c1, self.c1e, self.c2, self.c2e = 'blue', 'cyan', 'xkcd:shamrock green', 'lime' 
        self.rc, self.rce = 'gold', 'xkcd:bright yellow' 
        

        self.color_maps = [make_colormap(a, b) for a,b in [[self.c1,self.c1e],[self.c2,self.c2e],[self.rc,self.rce]]]

        #self.map1 = make_colormap(self.c1, self.c1e) 
        #self.map2 = make_colormap(self.c2, self.c2e) 
        #self.map3 = make_colormap(self.rc, self.rce) 
        index_plots, rare_plots = [], [] 
        
        self.progress.set_panel('a') 
        for i,(idx,ti) in enumerate(zip([1,3,5,7],self.options.indexTraits)):
            spp = SP.POPplot(self.axes[idx], self, ti, sz1=20,sz2=18,sz3=12,fs1=10,fs2=8,fs3=6) 
            spp.draw_extreme_recovery() 
            index_plots.append(spp) 
            if ti in self.traits: 
                self.axes[idx].set_title(self.traits[ti].name.mini, x=0,y=0.97,va='center', fontsize=self.fs3) 
        
        DL.TailLabels(self.options).make_extreme_index_key(index_plots[3], self) 
       

        for i,(idx,ti) in enumerate(zip([0,2,4,6],self.options.indexTraits)):
            rpp = SP.POPplot(self.axes[idx], self, ti, sz1=20,sz2=18,sz3=12,fs1=10,fs2=8,fs3=6) 
            rpp.draw_extreme_rares('A+B+burden', yc1=self.rc, yc2=self.rc, yc3=self.rce, ec1='k' ,ec2='k')
            rare_plots.append(rpp) 
        
        self.progress.set_panel('b') 
        if self.TAIL_INDIVS: self.draw_tail_indivs(self.axes[8:12])

        self.draw_extreme_dists(self.axes[-2], self.axes[-1]) 
        return 

    


    def test_tails(self, upper=[30070,20015],lower=[30020,20015]): 
        self.TAIL_INDIVS, self.tail_traits, self.TK = True, [], dd(lambda: {}) 
        try: 
            for ti in upper: self.tail_traits.append(['upper',ti,self.traits[ti],self.traits[ti].pts['binned']['upper|>95']]) 
            for ti in lower: self.tail_traits.append(['lower',ti,self.traits[ti],self.traits[ti].pts['binned']['lower|<5']]) 
            self.TK['lower']['bn'] = ['1.0%','0.9%', '0.8%', '0.7%', '0.6%', '0.5%', '0.4%', '0.3%', '0.2%', '0.1%']
            self.TK['upper']['bn'] = ['99.0%','99.1%', '99.2%', '99.3%', '99.4%', '99.5%', '99.6%', '99.7%', '99.8%', '99.9%'] 
            for n,k in zip(['spot','xlab','ylab'],['<5','Lower Tail: ','% Sample with Low PRS']): self.TK['lower'][n] = k 
            for n,k in zip(['spot','xlab','ylab'],['>95','Upper Tail: ','% Sample with High PRS']): self.TK['upper'][n] = k 
        except: 
            self.TAIL_INDIVS = False 
        


    def draw_tail_indivs(self, axes, upper=[30070, 20015], lower=[30020,20015]): 
        
        if self.progress.SAVESRC:
            wss,wpp = self.progress.out3, self.progress.panel 
            wss.write('%s,%s,%s,%s,%s,%s\n' % (wpp,'Trait-ID','Tail','PRS-Type','Data-Type','Values'))

        bw,bj = 0.20, 0.23 
        my_bin_locs = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] 
        colors = [self.c1, self.c2, self.rc] 
        kTypes = ['common','combo','A+B+burden'] 
        for i,(tail,ti,T,P) in enumerate(self.tail_traits): 
            if self.progress.SAVESRC: wss.write('%s,%s,%s,%s,%s,%s\n' % (wpp,T.id,tail,'all','Bins',';'.join(self.TK[tail]['bn'])))
            ax = axes[i] 
            x0 = -0.2
            for m,k in enumerate(kTypes): 
                for  j,(fr,ci) in enumerate(zip(P[k].fracs, P[k].binomialCI)): 
                    ax.bar(x0+j, fr, width=bw, color=self.color_maps[m][j], ec = colors[m],lw=1, clip_on=False) 
                    ax.plot([x0+j,x0+j],[fr-ci, fr+ci],zorder=10,color='k',lw=0.5,clip_on=False) 
                    if m > 0 and fr - ci > P[kTypes[m-1]].fracs[j]: ax.scatter(x0+j, fr+ci+0.01, marker='*', ec = colors[m], lw=1, color='k', s= 10, clip_on=False, zorder=100) 
                x0 += 0.23 
                if self.progress.SAVESRC: 
                    fStr = ';'.join([str(round(fx,3)) for fx in P[k].fracs])    
                    cStr = ';'.join([str(round(fx - ci,3))+'-'+str(round(fx+ci,3)) for fx,ci in zip(P[k].fracs, P[k].binomialCI)])
                
                    if tail == 'upper':  
                        wss.write('%s,%s,%s,%s,%s,%s\n' % (wpp,T.id,tail,k,'%SampleWithHighPRS',fStr)) 
                        wss.write('%s,%s,%s,%s,%s,%s\n' % (wpp,T.id,tail,k,'%SampleWithHighPRS-ConfidenceIntervals',cStr)) 
                    else: 
                        wss.write('%s,%s,%s,%s,%s,%s\n' % (wpp,T.id,tail,k,'%SampleWithLowPRS',fStr)) 
                        wss.write('%s,%s,%s,%s,%s,%s\n' % (wpp,T.id,tail,k,'%SampleWithLowPRS-ConfidenceIntervals',cStr)) 
            xMin, xMax = -0.8 , 9.5 
            yMin, yMax =   0,0.35 
            ax.set_ylim(yMin,yMax-0.05)  
            ax.set_xticks(my_bin_locs, labels=self.TK[tail]['bn'], rotation = 20) 
            ax.set_xlabel(self.TK[tail]['xlab'] + " ".join(T.name.mini.split('_')), fontsize=self.fs3) 
            ax.spines[['left','right','top','bottom']].set_visible(False)
            if i in [0,2]: 
                ax.set_xlim(xMin,xMax-0.5)  
                ax.set_ylabel(self.TK[tail]['ylab'], fontsize=self.fs4) 
                ax.set_yticks([0,0.1,0.2,0.30],labels=['0','10%','20%','30%'],clip_on=False) 
                ax.plot([xMin,xMin],[yMin,yMax],color='k',lw=1,clip_on=False) 
                ax.plot([xMin,xMax+0.15],[0,0],color='k',lw=1,clip_on=False) 
                ax.plot([xMax+0.26,xMax+5],[0,0],color='k',lw=1,clip_on=False) 
                ax.plot([xMax+0.11,xMax+0.19],[0.01,-0.01],color='k',lw=1,clip_on=False) 
                ax.plot([xMax+0.20,xMax+0.28],[0.01,-0.01],color='k',lw=1,clip_on=False) 
            else: 
                ax.set_yticks([]) 
                ax.set_xlim(xMin+0.1,xMax)  
                ax.plot([xMin,xMax-0.2],[yMin, yMin], color='k', lw=1, clip_on=False) 
        
        
        DL.TailLabels(self.options).add_indiv_key(axes[0], self, RULE='UPPER') 
        DL.TailLabels(self.options).add_indiv_key(axes[2], self, RULE='LOWER') 
        return






    def draw_extreme_dists(self, ax1, ax2):  
        box_data = dd(list) 
        for ti,T in self.traits.items(): 
            try:  
                pC = T.vals['pop']['common-snp'] 
                pE = T.vals['pop']['common@0.1'] 
            except: continue 
            if pC.f1 and pC.e1 > 0: 
                box_data['e1'].append(pC.e1)  
                box_data['e2'].append(pE.e1)  
                if 'recovery' in T.vals: 
                    if T.vals['recovery']['combo'].total1 != 'NA': 
                        tC = max(0,T.vals['recovery']['combo'].total1)  
                        tE = max(0,T.vals['recovery']['combo@0.1'].total1)  
                        box_data['r1'].append(tC) 
                        box_data['r2'].append(tE) 
            if pC.f2 and pC.e2 > 0: 
                box_data['e1'].append(pC.e2)  
                box_data['e2'].append(pE.e2)  
                if 'recovery' in T.vals: 
                    if T.vals['recovery']['combo'].total2 != 'NA': 
                        tC = max(0,T.vals['recovery']['combo'].total2)  
                        tE = max(0,T.vals['recovery']['combo@0.1'].total2)  
                        box_data['r1'].append(tC) 
                        box_data['r2'].append(tE) 
        z1 = stats.ttest_ind(box_data['e1'], box_data['e2'])[1] 
        z2 = stats.ttest_ind(box_data['r1'], box_data['r2'])[1] 
        L1, L2= str(len(box_data['e1'])), str(len(box_data['r2']))
        m1, m2 = str(round(np.mean(box_data['e1']),3)), str(round(np.mean(box_data['e2']),3)) 
        q1, q2 = str(round(np.mean(box_data['r1']),3)), str(round(np.mean(box_data['r2']),3)) 
        zP, zS = [] , [] 
        for z in [z1,z2]: 
            if z < 0.001: 
                zA, zB = str(z)[0:3], str(z).split('e-')[-1] 
                zS.append('$P{=}'+zA+' \\times 10^{-'+zB+'}$') 
            else: 
                zS.append('$P{=}'+str(round(z,4))+'$') 
        self.progress.report_result('For '+L1+' FDR-Sig Positive POPout From 1% Tails, Avg Effect 1% vs 0.1%: '+m1+', '+m2+' (P='+str(z1)+')') 
        self.progress.report_result('For '+L2+' Above Tails w Rare Variants, Avg Recovery 1% vs 0.1%: '+q1+', '+q2+' (P='+str(z2)+')')  
        xMin, xMax = 0, 0.35
        xx1, xx2 = 0.08,0.26
        wx = 0.05 
        bp1 = ax1.boxplot([box_data['e1'], box_data['e2']], vert=True, patch_artist=True, positions = [xx1,xx2],widths=wx) #patch_artist=True, notch='False') #orientation='horizontal')
        bp2 = ax2.boxplot([box_data['r1'], box_data['r2']], vert=True, patch_artist=True, positions = [xx1,xx2],widths=wx) 
        if self.progress.SAVESRC:
            self.progress.set_panel('c') 
            wss,wpp = self.progress.out3, self.progress.panel 
            wss.write('%s,%s,%s\n' % (wpp,'Tail Size','SignificantPOPoutEffects'))
            wss.write('%s,%s,%s\n' % (wpp,'1%',";".join([str(zz) for zz in box_data['e1']])))
            wss.write('%s,%s,%s\n' % (wpp,'0.1%',";".join([str(zz) for zz in box_data['e2']])))
            self.progress.set_panel('d') 
            wss,wpp = self.progress.out3, self.progress.panel 
            wss.write('%s,%s,%s\n' % (wpp,'Tail Size','POPoutReductions'))
            wss.write('%s,%s,%s\n' % (wpp,'1%',";".join([str(zz) for zz in box_data['r1']])))
            wss.write('%s,%s,%s\n' % (wpp,'0.1%',";".join([str(zz) for zz in box_data['r2']])))

        ax1.set_ylabel('POPout Effect Size', fontsize=self.fs4) 
        colors = ['blue','blue','cyan','cyan']  
        for j,(ax,bp) in enumerate(zip([ax1,ax2],[bp1,bp2])):
            if j == 0: 
                yMin, yMax, my_colors = -0.31, 1.26, ['blue','cyan'] 
                ax.set_yticks([-0.2,0,0.25,0.5,0.75,1,1.25]) 
                ax.text(xMax,yMin,zS[0], ha='right',va='bottom',fontsize=self.fs3) 
            else:      
                yMin, yMax, my_colors = -0.13, 1.15, ['xkcd:shamrock green','lime'] 
                ax.set_yticks([0,0.25,0.5,0.75,1],[0,'25%','50%','75%','100%']) 
                ax.set_ylabel('POPout Reduction', fontsize=self.fs4) 
                ax.text(xMax,yMin,zS[1], ha='right',va='bottom',fontsize=self.fs4)        
            full_colors = [my_colors[0], my_colors[0], my_colors[1], my_colors[1]] 
            for patch, median, color in zip(bp['boxes'], bp['medians'], my_colors): 
                patch.set_facecolor(color)
                median.set(color='k',linewidth=1)
            for i in [0,1,2,3]: 
                bp['whiskers'][i].set(color=full_colors[i],linewidth=1)
                bp['caps'][i].set(color=full_colors[i],linewidth=1)
            for i,flyer in enumerate(bp['fliers']): 
                if i == 0: flyer.set(marker='D', markerfacecolor=my_colors[0], markeredgecolor='k',fillstyle='full', markersize=3)  
                else: flyer.set(marker='D', markerfacecolor=my_colors[1], markeredgecolor='k',fillstyle='full', markersize=3)  
            
            

            ax.set_xlim(xMin,xMax+0.01)  
            ax.set_ylim(yMin,yMax) 
            ax.spines[['right','top','bottom']].set_visible(False)
            ax.plot([xMin,xMax],[yMin,yMin], color='k', lw =1 ) 
            ax.set_xticks([xx1,xx2],labels=['1%','0.1%']) 
            ax.set_xlabel('Tail Size',fontsize=self.fs3, labelpad=-3, x=0.45) 
        return









    def finish(self, fs =13):
        #letters = ['$a$','$b$','$c$','$d$','$e$','$f$'] 
        for i,x in zip([0,8,12,13],['$a$','$b$','$c$','$d$','$e$','$g$','$h$']): 
            try: 
                if i == 0:   self.axes[i].set_title(x, x= -0.06, y = 0.98, fontsize=fs) 
                elif i == 8:   self.axes[i].set_title(x, x= -0.11, y = 1.07, fontsize=fs) 
                elif i == 12:   self.axes[i].set_title(x, x= -0.12, y = 1.05, fontsize=fs) 
                elif i == 13:   self.axes[i].set_title(x, x= -0.04, y = 1.03, fontsize=fs) 
            except: pass 
        plt.subplots_adjust(left=0.03, bottom=0.01, right=1.03, top=0.975,wspace=0.05, hspace=0.05) 
        
        self.progress.save() 
        return









