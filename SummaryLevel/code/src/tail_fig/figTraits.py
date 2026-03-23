import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path: sys.path.insert(0, HERE)
from figures.util.Util import *
import figNames as TN 


class Trait:
    def __init__(self, ti, tData):
        self.id, self.ti = ti, ti 
        self.qc, self.vals, self.pts, self.lists = {}, {} ,{} , {} 
        if ti == 0 and len(tData) == 0: self.name, self.group = None, None  
        else: 
            self.name = TN.TailName(ti, tData[0], tData[1]) 
            self.find_group(tData[1]) 
        
    def find_group(self, group): 
        self.group = group 
        if self.group == 'Questionnaire/Cognitive': self.group_color = 'xkcd:olive yellow' 
        elif self.group == 'Biomarkers':            self.group_color =  'xkcd:rose red'
        elif self.group == 'Physical_Measures':     self.group, self.group_color = 'Physical Measures', 'xkcd:sea blue'
        else:                                       self.group, self.group_color = 'Unknown', 'magenta'  






class TraitList(list):
    def __init__(self, name, iterable=None):
        super().__init__(iterable or [])
        self.name = name

    def add_dict(self, K):
        self.append(ListItem(K)) 


class ListItem:
    def __init__(self, K): 
        for k,v in K.items(): vars(self)[k] = v 
        self.key = K 

    def __str__(self):
        return str(len(self.key))+" elements: "+','.join([x for x in self.key.keys()])

    def __repr__(self):
        return str(len(self.key))+" elements: "+','.join([x for x in self.key.keys()])







class TraitPts: 
    def __init__(self, n1):
        self.name = n1 

    def add_pt_dict(self, tDict): 
        for k,v in tDict.items(): vars(self)[k] = v 

    def add_pt_data(self, tData, opts=[]): 
        if len(opts) == 0: self.Y = tData 
        else: 
            if len(opts) == 1: vars(self)[opts[0]] = tData 
            else: 
                print('wtf') 
                sys.exit() 




class TraitVals: 
    def __init__(self, n1):
        self.name = n1 
    
    def add_val_dict(self, tDict, opts=[]):  
        self.key = {} 
        for k,v in tDict.items(): 
            self.key[k] = v 
            vars(self)[k] = v 
            
        for x,y in zip(['p1','p2'],['f1','f2']): 
            if x in self.key: 
                self.key[y] = 'NA'  
                vars(self)[y] = 'NA'  


    def __str__(self):
        return str(len(self.key))+" keys: "+','.join([x for x in self.key.keys()])

    def __repr__(self):
        return str(len(self.key))+" keys: "+','.join([x for x in self.key.keys()])









