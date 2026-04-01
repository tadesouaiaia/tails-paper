import sys, os                                                                                                                                                                                                                                                                               
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path: sys.path.insert(0, HERE)

from util.Util   import *
from util import drawScatter as SP
from util import drawVarious as DV
from util import drawLabels  as DL

# yo

class MyFigure:
    def __init__(self, options, traits, progress,figName=None): 
        self.options, self.data, self.traits, self.figName = options, traits, traits.members,figName
        self.progress = progress.update(self) 
        self.fs0, self.fs1, self.fs2, self.fs3, self.fs4 = 20, 15, 10, 7, 5
        self.sz1, self.sz2, self.sz3 = 15,10,8 
        self.lw1, self.lw2, self.lw3 = 1, 0.5, 0.2
        self.blockclr = 'whitesmoke' 


    def setup(self, STYLE='HOR'): 
        self.ax_index, self.base = 0, 20   
        self.fig, self.axes = matplotlib.pyplot.gcf(), [] 
        self.rows, self.cols, self.WD, self.HT = 45, 75, 7.1, 6.6
        rs1, rs2, cs1, cs2 = 6, 4, 14, 9 
        xn1, xn2 = rs1*2+4, 26 
        for i in [0,rs1]: 
            for j in [4,cs1+4]: 
                self.axes.append(plt.subplot2grid((self.rows,self.cols), (i,j), rowspan = rs1, colspan =cs1))
        self.axes.append(plt.subplot2grid((self.rows,self.cols), (0,cs1*2+12), rowspan = rs1*2-1, colspan =cs1*2+4))
        for rx in [xn1, xn1 + rs2+1]: 
            for cx in [0, cs2*4+2]: 
                for jp in range(4): 
                    if jp < 3: self.axes.append(plt.subplot2grid((self.rows,self.cols), (rx,cx+jp*cs2), rowspan = rs2, colspan =cs2))
                    else:      self.axes.append(plt.subplot2grid((self.rows,self.cols), (rx,cx+jp*cs2), rowspan = rs2, colspan =cs2+1))
        rs, cs = self.rows - xn1 - 1, int((self.cols/2))
        self.axes.append(plt.subplot2grid((self.rows,self.cols), (xn2,0), rowspan = rs, colspan =cs))
        self.axes.append(plt.subplot2grid((self.rows,self.cols), (xn2,cs+1), rowspan = rs, colspan =cs))
        self.fig.set_size_inches(self.WD, self.HT) 
        return         
                                



    def finish(self, fs =16):
        letters = ['$a$','$b$','$c$','$d$','$e$','$f$'] 
        for i,x in zip([0,4,5,21],['$a$','$b$','$c$','$d$','$e$','$g$','$h$']): 
            if i == 0:   self.axes[i].set_title(x, x= -0.25, y = 0.75, fontsize=fs) 
            elif i == 4:   self.axes[i].set_title(x, x= -0.1, y = 0.85, fontsize=fs) 
            elif i == 5:   self.axes[i].set_title(x, x= 0.05, y = 1.05, fontsize=fs+5) 
            elif i == 21:   self.axes[i].set_title(x, x= 0.01, y = 0.93, fontsize=fs) 
        plt.subplots_adjust(left=0.01, bottom=0.0075, right=0.99, top=0.99,wspace=0.05, hspace=0.1) 
        self.progress.save() 
        return



    def draw(self): 
        self.setup() 
        self.create() 
        self.finish() 

    
    def create(self, fs=33):
        self.c1, self.c2 = 'blue', 'xkcd:shamrock green'
        self.rc1, self.rc2, self.rc3 = 'xkcd:squash', 'xkcd:reddish', 'pink' 
        
        self.progress.set_panel('a') 
        self.draw_four_trumpets(self.axes[0:4]) 
        

        self.progress.set_panel('b') 
        self.draw_exome_popout_corrs(self.axes[4]) 
        DL.BoxKeys(self.axes[2]).add_trumpet_key('bottom-2') 
        DL.BoxKeys(self.axes[4]).add_rare_key('bottom',self.data) 
        
        self.progress.set_panel('c') 
        index_plots, rare_plots = [], [] 
        for i,(idx,ti) in enumerate(zip([8,12,16,20],self.options.indexTraits)): 
            sp = SP.POPplot(self.axes[idx], self, ti).draw_common_recovery() 
            index_plots.append(sp) 
            self.axes[idx-2].set_title(self.traits[ti].name.mini, fontsize=self.fs3, x=1, y=0.90, ha='center') 
        


        for i,(idx,ti) in enumerate(zip([5,9,13,17],self.options.indexTraits)):
            for j,(ax,k,c) in enumerate(zip(self.axes[idx:idx+3],['rareA','rareB','burden'],[self.rc1,self.rc2,self.rc3])): 
                sp = SP.POPplot(ax, self, ti).draw_body(k, yc1=c, yc2=c) 
                sp.draw_tail()
                sp.set_subtitle(k,fs=35) 
                rare_plots.append(sp)
        DL.BoxKeys(self.axes[15]).add_multi_key('bottom-4.25',clrs=[self.rc1,self.rc2,self.rc3,self.c1,self.c2])  
        

        self.progress.set_panel('d') 
        self.draw_tail_recovery([self.axes[-2],self.axes[-1]]) 
        DL.BoxKeys(self.axes[-2]).add_recovery_key(c1 = self.rc1, c2 = self.rc2, c3=self.rc3, c4='lime', RULE='LOWER') 
        DL.BoxKeys(self.axes[-2]).add_odds_key(c1 = self.c1, c2 = self.c2, RULE='LOWER') 
        return
    

    def split_recovery_traits(self): 
        TR = dd(list)  
        found, negs, nots, nosnps, yessnps = 0, 0, 0, 0, 0 
        for ti,T in self.traits.items(): 
            
            f1, e1 = T.vals['pop']['common-snp'].f1, T.vals['pop']['common-snp'].e1
            f2, e2 = T.vals['pop']['common-snp'].f2, T.vals['pop']['common-snp'].e2
            n_found, z_found, t_found = 0,0,0
            if f1: 
                if e1 > 0: t_found +=1 
                else:      n_found +=1 
            else:          z_found   +=1 
            if f2: 
                if e2 > 0: t_found +=1 
                else:      n_found +=1 
            else:          z_found +=1 
            found += t_found 
            negs += n_found 
            nots += z_found 
            if 'snp' not in T.lists.keys(): 
                nosnps += t_found
                continue 
            else: yessnps += t_found 

            p = T.vals['pop']['common-snp'] 
            r = T.vals['recovery']['combo']   
            FOUND=False 
            if p.e1 > 0 and p.f1 and r.total1 != 'NA': 
                FOUND=True 
                TR['Lower'].append([r.total1, T]) 
            if p.e2 > 0 and p.f2 and r.total2 != 'NA': 
                FOUND=True 
                TR['Upper'].append([r.total2, T]) 

        self.progress.report_result('Total of '+str(found+negs+nots)+' Trait Tails, '+str(nots)+' (no FDR-SIG POPout), '+str(negs)+' (Neg POPout), '+str(found)+' (Pos POPout)')  
        self.progress.report_result('In '+str(yessnps)+' of '+str(found)+' Tails w/Sig +POPout, (>0.01%) GWAS-SIG snps located and tested for reduction (via common+rare PRS)') 
        return TR 




    def validate_fractions(self, rTot, T, i): 
        if i == 0: rf,rS = [float(y) for y in T.vals['recovery']['combo'].frac1.split(',')], T.vals['recovery']['combo'].sig1
        else:      rf,rS = [float(y) for y in T.vals['recovery']['combo'].frac2.split(',')], T.vals['recovery']['combo'].sig2
        if rTot > 0 and all([r>=0 for r in rf]): return rf, rS 
        elif rTot < 0 and all([r<=0 for r in rf]): return rf, rS 
        else: 
            minI, maxI = rf.index(min(rf)), rf.index(max(rf)) 
            if rTot > 0: return [0 if j != maxI else rTot for j in range(len(rf))], rS
            else:        return [0 if j != minI else rTot for j in range(len(rf))], rS
            
    def validate_odds(self, T, OR, idx):
        if idx == 0: keys = ['odds-1','ci-1'] 
        else:        keys = ['odds-99','ci-99'] 
        odd_raw = [OR['common'].key[k] for k in keys] + [OR['combo'].key[k] for k in keys] 
        odd_data = [x/10.0 for x in odd_raw]
        pts, cis = [], [] 
        for j in [0,2]: 
            pt, c1, c2 = odd_data[j], odd_data[j+1], odd_data[j+1] 
            if pt > 1: 
                pt = 1 + (pt-1) * 0.25 
                c2 *= 0.25
                if odd_data[j] - c1 < 1: 
                    lp = 1 - (odd_data[j] - c1) 
                    rp = pt - 1 
                    c1 = lp + rp 
                else: c1 *= 0.25  
            elif pt + c2 > 1: 
                lp = 1-pt 
                rp = (c2 - (lp)) * 0.25 
                c2 = lp + rp 
            pts.append(pt) 
            cis.append([c1,c2])  
        z1, z2 =odd_raw[0], odd_raw[2] 
        rel_change = (z2-z1)/z1 
        tR = [odd_raw[0],odd_raw[0]-odd_raw[1],odd_raw[0]+odd_raw[1],odd_raw[2],odd_raw[2]-odd_raw[3],odd_raw[2]+odd_raw[3]]
        tR = [str(round(rr,3)) for rr in tR] 
        tR = [tR[0], tR[1]+'-'+tR[2], tR[3], tR[4]+'-'+tR[5]]
        return tR, rel_change, pts, cis 


    def odds_vs_r2_progress(self, all_pairs, sig_pairs): 

        for i,pair in enumerate([all_pairs, sig_pairs]): 
            traits, odds = pair 
            odd_change = np.mean(odds) 
            r_change = [] 
            for T in traits: 
                r1 = T.vals['corr'].key['common-R'] 
                r2 = T.vals['corr'].key['combo-R']
                R1 = r1*r1
                R2 = r2*r2 
                r_change.append((R2-R1)/R1) 
            
            rC = str(round(100*np.mean(r_change),1)) 
            oC = str(round(100*np.mean(odd_change),1)) 

            if i == 0: self.progress.report_result('Among All Traits R2/TailOdd Change: '+rC+', '+oC) 
            else:      self.progress.report_result('Alongside Sig Reduction: R2/TailOdd Change: '+rC+', '+oC) 
        return



    def draw_tail_recovery(self,axes, PRINT=False, cMax=0.29, cScale=5.0, offScale = 1): 
        
        if self.progress.SAVESRC: 
            w = self.progress.out3 
            r_names = ['POPoutReduction(rare>0.1%)','POPoutReduction(rare>0.01%)','POPoutReduction(Burden)','POPoutReduction(SumTotal)','Common-OR','Common-OR-CI','Common+Rare-OR','Common+Rare-OR-CI'] 
            w.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' % tuple(['Panel','Trait-ID','Tail'] + r_names))


        TR = self.split_recovery_traits() 
        leftEnd, self.offset, STEP1, STEP2 = -0.5, 0.12,  1, 1.02 
        barHt, MID2, rightEnd = 7.5, self.offset + STEP2, 2*self.offset + STEP2 + 1.128 
        rec_results = dd(list) 
        obs_traits, obs_odds, sig_traits, sig_odds = [], [], [], [] 
        for ki,k in enumerate(['Lower','Upper']): 
            self.ax, ax, yp = axes[ki], axes[ki], 0 
            tail_data = sorted(TR[k], key = lambda X: X[0], reverse=True) 

            for rTot,T in tail_data: 
                

                if T not in obs_traits: obs_traits.append(T) 
                self.ax.text(-0.235,yp-2.5,T.name.mini[0:15],fontsize=self.fs4, ha='center',va='center') 
                self.ax.add_patch(matplotlib.patches.Rectangle((leftEnd, yp-8),1.38+self.offset*2, 12, color=self.blockclr, ec = 'k', lw = 0, alpha=0.9, zorder=0,clip_on=False))
                self.ax.add_patch(matplotlib.patches.Rectangle((self.offset+STEP2, yp-8),rightEnd - (STEP2 + self.offset), 12, color=self.blockclr, ec = 'k', lw = 0, alpha=0.9, zorder=0,clip_on=False))
                yl, yp = yp - 2, yp - 14 
                ax.barh(yl,rTot,left=0+self.offset,height=barHt,facecolor='white',clip_on=False,alpha=0.95,lw=self.lw2,ec='k')
                my_offset, my_shrink = self.offset, 0 
                r_vals, rSig = self.validate_fractions(rTot, T, ki) 
                rec_results[rSig].append(rTot) 
                rec_results['ALL'].append(rTot) 
                for i,(val,clr) in enumerate(zip(r_vals,[self.rc1,self.rc2,self.rc3])): 
                    ax.barh(yl,val,left=my_offset,height=barHt,color=clr,clip_on=False,alpha=0.95,lw=0,ec=self.c2)
                    my_offset += val 
                if rSig == 'True': 
                    if my_offset < 1.1: ax.scatter(my_offset+0.017, yl+0.35, color = 'k', marker= '*', lw = 0.2, zorder=990, s=self.sz2) 
                    else:               ax.scatter(my_offset-0.03, yl+1, color ='k', marker='*', lw = 0.2,zorder=990, s = self.sz2,clip_on=False) 

                print_odds, rel_change, pts, cis = self.validate_odds(T, T.vals['odds'], ki) 
                obs_odds.append(rel_change) 
                if rSig == 'True': 
                    sig_traits.append(T) 
                    sig_odds.append(rel_change) 

                for pt,ci,clr in zip(pts, cis, [self.c1, self.c2]): 
                    ax.scatter(pt+MID2, yl, color=clr,ec='k',s=self.sz2,lw=self.lw3,alpha=0.8,zorder=10) 
                    ax.plot([pt+MID2-ci[0],pt+MID2+ci[1]],[yl,yl], color=clr,lw=self.lw2, alpha=0.6) 
            

                if self.progress.SAVESRC: 
                    w.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' % tuple([self.progress.panel, T.id, k] + r_vals+[rTot]+print_odds))
                    




            yp += 5 
            ax.set_xlim(leftEnd,rightEnd) 
            self.ax.set_yticks([]) 
            self.ax.axis('off') 
            for y1,y2 in [[barHt, yp],[yp,barHt]]: 
                for x1,x2 in [[leftEnd,self.offset+STEP1],[MID2,rightEnd]]: 
                    self.ax.plot([x1,x1],[y1, y2], linestyle = '-', linewidth=self.lw3,color='k',clip_on=False)
                    self.ax.plot([x2,x2],[y1, y2], linestyle = '-', linewidth=self.lw3,color='k',clip_on=False)
                    if x1 == MID2 and y1 == yp: 
                        xa,xb = x1 + 1.015, x1 + 1.035
                        self.ax.plot([x1,xa],[y1, y1], linestyle = '-', linewidth=self.lw3,color='k',clip_on=False)
                        self.ax.plot([xb,x2],[y1, y1], linestyle = '-', linewidth=self.lw3,color='k',clip_on=False)
                        self.ax.plot([xa-0.009,xa+0.01],[y1+2,y1-3],clip_on=False,lw=self.lw3,color='k') 
                        self.ax.plot([xb-0.009,xb+0.01],[y1+2,y1-3],clip_on=False,lw=self.lw3,color='k') 
                    else:
                        self.ax.plot([x1,x2],[y1, y1], linestyle = '-', linewidth=self.lw3,color='k',clip_on=False)
            ax.text(self.offset+0.3,yp-18,k+' Tail POPout Reduction', va='top',ha='center',fontsize=self.fs3-1)
            ax.text(self.offset+1.65,yp-18,k+' Tail Odds Ratios', va='top',ha='center',fontsize=self.fs3-1) 
            for i,a in enumerate([-0.1,0,0.20,0.40,0.60,0.8]): 
                self.ax.plot([a+self.offset, a+self.offset],[yp-2,barHt], linestyle = '-', color = 'k', zorder=10, linewidth=0.1, alpha=0.5, clip_on=False)
                if i == 0: self.ax.text(a+self.offset-0.02, yp -3, str(int(a*100))+'%', ha='center', va='top', fontsize=self.fs4) 
                elif i == 1: self.ax.text(a+self.offset, yp -3, str(int(a*100)), ha='center', va='top', fontsize=self.fs4) 
                else:      self.ax.text(a+self.offset, yp -3, str(int(a*100))+'%', ha='center', va='top', fontsize=self.fs4) 
            for pos in [1, 2.5, 5, 7.5, 10, 11.25, 12.5]: 
                x = round((pos/10.0) + STEP2, 2) + self.offset
                self.ax.plot([x,x],[yp-2,barHt], linestyle = '-', color = 'k', zorder=10, linewidth=0.1, alpha=0.5, clip_on=False)
                

                if pos <= 10: self.ax.text(x, yp -3, str(pos), ha='center', color='k',va='top', fontsize=self.fs4) 
                elif pos < 12:         self.ax.text(x, yp -3, '15', ha='center', color='k',va='top', fontsize=self.fs4) 
                else:         self.ax.text(x, yp -3, '20', ha='center', color='k',va='top', fontsize=self.fs4) 
        rLen, rPos, rSig = len(rec_results['ALL']), [r for r in rec_results['ALL'] if r > 0], rec_results['True'] 
        self.odds_vs_r2_progress([obs_traits, obs_odds],[sig_traits, sig_odds]) 
        self.progress.report_result(str(rLen)+' Tails Tested for Reduction: '+str(len(rPos))+' >0, '+str(len(rSig))+' Significant')  
        self.progress.report_result('Mean Reduction (all,pos,sig): '+', '.join([str(round(np.mean(x),3)) for x in [rec_results['ALL'],rPos,rSig]])) 
        return
 






    def draw_exome_popout_corrs(self, ax): 
        
        if self.progress.SAVESRC: self.progress.out3.write('%s,%s,%s,%s,%s\n' % ('Panel', 'Trait-ID','Tail','POPoutEffect','ExomeHits'))
        X,Y = [], [] 
        for ti,T in self.traits.items(): 
            pos, neg = 0, 0 
            for k in ['rare','burden']: 
                try: kd = T.pts['backman'][k].effects
                except KeyError: continue 
                pos += len([z for z in kd if z > 0])
                neg += len([z for z in kd if z <= 0]) 
            if pos + neg > 0: 
                e1, e2, f1, f2  = [T.vals['pop']['common-snp'].key[mm] for mm in ['e1','e2','f1','f2']]
                for i,(x,y,m) in enumerate([[e1,neg,'v'],[e2,pos,'^']]): 
                    ax.scatter(x, y,marker = m, s=self.sz1,color=T.group_color, linewidth=0.1,alpha=0.8, ec = 'black', clip_on=False) 
                    X.append(x) 
                    Y.append(y) 
                    if self.progress.SAVESRC: 
                        if i == 0: self.progress.out3.write('%s,%s,%s,%s,%s\n' % (self.progress.panel,T.id,'Lower',x,y)) 
                        else:      self.progress.out3.write('%s,%s,%s,%s,%s\n' % (self.progress.panel,T.id,'Upper',x,y)) 
                    if ti in self.options.indexTraits+[50,3581]: 
                        if x > 0.1 and x == max([e1,e2]): 
                            if y < 4: ax.text(x+0.005,y,T.name.mini, ha='left', va='top',fontsize=self.fs4, fontweight='bold') 
                            elif i == 1: ax.text(x,y+1.2,T.name.mini, ha='center', va='bottom',fontsize=self.fs4, fontweight='bold') 
                            elif y > 20: ax.text(x,y+1,T.name.mini, ha='center', va='bottom',fontsize=self.fs4, fontweight='bold') 
                            else:        ax.text(x,y-1.2,'\n'.join(T.name.mini.split()), ha='center', va='top',fontsize=self.fs4, fontweight='bold') 
        



        R,pv = DV.add_scatter_corr(ax,X,Y) 
        self.progress.report_result('POPout/ExomeHit Correlation: '+str(round(R,3))+', pv='+str(pv))
        lms = DV.AxLims(ax,ylab='Exome hits in tail', fs = self.fs3, COMMANDS=['nospines']) 
        ax.set_xlabel('$POPout$ Effect Size',fontsize=self.fs3, labelpad=0.5) 
        return





    def draw_four_trumpets(self, axes, rc = 'xkcd:cherry red'):
        if self.progress.SAVESRC: self.progress.out3.write('%s,%s,%s,%s\n' % ('Panel', 'Trait-ID','snpType','pairedValues(x=maf|y=beta)'))
        for i,ti in enumerate(self.options.indexTraits): 
            ax = axes[i]
            if ti not in self.traits: 
                DV.draw_blank(ax) 
                continue 
            T = self.traits[ti] 
            for j,(k,c1,c2,lw) in enumerate(zip(['common','burden','rare'],['grey','white',rc],['grey',rc,rc],[self.lw3,self.lw2,self.lw2])): 
                try: 
                    kd = T.pts['backman'][k]
                    mafs, betas = [math.log(x,self.base) for x in kd.mafs], kd.effects 
                    ax.scatter(mafs,betas,s=[1+y*y*10 for y in betas],fc=c1, ec=c2,lw=lw, alpha=0.7) 
                    if self.progress.SAVESRC: 
                        pairs = ";".join([str(a)+'|'+str(b) for a,b in zip(kd.mafs, kd.effects)]) 
                        self.progress.out3.write('%s,%s,%s,%s\n' % (self.progress.panel, T.ti, k+'Effects',pairs)) 
                except KeyError: continue 

            if i in [2,3]: 
                ax.set_xlabel('Minor Allele Frequency',fontsize=self.fs4,labelpad=-1) 
                xl = [0.00001, 0.0001, 0.001, 0.01, 0.1, 0.45]
                xticks = [math.log(x,self.base) for x in xl] 
                xl[-1] = 0.5
                xl[0] = '10^{-5}'
                xl[1] = '10^{-4}'
                xl = ['$'+str(x)+'$' for x in xl] 
                if i == 3: 
                    ax.set_xticks(xticks)
                    ax.set_xticklabels(xl) 
                else:
                    ax.set_xticks(xticks[0:-1])
                    ax.set_xticklabels(xl[0:-1]) 
            else:
                ax.set_xticks([]) 
            if i in [0,2]: ax.set_ylabel('Effect Size (z)',fontsize=self.fs3, labelpad=-1) 
            else:          ax.set_yticks([]) 
            ax.set_ylim(-2.9,2.9)
            ax.set_ylim(-2.9,2.9)
            ax.set_xlim(math.log(0.000004,self.base),math.log(0.5,self.base))
            ax.set_xlim(math.log(0.000003,self.base),math.log(0.6,self.base))
            

            ax.text(-0.25,2.8,T.name.cornerStyle, fontsize=self.fs3, ha='right', va='top') 
        return




