import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path: sys.path.insert(0, HERE)
from util.Util   import * 
#from util import drawScatter as SP 
from util import drawSnps as DT
#from util import drawVarious as DV 



MK = {'0.1%-1%': '<1%', '0.01%-0.1%': '<0.01%', '~0.1%': '~0.1%', '~0.01%': '~0.01%','~1%': '~1%'} 
SK = {'3_prime_utr': '3pUTR', '5_prime_utr': '5pUTR','missense-snp': 'missense','synonymous-snp': 'synonymous','missense-indel': 'missense'} 




class RareSnp:
    def __init__(self, loc, s, group = 'rare'): 
        self.loc, self.group = loc, group
        self.hits, self.genes, self.annos = [], s.gene.split(';'), s.annos.split(';') 
        s.maf = MK[s.maf]        
        if len(self.genes) > 1: self.genes = ',\n'.join(self.genes) 
        else:                   self.genes = self.genes[0] 
        
        


        for i in range(len(self.annos)): 
            if len(self.annos[i].split('_')) == 1: continue 
            x = self.annos[i].split("_") 
            if 'related_disorder' in self.annos[i] and x[-1] == 'disorder': self.annos[i] = self.annos[i].split('_disorder')[0]  
            elif x[0] in ['familial','hereditary','recessive']: self.annos[i] = "_".join(x[1::])
            else: continue 
        
        self.annos = sorted(list(set(self.annos)) , key = lambda X: len(X)) 
        self.annos = [a.capitalize() for a in self.annos] 

        if self.group == 'burden': 
            self.add = self.add_burden 
            self.masks, self.mafs = [s.type], [s.maf] 
        else:                     
            self.add = self.add_rare 
            self.rs, self.type, self.maf = s.rs, s.type, s.maf
            if self.type in SK: self.type = SK[self.type] 
            if len(self.type.split(';')) > 1: self.type = '\n'.join(self.type.split(';')) 



    def add_burden(self, T, k): 
        self.hits.append([k.beta, k.pv, T])  
        self.masks.append(k.type) 
        self.mafs.append(k.maf) 

    
    def add_rare(self, T, k): 
        self.hits.append([k.beta, k.pv, T])  







class MyFigure:
    def __init__(self, options, traits, progress, figName = None): 
        self.options, self.traits, self.data, self.progress, self.figName = options, traits.members, traits, progress, figName
        self.snpTraits = [T for T in self.traits.values() if 'snp' in T.lists] 
        self.C1 = 'xkcd:very light blue' 
        self.C1 = 'xkcd:very light pink' 
        self.C2 = 'xkcd:off white' 
        self.E1, self.E2 = 'darkslategray','gray' 




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



        #for i in range(3,self.rows,1):                                                                                                                                        
        #    self.axes.append(plt.subplot2grid((self.rows,self.cols),(i,0),rowspan = 2,colspan =cs[0]))                                                                       
        #    self.axes.append(plt.subplot2grid((self.rows,self.cols),(i,cs[0]),rowspan = 2,colspan =cs[1]))                                                                       
        #    self.axes.append(plt.subplot2grid((self.rows,self.cols),(i,cs[0]+cs[1]),rowspan = 2,colspan =cs[2]))                                                                       
        self.fig.set_size_inches(self.WD,self.HT)                                                                                                                                  
        self.ax_index,self.xLoc,self.fq1,self.fq2 = 0, 1, 24, 22                



    def draw_one(self, req): 
        
        self.snps = {} 
        if req == 1 or req % 4 == 1:    self.my_type = 'annotated_rares' 
        elif req == 2 or req % 4 == 2:  self.my_type = 'annotated_burdens' 
        elif req == 3 or req % 4 == 3:  self.my_type = 'other_burdens' 
        else:                           self.progress.error('Unrecognized Snp Type')  
        for T in self.snpTraits: 
            if self.my_type == 'annotated_rares': 
                snps = [s for s in T.lists['snp'] if s.rs.upper() != 'BURDEN' and s.annos != 'NA'] 
                for s in snps: 
                    if s.loc not in self.snps: self.snps[s.loc] = RareSnp(s.loc, s) 
                    self.snps[s.loc].add(T, s) 
            else:   
                if self.my_type == 'annotated_burdens': snps = [s for s in T.lists['snp'] if s.rs.upper() == 'BURDEN' and s.annos != 'NA'] 
                else:                                   snps = [s for s in T.lists['snp'] if s.rs.upper() == 'BURDEN' and s.annos == 'NA'] 
                for s in snps: 
                    if s.loc not in self.snps: self.snps[s.loc] = RareSnp(s.loc, s, 'burden') 
                    self.snps[s.loc].add(T, s) 

        sorted_snps = sorted([s for s in self.snps.values()], key = lambda X: len(X.hits), reverse=True)  


        if self.my_type == 'annotated_rares': self.my_data = self.process_rares(sorted_snps) 
        else:                                 self.my_data = self.process_burdens(sorted_snps) 
        self.setup() 
        

        self.create() 
        
        self.finish(self.figName+'.pdf') 
        figPath = self.options.out+self.figName+'.pdf' 
        self.progress.save('(Figure Saved: '+figPath+')')
        return



    def create(self): 
        dt = DT.SnpTable(self, self.my_type).initialize(self.axes[0:3],c1=self.i1,c2=self.i2) 
        self.ax_index += 3 
        count = 0 
        #self.clr = self.C1
        
        for i,snp_data in enumerate(self.my_data): 
            dt.add_snp(self.axes[self.ax_index: self.ax_index+3], snp_data, i, len(self.my_data)) # self.clr) 

            self.ax_index += 3
            #if self.clr == self.C1: self.clr = self.C2 
            ##else:                   self.clr = self.C1 
        return self


    def finish(self,fname):
        plt.subplots_adjust(left=0.015, bottom=0.01, right=0.99, top=0.98,wspace=0.0,hspace=0.03) 
        plt.savefig(self.options.out+fname, dpi=500) 
        plt.clf() 





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









