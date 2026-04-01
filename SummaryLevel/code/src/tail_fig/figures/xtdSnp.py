import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path: sys.path.insert(0, HERE)
from util.Util   import * 
from util import drawSnps as DS

class MyFigure:
    def __init__(self, options, traits, progress, figName = None): 
        self.options, self.traits, self.data, self.figName = options, traits.members, traits, figName
        self.progress = progress.update(self) 
        self.snpTraits = [T for T in self.traits.values() if 'snp' in T.lists] 
        self.determine_type(figName) 
        self.separateSnpsByType() 

    def determine_type(self, figName): 
        try:    req = int(figName[-1]) 
        except: req = 1 
        if   req  == 1 or req % 4 == 1:  self.my_type = 'annotated_rares' 
        elif req  == 2 or req % 4 == 2:  self.my_type = 'annotated_burdens' 
        elif req  == 3 or req % 4 == 3:  self.my_type = 'other_burdens' 
        return 

    def separateSnpsByType(self): 
        self.snps = {} 
        for T in self.snpTraits: 
            if self.my_type == 'annotated_rares': 
                snps = [s for s in T.lists['snp'] if s.rs.upper() != 'BURDEN' and s.annos != 'NA'] 
                for s in snps: 
                    if s.loc not in self.snps: self.snps[s.loc] = DS.RareSnp(s.loc, s) 
                    self.snps[s.loc].add(T, s) 
            else:   
                if self.my_type == 'annotated_burdens': snps = [s for s in T.lists['snp'] if s.rs.upper() == 'BURDEN' and s.annos != 'NA'] 
                else:                                   snps = [s for s in T.lists['snp'] if s.rs.upper() == 'BURDEN' and s.annos == 'NA'] 
                for s in snps: 
                    if s.loc not in self.snps: self.snps[s.loc] = DS.RareSnp(s.loc, s, 'burden') 
                    self.snps[s.loc].add(T, s) 
        sorted_snps = sorted([s for s in self.snps.values()], key = lambda X: len(X.hits), reverse=True)  
        if self.my_type == 'annotated_rares': self.my_data = self.process_rares(sorted_snps) 
        else:                                 self.my_data = self.process_burdens(sorted_snps) 
        return 

    def draw(self): 
        self.setup() 
        self.create() 
        self.finish() 
        return

    def setup(self): 
        self.i1, self.i2 = 'whitesmoke','gainsboro'
        self.fig, self.axes = matplotlib.pyplot.gcf(), []
        self.WD, self.HT = 7.2, 9.7
        if self.my_type   == 'annotated_rares': cs = [45,30,25] 
        elif self.my_type == 'annotated_burdens':  cs = [32,35,33] 
        elif self.my_type == 'other_burdens':      cs = [34,33,33] 
        else:                                      self.progress.error('Unknown Snp Type: ', self.my_type)
        s_rows = [x[-1] for x in self.my_data] 
        self.cols, self.rows = 100, sum(s_rows) + 1 
        self.axes.append(plt.subplot2grid((self.rows,self.cols),(0,0),rowspan = 1,colspan =cs[0]))                                                                       
        self.axes.append(plt.subplot2grid((self.rows,self.cols),(0,cs[0]),rowspan = 1,colspan =cs[1]))                                                                       
        self.axes.append(plt.subplot2grid((self.rows,self.cols),(0,cs[0]+cs[1]),rowspan = 1,colspan =cs[2]))                                                                       
        rl = 1
        for rs in s_rows: 
            self.axes.append(plt.subplot2grid((self.rows,self.cols),(rl,0),rowspan = rs,colspan =cs[0]))                                                                       
            self.axes.append(plt.subplot2grid((self.rows,self.cols),(rl,cs[0]),rowspan = rs,colspan =cs[1]))                                                                       
            self.axes.append(plt.subplot2grid((self.rows,self.cols),(rl,cs[0]+cs[1]),rowspan = rs,colspan =cs[2]))                                                                       
            rl += rs 
        self.fig.set_size_inches(self.WD,self.HT)                                                                                                                                  
        self.ax_index,self.xLoc,self.fq1,self.fq2 = 0, 1, 24, 22                

    def create(self): 
        dt = DS.SnpTable(self, self.my_type).initialize(self.axes[0:3],c1=self.i1,c2=self.i2) 
        self.ax_index += 3 
        count = 0 
        for i,snp_data in enumerate(self.my_data): 
            dt.add_snp(self.axes[self.ax_index: self.ax_index+3], snp_data, i, len(self.my_data)) 
            self.ax_index += 3
        return self


    def finish(self):
        plt.subplots_adjust(left=0.015, bottom=0.01, right=0.99, top=0.98,wspace=0.0,hspace=0.03) 
        self.progress.save() 

    def process_hits(self, s): 
        DN,UP = [], [] 
        for beta,pv,T  in s.hits: 
            if beta < 0: DN.append([beta*beta,T]) 
            else:        UP.append([beta*beta,T]) 
        DN.sort(reverse=True, key=lambda X: X[0]) 
        UP.sort(reverse=True, key=lambda X: X[0]) 
        hits = [[x[1].name.snp for x in DN],[x[1].name.snp for x in UP]] 
        return hits 

    def process_rares(self, snps): 
        p_key, p_data = dd(list), [] 
        for s in snps: 
            my_data = [":".join(s.loc.split('chr')[1].split(':')[0:2]), s.rs, s.maf, s.type, s.genes] 
            hits    = self.process_hits(s)  
            snp_data = [my_data, hits, [" ".join(a.split('_')) for a in s.annos]] 
            rows = 1  
            if len(hits[0]) > 0 and len(hits[1]) > 0: rows = 2
            else:                                     rows = 1 
            p_key[rows].append([snp_data,rows]) 
        R1, R2 = p_key[1], p_key[2] 
        if len(R1) > 2 * len(R2): 
            rd, k = [], 0 
            for i,r in enumerate(R1): 
                rd.append(r) 
                if i % 2 != 0 and k < len(R2): 
                    rd.append(R2[k]) 
                    k+= 1 
            return rd 
        my_rows = R1 + R2  
        random.shuffle(my_rows) 
        return my_rows 
    
    def process_burdens(self, snps): 
        p_key, p_data = dd(list), [] 
        for s in snps: 
            my_data = [s.loc, s.genes] 
            hits    = self.process_hits(s)  
            snp_data = [my_data, hits, [" ".join(a.split('_')) for a in s.annos]] 
            rows = 1  
            if len(hits[0]) > 0 and len(hits[1]) > 0: rows = 2
            else:                                     rows = 1 
            p_key[rows].append([snp_data,rows]) 
        R1, R2 = p_key[1], p_key[2] 
        raw_data = R1 + R2  
        if self.my_type == 'other_burdens': 
            random.shuffle(raw_data)
            return [[rd[0],1] for rd in raw_data]
            sys.exit() 
        if len(R1) > 2 * len(R2): 
            rd, k = [], 0 
            for i,r in enumerate(R1): 
                rd.append(r) 
                if i % 2 != 0 and k < len(R2): 
                    rd.append(R2[k]) 
                    k+= 1 
            return rd 
        else: 
            random.shuffle(raw_data)
            return raw_data 









