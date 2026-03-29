import sys,os                                                                                                                                                                                                             
HERE = os.path.dirname(os.path.abspath(__file__))             
if HERE not in sys.path: sys.path.insert(0, HERE)
from Util import *
import drawVarious as DV

class PredPlot:
    def __init__(self, fig, sz=3, lw1=0.9, lw2=0.3):
        self.fig, self.traits, self.options, self.progress = fig, fig.traits, fig.options, fig.progress
        self.sz, self.lw1, self.lw2 = sz, lw1, lw2
        if self.progress.SAVESRC: self.progress.start_src('%s,%s,%s,%s,%s\n',('Panel', 'Trait-ID','PseudoDisease','DataType','Values')) 

    def draw_index_pair(self, axes): 
        if self.options.indexTraits[1] in self.traits:   self.draw_odds(self.traits[self.options.indexTraits[1]], axes[0:4])
        elif self.options.indexTraits[0] in self.traits: self.draw_odds(self.traits[self.options.indexTraits[0]], axes[0:4])
        else:                                            self.draw_odds(None, axes[0:4])
        if self.options.indexTraits[2] in self.traits:   self.draw_odds(self.traits[self.options.indexTraits[2]], axes[4:8])
        elif self.options.indexTraits[3] in self.traits: self.draw_odds(self.traits[self.options.indexTraits[3]], axes[4:8])
        else:                                            self.draw_odds(None, axes[4:8])
        return
  
    def draw_odds(self, T, axes, fs1=9, fs2=6, fs3=5,clr1='blue',clr2='darkorange',clr3='orange', QT=False): 
        if T is None: 
            for ax in axes: DV.draw_blank(ax) 
            return
        smartX = [4.0, 11.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 89.0, 96.0] 
        smartXl = ['$<5$', '5-15', '15-25', '25-35', '35-45', '45-55', '55-65', '65-75', '75-85', '85-95', '$>95$']
        axes[1].set_title(T.name.flat, fontsize=fs1, x=0, y= 0.95)  
        for i,k in enumerate(['Lower1', 'Upper1', 'Lower25', 'Upper25']): 
            ax, p = axes[i], T.pts['pred'][k] 
            ax.plot(p.X, p.null, color=clr2,linestyle='--',lw=self.lw1) 
            ax.plot(p.X, p.Y, color=clr1, lw=self.lw2) 
            nW = [] 
            for j,(x,y,n,c) in enumerate(zip(p.X,p.Y,p.null, p.ci)): 
                ax.plot([x,x],[y-c,y+c], lw=self.lw2, color=clr1) 
                ax.scatter(x,y,color=clr1, s=self.sz, marker='o', zorder=22) 
                if n > y: nW.append(j) 
                else: 
                    if len(nW) > 1: 
                        nA,nB = nW[0], nW[-1]+2 
                        ax.fill_between(p.X[nA:nB], p.null[nA:nB], p.Y[nA:nB], color = clr3, alpha=0.5) 
                    nW = [] 
            if len(nW) > 1: ax.fill_between(p.X[nW[0]::], p.null[nW[0]::], p.Y[nW[0]::], color = clr3, alpha=0.5) 
            if i in [2,3]:
                ax.set_xticks(smartX) 
                ax.set_xticklabels(smartXl, fontsize=fs3-1, rotation=45)        
                if QT: ax.set_xlabel('PRS Quantiles',fontsize=fs2)
            else: ax.set_xticks([]) 
            if i in [0,2]: 
                ax.set_ylabel('Odds Ratio', fontsize=fs2) 
                y1, y2 = ax.get_ylim() 
                if y2 > 5.5 and y2 < 6.5: ax.set_yticks([1,3,5]) 
                elif y2 > 3.5 and y2 < 4.5: ax.set_yticks([1,3]) 
                ys = (y2-y1)/8.0
                ax.set_ylim(0,y2) 
            else:   
                ax.set_ylim(0,y2) 
                ax.set_yticks([]) 
            k_str = 'Prediction of '+k[0:5]+' '+k[5::]+'%' 
            ax.text(50, y2-ys, k_str,fontsize=fs2, ha='center',va='center') 
            if self.progress.SAVESRC: 
                Xb = ";".join([str(int(x)) for x in p.X]) 
                Ns = ";".join([str(x) for x in p.null]) 
                Ys = ";".join([str(x) for x in p.Y]) 
                Yi = ";".join(["-".join([str(round(y-c,4)),str(round(y+c,4))]) for y,c in zip(p.Y, p.ci)])
                w = self.progress.out3
                for n,v in [['Xbins',Xb],['ExpectedOdds',Ns],['ObservedOdds',Ys],['95%CI',Yi]]: 
                    w.write('%s,%s,%s,%s,%s\n' % (self.progress.panel, T.id, "_".join(k_str.split('of ')[-1].split()),n,v)) 
        return 