class Traits: 
    def __init__(self, qc_traits, args): 
        self.args = args 
        self.members = {}
        for line in qc_traits: 
            line = line.split() 
            ti, tx, tNames, tData = int(line[0]), line[1], line[2].split(','), [] 
            for x in line[3].split(','): 
                try: tData.append(float(x)) 
                except: tData.append(x) 
            
            if ti not in self.members and line[1] == 'info': self.members[ti] = Trait(ti,tData) 
            else: 
                m = self.members[ti] 
                K = {h:x for h,x in zip(tNames, tData)} 
                if tx not in m.qc: m.qc[tx] = TraitVals(tx) 
                m.qc[tx].add_val_dict(K) 
        
    
    def load(self, value_files, pt_files): 
        self.add_values(value_files) 
        self.add_pts(pt_files) 
        self.summarize() 
        return self 



    def add_values(self, value_files): 
        for f in value_files: 
            fn = f.name.split('/')[-1].split('.')[0]  
            n1,n2 = fn.split('-')[0], fn.split('-')[-1]   
            header = f.readline().split()[1::] 
            for line in f: 
                line = line.split() 
                ti, td = int(line[0]), [] 
                if ti not in self.members: continue 
                for x in line[1::]: 
                    try: td.append(float(x)) 
                    except: td.append(x) 
                m = self.members[ti] 
                K = {h:x for h,x in zip(header, td)} 
                
                if n2 == 'list': 
                    if n1 not in m.lists: m.lists[n1] = TraitList(n1) 
                    m.lists[n1].add_dict(K)  
                      
                else: 
                    if 'src' in K: src = K.pop('src') 
                    elif n1 != n2: src = n2 
                    else:          src = 'NA' 
                    if src == 'NA': 
                        if n1 not in m.vals: m.vals[n1] = TraitVals(n1) 
                        m.vals[n1].add_val_dict(K) 
                    else: 
                        if n1 not in m.vals: m.vals[n1] = {} 
                        if src not in m.vals[n1]: m.vals[n1][src] = TraitVals(src) 
                        m.vals[n1][src].add_val_dict(K) 
                
    def add_pts(self, pt_files): 
        for f in pt_files: 
            fn = f.name.split('/')[-1].split('.')[0]  
            n1, n2 = fn.split('-')[0], fn.split('-')[-1] 
            if n2 == 'vert': 
                header = f.readline().split() 
                K = dd(lambda: dd(list)) 
                for line in f: 
                    line = line.split() 
                    ti = int(line[0]) 
                    if ti not in self.members: continue 
                    for h,v in zip(header[1::], line[1::]): 
                        try: v = float(v) 
                        except: v = v 
                        K[ti][h].append(v) 
                for ti in K.keys(): 
                    m = self.members[ti] 
                    m.pts[n1] = TraitPts(n1)  
                    m.pts[n1].add_pt_dict(K[ti]) 
            else:
                if n1 != n2: opts = [n2] 
                else:        opts = [] 
                for line in f:
                    line = line.split()
                    line_opts = [line[1+i] for i in range(0,len(line)-2)] 
                    ti, Tpts = int(line[0]), [float(x) for x in line[-1].split(',')] 
                    if ti not in self.members: continue 
                    m = self.members[ti] 
                    my_opts = opts + [line[1+i] for i in range(0,len(line)-2)] 
                    

                    if len(my_opts) < 2:   
                        if n1 not in m.pts: m.pts[n1] = TraitPts(n1) 
                        m.pts[n1].add_pt_data(Tpts, my_opts)  
                    
                    elif len(my_opts) <= 3: 
                        if n1 not in m.pts: m.pts[n1] = {} 
                        #optA, optB = my_opts[0:-1], my_opts[-1::]  
                        if len(line_opts) < 3:  
                            optA, optB = my_opts[-2], my_opts[-1] 
                            if optA not in m.pts[n1]: m.pts[n1][optA] = TraitPts(optA) 
                            m.pts[n1][optA].add_pt_data(Tpts, [optB]) 

                        elif len(line_opts) == 3: 
                            
                            optA, optB, optC = my_opts[-3], my_opts[-2], my_opts[-1] 
                            if optA not in m.pts[n1]: m.pts[n1][optA] = {} 

                            if optB not in m.pts[n1][optA]: m.pts[n1][optA][optB] = TraitPts(optB) 

                            m.pts[n1][optA][optB].add_pt_data(Tpts, [optC]) 
                        else: 
                            print('unsupported filetype') 
                            sys.exit() 
                    else: 
                        print('unsupported filetype') 
                        sys.exit() 





    def summarize(self): 
        self.process_fdrs()
        self.process_sibs()
        valid_traits = [T for T in self.members.values() if T.ti != 0] 
        K = sorted({T.group: T.group_color for T in valid_traits}.items()) 
        self.group_names, self.group_colors = [k[0] for k in K], [k[1] for k in K] 
        for T in valid_traits: 
            model, beta0, beta1, beta2 = T.vals['lrs'].model, T.vals['lrs'].beta0, T.vals['lrs'].beta1, T.vals['lrs'].beta2 
            if T.vals['lrs'].model == 'Y~yInt': 
                evo, params = 'none', [beta0, 0, 0] 
            elif T.vals['lrs'].model == 'Y~yInt+X2': 
                params = [beta0, 0, beta1] 
                if beta1 < 0: evo = 'stabilising' 
                else:         evo = 'diverging' 
            else: 
                params = [0 if bb == 'NA' else bb for bb in [beta0, beta1, beta2]] 
                if beta1 > 0: evo = 'pos' 
                else:         evo = 'neg' 
                if beta2 != 'NA': 
                    if beta2 < 0: evo += '-stabilising' 
                    else:         evo += '-diverging' 
            T.vals['lrs'].evo, T.vals['lrs'].key['evo'] =  evo, evo 
            T.vals['lrs'].params, T.vals['lrs'].key['params'] = params, params 
        return  



    def get_meta_p(self, p_denovo, p_mend):
        eps = 1e-300
        p_mend = max(min(p_mend, 1.0), eps)
        p_denovo = max(min(p_denovo, 1.0), eps)
        stat = -2.0 * (math.log(p_mend) + math.log(p_denovo))  # ~ chi2(df=4) under null
        meta_p = stats.chi2.sf(stat, df=4)  # survival function = 1 - CDF, numerically stable
        return meta_p



    def process_sibs(self): 
        for ti,T in self.members.items(): 
            
            if 'sib' in T.vals: 

                d1,d2 = [T.vals['sib'].key[k] for k in ['novo1','novo2']]
                m1,m2 = [T.vals['sib'].key[k] for k in ['mend1','mend2']]
                meta1, meta2 = self.get_meta_p(d1,m1), self.get_meta_p(d2,m2)
                T.vals['sib'].meta1, T.vals['sib'].meta2 = meta1, meta2 
                T.vals['sib'].key['meta1'] = meta1 
                T.vals['sib'].key['meta2'] = meta2 
        return 




    def process_fdrs(self): 
        FDR = dd(list) 
        for k in ['common-snp','common@0.1','combo','combo@0.1','rare','poc','rep','aou']: 
            FDR = [] 
            for ti,T in self.members.items(): 
                if 'pop' in T.vals and k in T.vals['pop'] and T.vals['pop'][k].QC != 'FAIL': 
                    
                    pop = T.vals['pop'][k]
                    p1, p2 = pop.key['p1'], pop.key['p2'] 
                    if type(p1) == float and type(p2) == float: 
                        FDR.extend([[p1,1,ti],[p2,2,ti]]) 
            pvals, locs, tis = [v[0] for v in FDR], [v[1] for v in FDR], [v[2] for v in FDR]  
            reject, p_adj, _, _ = statsmodels.stats.multitest.multipletests(pvals, method='fdr_bh') 
            for rB,pA,loc,ti in zip(reject, p_adj, locs, tis): 
                if loc == 1: 
                    self.members[ti].vals['pop'][k].f1 = rB  
                    self.members[ti].vals['pop'][k].key['f1'] = rB
                else: 
                    self.members[ti].vals['pop'][k].f2 = rB 
                    self.members[ti].vals['pop'][k].key['f2'] = rB


                


