import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path: sys.path.insert(0, HERE)
from util.Util   import * 
from util import drawSims    as DI
from util import drawVarious as DV
import pandas as pd

# set_xlabel

class MyFigure:
    def __init__(self, options, traits, progress, figName = None): 
        self.options, self.traits, self.data, self.progress, self.figName = options, traits.members, traits, progress, figName
        self.lib = DI.SlimFig(self) 
        self.fs0, self.fs1, self.fs2, self.fs3, self.fs4, self.fs5 = 12,10, 9,7.5,6, 5
        self.lw1,self.lw2,self.lw3 = 1.5, 1.15,0.85
        self.sz1,self.sz2,self.sz3 = 20,15,10
        if figName == 'sim1': self.draw = self.draw_one 
        elif figName == 'sim2': self.draw = self.draw_two 
        else:                   self.draw = self.draw_three 
        

    def finish(self):
        for ax, lab in zip(self.axes, list('abcdefgh')): self.lib.add_panel_label(ax, lab,x=-0.08,  y=0.95)
        self.leg.get_frame().set_linewidth(0.8)
        self.leg.get_frame().set_edgecolor('black')
        self.leg.get_frame().set_facecolor('white')
        if self.figName == 'sim3': plt.subplots_adjust(left=0.05, bottom=0.08, right=0.96, top=0.95,wspace=0.20,hspace=0.5) 
        else:                 plt.subplots_adjust(left=0.05, bottom=0.18, right=0.98, top=0.95,wspace=0.3,hspace=0.5) 
        figPath = self.options.out+self.figName+'.pdf' 
        self.progress.save('(Figure Saved: '+figPath+')')
        plt.savefig(figPath, dpi=500) 
        plt.clf() 


    def setup(self): 
        self.fig, self.axes = matplotlib.pyplot.gcf(), []
        self.WD, self.ax_index, self.cols = 7.2, 0, 2 
        if self.figName == 'sim3':  self.rows, self.HT = 4, 8
        else:                       self.rows, self.HT = 2, 4.5
        for i in range(self.rows): 
            for j in range(self.cols): 
                self.axes.append(plt.subplot2grid((self.rows,self.cols),(i,j),rowspan = 1,colspan =1))                                                                       
        self.fig.set_size_inches(self.WD,self.HT)                                                                                                                                  

    #################### FIGURE 1 #############################################

    def draw_one(self): 
        self.colors = {'110000': '#1b9e77', '150000': '#d95f02', '200000': '#7570b3'}
        self.labels = {'110000': '10k', '150000': '50k', '200000': '100k'}
        self.linestyles = {'110000': '-', '150000': '--', '200000': ':'}
        self.cycles = ['110000', '150000', '200000']
        self.setup()  
        data = self.lib.load_single() 
        specs = [('f1', 'maf1', 12),('f1', 'maf1_top', 12),('f100', 'maf1_top', 12),('f1', 'n1_10_top', 12)]
        


        for ax, (factor, maf_class2, ymax) in zip(self.axes, specs):   
            self.plot_one_panel(ax, self.subset_df_one(data, factor, maf_class2), ymax, factor+'@'+maf_class2)
        

        handles, labels = self.axes[0].get_legend_handles_labels()
        self.leg = self.fig.legend(handles, labels, loc='lower center', ncol=3, bbox_to_anchor =(0.5, 0.03), frameon=True, fontsize=self.fs2)
        self.finish() 
        return
   



    def subset_df_one(self, data, factor, maf_class2, dist='gammacustom_mean01'):
        return data[(data['factor'] == factor) & (data['maf_class2'] == maf_class2) & (data['dist'] == dist)].copy()

    def style_axis_one(self, ax, ymax):
        ax.axhline(1, linestyle='--', linewidth=self.lw3, color='k')
        ax.set_ylim(0, ymax)
        ax.set_xlabel('Trait quantiles', fontsize=self.fs2)
        ax.set_ylabel('Rare Enrichment', fontsize=self.fs2)
        self.lib.clean_axis(ax)

    def plot_one_panel(self, ax, df, ymax, info=None):
        
        if info == 'f1@maf1': dt = 'Weak,1,All' 
        elif info == 'f1@maf1_top': dt = 'Weak,1,Large'
        elif info == 'f100@maf1_top': dt = 'Strong,1,Large'
        elif info == 'f1@n1_10_top': dt = 'Strong,0.05,Large'
        else: dt = info  



        if 'prs_bin_num' not in df.columns:
            df = df.copy()
            df['prs_bin_num'] = pd.to_numeric(df['prs_bin2'])
        for cyc in self.cycles:
            sub = df[df['cycle'] == cyc].sort_values('prs_bin_num')
            if len(sub) == 0: continue
            
            #print(sub['prs_bin_num'], sub['mean_odds'])      
            
            X = [x for x in sub['prs_bin_num']]
            Y = [x for x in sub['mean_odds']]
            print('EnrichmentByTime', dt, self.labels[cyc], 'X', ",".join([str(x) for x in X])) 
            print('EnrichmentByTime', dt, self.labels[cyc], 'Y', ",".join([str(round(y,2)) for y in Y])) 
            #ax.plot(sub['prs_bin_num'], sub['mean_odds'], color=self.colors[cyc], linewidth=self.lw1, alpha=0.6, linestyle=self.linestyles[cyc], label=self.labels[cyc])
            ax.plot(X, Y, color=self.colors[cyc], linewidth=self.lw1, alpha=0.6, linestyle=self.linestyles[cyc], label=self.labels[cyc])
        



        self.style_axis_one(ax, ymax)






    #################### FIGURE 1 #############################################
    def draw_two(self): 
        self.colors = {'gammacustom_mean005': '#1b9e77','gammacustom_mean01': '#d95f02','gammacustom_mean02': '#7570b3','gaussian': '#e7298a', }
        self.labels = {'gammacustom_mean005': 'gamma(u=0.05)','gammacustom_mean01': 'gamma(u=0.1)','gammacustom_mean02': 'gamma(u=0.2)','gaussian': 'gaussian N(0,1)',}
        self.linestyles = {'gammacustom_mean005': '-','gammacustom_mean01': '--','gammacustom_mean02': ':','gaussian': '-',}
        self.dists = ['gammacustom_mean005', 'gammacustom_mean01', 'gammacustom_mean02', 'gaussian']
        self.setup()  
        self.data = self.lib.load_double() 
        specs = [('f1', 'maf1', 12),('f1', 'maf1_top', 12),('f100', 'maf1_top', 12),('f1', 'n1_10_top', 12)]
        for ax, (factor, maf_class2, ymax) in zip(self.axes, specs):   
            self.plot_panel_two(ax, self.subset_df_two(self.data, factor, maf_class2), ymax, factor+'@'+maf_class2)

        handles, labels = self.axes[0].get_legend_handles_labels()
        self.leg = self.fig.legend(handles, labels, loc='lower center', ncol=2, bbox_to_anchor =(0.5, 0.01), frameon=True, fontsize=self.fs3)
        self.finish() 


    def subset_df_two(self, data, factor, maf_class2, cycle='110000'):
        return data[(data['factor'] == factor) & (data['maf_class2'] == maf_class2) & (data['cycle'] == cycle)].copy()

    def style_axis_two(self, ax, ymax):
        ax.axhline(1, linestyle='--', linewidth=self.lw3, color='k')
        ax.set_ylim(0, ymax)
        ax.set_xlabel('Trait quantiles', fontsize=self.fs2)
        ax.set_ylabel('Rare Enrichment', fontsize=self.fs2)
        self.lib.clean_axis(ax)

    def plot_panel_two(self, ax, df, ymax, info=None):
        
        if info == 'f1@maf1': dt = 'Weak,1,All' 
        elif info == 'f1@maf1_top': dt = 'Weak,1,Large'
        elif info == 'f100@maf1_top': dt = 'Strong,1,Large'
        elif info == 'f1@n1_10_top': dt = 'Strong,0.05,Large'
        else: dt = info  



        if 'prs_bin_num' not in df.columns:
            df = df.copy()
            df['prs_bin_num'] = pd.to_numeric(df['prs_bin2'])
        for dist in self.dists:
            sub = df[df['dist'] == dist].sort_values('prs_bin_num')
            if len(sub) == 0: continue
            

            X = [x for x in sub['prs_bin_num']]
            Y = [x for x in sub['mean_odds']]
            print('EnrichmentByDist', dt, self.labels[dist], 'X', ",".join([str(x) for x in X])) 
            print('EnrichmentByDist', dt, self.labels[dist], 'Y', ",".join([str(round(y,2)) for y in Y])) 

            ax.plot(sub['prs_bin_num'], sub['mean_odds'], color=self.colors[dist], linewidth=self.lw1,linestyle=self.linestyles[dist], alpha=0.85, label=self.labels[dist])
        self.style_axis_two(ax, ymax)

    #################### FIGURE 3 #############################################
    def draw_three(self): 
        self.pt_size = 18 
        self.grp_colors = {'selection': 'darkred', 'neutrality': '#7f7f7f'}
        self.grp_labels = {'selection': 'Selection', 'neutrality': 'Neutrality'}
        self.dist_order = ['mean005', 'mean01', 'mean02', 'gaussian']
        self.dist_titles = {'mean005': 'gamma('+'$\gamma$'+'=0.05)', 'mean01': 'gamma('+'$\gamma$'+'=0.1)', 'mean02': 'gamma('+'$\gamma$'+'=0.2)', 'gaussian': 'gaussian '+'$N$'+'(0,1)'}
        self.selection_order = ['weak selection', 'strong selection']
        self.selection_titles = {'weak selection': 'Weak selection', 'strong selection': 'Strong selection'}
        self.plotbins = list(range(1, 11)) + list(range(15, 90, 5)) + list(range(90, 101))
        self.setup()  
        self.data = self.lib.load_double('popout') 
        specs = []
        for dist in self.dist_order:
            for selection in self.selection_order:
                specs.append((dist, selection))
        



        for ax, (dist, selection) in zip(self.axes, specs):
            self.plot_panel_three(ax, self.subset_df_three(self.data, dist, selection), dist+'@'+selection.split()[0].capitalize())
            ax.text(0.50, 0.94, self.dist_titles[dist] + '\n' + self.selection_titles[selection],transform=ax.transAxes, ha='center', va='top', fontsize=self.fs3)
            lms = DV.AxLims(ax)  


        handles, labels = self.axes[0].get_legend_handles_labels()
        seen, uniq_h, uniq_l = set(), [], []
        for h, l in zip(handles, labels):
            if l not in seen:
                uniq_h.append(h)
                uniq_l.append(l)
                seen.add(l)
        self.leg = self.fig.legend(uniq_h, uniq_l, loc='lower center', ncol=2, bbox_to_anchor=(0.5,0.001), frameon=True, fontsize=self.fs3)
        self.finish() 
        return

    def subset_df_three(self, data, dist, selection):
        use = data[(data['selection'] == selection) & (data['cycle'].isin(['100000', '110000', 100000, 110000]))].copy()
        use = use[use['prs_bin'].isin(self.plotbins)]
        use = use[use['dist'] == dist]
        return use.sort_values(['Group', 'prs_bin'])

    def style_axis_three(self, ax):
        ax.axhline(0, linestyle='-', linewidth=self.lw3, color='k')
        ax.set_ylim(-0.5, 3.0)
        ax.set_xlim(-5, 106)
        ax.set_xticks([1, 20, 40, 60, 80, 100])
        ax.set_xlabel('Trait Quantiles', fontsize=self.fs2)
        ax.set_ylabel('POPout Effects', fontsize=self.fs2)
        self.lib.clean_axis(ax)

    def plot_panel_three(self, ax, df, info=None):
        
        dist,sel = info.split('@')  
        if dist[0:4] == 'mean': dist = 'gamma0.'+dist[5::] 
        
        dt = dist+','+sel 
        #print('EnrichmentByDist', dt, self.labels[dist], 'X', ",".join([str(x) for x in X])) 
        #print('EnrichmentByDist', dt, self.labels[dist], 'Y', ",".join([str(round(y,2)) for y in Y])) 



        for group in ['selection', 'neutrality']:
            sub = df[df['Group'] == group]
            if len(sub) == 0: continue
            
            lab = self.grp_labels[group] 
            
            zt = dt+','+lab 
            X = ",".join([str(x) for x in sub['prs_bin']])
            Y = ",".join([str(round(y,4)) for y in sub['mean']]) 
            
            yL = ",".join([str(round(y,4)) for y in sub['lower']])
            yH = ",".join([str(round(y,4)) for y in sub['upper']])
            
            #print(len(X)) 
            #print(Y[0:3]) 
            
            #X = ",".join([str(x) for x in X]) 
            
            #Y = ",".join([str(round(y,2)) for y in Y])) 

            
            print('POPoutByDist', dt, lab, 'X', X) 
            print('POPoutByDist', dt, lab, 'Y', Y) 
            print('POPoutByDist', dt, lab, 'yL', yL) 
            print('POPoutByDist', dt, lab, 'yH', yH) 



            ax.errorbar(sub['prs_bin'],sub['mean'],yerr=[sub['mean']-sub['lower'],sub['upper']-sub['mean']],fmt='o',color=self.grp_colors[group],ecolor='k',elinewidth=self.lw2,capsize=0, markersize=2.9,alpha=0.6,label=self.grp_labels[group])
        self.style_axis_three(ax)












