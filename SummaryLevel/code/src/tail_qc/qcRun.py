#!/usr/bin/python3


#import random
#import numpy as np  
import sys,os 

# np
HERE = os.path.dirname(os.path.abspath(__file__))                                                                                                                                                        
if HERE not in sys.path: sys.path.insert(0, HERE)
import qcProgress as QP
import qcIO as IO 
import qcDedupe as QD 
from collections import defaultdict as dd



class qcRun:
    def __init__(self, args, command_line): 
        if os.path.isdir(args.out): 
            if not args.out.endswith(os.sep): args.out += os.sep 
            args.out = args.out+'qc'  
        self.args, self.progress = args, QP.qcProgress(args, command_line) 
        self.io = IO.qcIO(self) 
        self.config = dd(lambda: dd(list)) 
        self.traits = self.io.read_in(args.infile) 
        if args.qc_cmd == 'load':     self.go = self.load_qc_files 
        elif args.qc_cmd == 'filter': self.go = self.filter_qc_traits 
        else:                         self.go = self.load_and_filter 

   
    def load_and_filter(self): 
        
        self.load_qc_files()
        self.io.update_filenames() 
        self.progress.start_major_step('Filtering Begins',STEP=1) 
        self.filter_qc_traits()         


    def load_qc_files(self): 
        for i,f in enumerate(self.args.qcFiles): self.io.read_qc(f,i+1)  
        self.io.writeInit() 
        if self.args.showVariables: self.io.showVariables() 
        self.progress.finish()




    def filter_qc_traits(self): 
        if self.args.configFile is None and self.args.dupeFile is None and self.args.applyFilters is None: self.io.showVariables() 
        else:
            if self.args.configFile is not None:       self.configure(self.args.configFile) 
            if self.args.applyFilters is not None: self.filter(self.args.applyFilters)  
            if self.args.dupeFile is not None:  self.dedupe(self.args.dupeFile, self.args.dupeCutoff, self.args.dupeTieBreak) 
            self.post_customize()  
            self.io.writeResult() 
        self.progress.finish() 


    def configure(self, custom):
        self.config = self.io.read_custom_specification(custom)
        self.pre_customize() 

    def pre_customize(self):
        nR,nT = len(self.config['PRE']['REMOVE']), len(self.traits) 
        if nR > 0: 
            self.progress.start_step('PreFiltering Traits...',STEP=1) 
            for ti in self.config['PRE']['REMOVE']: self.traits[ti].fails['PRE'] = ['-CustomRemove', True] 
            self.progress.complete_step(str(nR)+' Traits Removed, '+str(nT-nR)+' Traits Remain') 
        return 


    def post_customize(self): 
        K = self.config['POST'] 
        if len(K) == 0: return 
        

        toRemove = [ti for ti in K['REMOVE'] if len(self.traits[ti].fails) == 0] 
        toKeep   = [ti for ti in K['KEEP'] if len(self.traits[ti].fails) != 0]
        if len(toRemove + toKeep) == 0: return 

        self.progress.start_step('PostFiltering Traits...',STEP=1) 
        for ti in toRemove: self.traits[ti].fails['POST'] = ['-customRemoval',True] 
        for ti in toKeep:   self.traits[ti].fails = {} 
        rL, kL, tL = str(len(toRemove)), str(len(toKeep)), str(len([T for T in self.traits.values() if len(T.fails) == 0])) 
        
        if rL!='0' and kL!='0': self.progress.complete_step(rL+' Traits Removed, '+kL+' Kept, Total of '+tL+' Traits Remain') 
        elif rL != '0':           self.progress.complete_step(rL+' Traits Removed, Total of '+tL+' Traits Remain') 
        elif kL != '0':           self.progress.complete_step(kL+' Traits Kept, Total of '+tL+' Traits Remain') 
        else: return  
        return 


   
   
    


    def customize(self, k): 
        K = self.config[k] 
        if len(K) == 0: return 


        if k == 'PRE': self.progress.start_step('PreFiltering Traits...',STEP=1) 
        else:          self.progress.start_step('PostFiltering Traits...',STEP=1) 

        for ti in K['REMOVE']:  self.traits[ti].fails[k] = ['-CustomRemoval', True] 
        for ti in K['KEEP']:    self.traits[ti].fails = {} 
        kDiff = len(K['REMOVE']) - len(K['KEEP']) 
        rem = str(len([ti for ti in self.traits.keys() if len(self.traits[ti].fails) == 0])) 
        if kDiff > 0: self.progress.complete_step(str(kDiff)+' Traits Removed, '+rem+' Traits Remain') 
        else:         self.progress.complete_step(str(-kDiff)+' Traits Kept, '+rem+' Traits Remain') 
        return 


   
    
    def dedupe(self, dupeFile, MIN_VAL=0.99, TIE_BREAKER='N'): 
        #self.progress.start_step('Deduping Traits...', STEP=1) 
        self.progress.start_step('Identifying Duplicated Traits...', STEP=1) 
        
        dupes = self.io.read_dupes(dupeFile) 
        deduper = QD.DeDupe(dupes, TIE_BREAKER) 
        deduper.separate_pairs_and_groups() 
        ordered_pairs = deduper.order_pairs() 
        
        
        ps = 'Found ' 
        if len(ordered_pairs) > 0: ps+= str(len(ordered_pairs))+' Duplicate Pairs, '
        if len(deduper.groups) > 0: ps += str(len(deduper.groups))+' Networks' 
        if len(ps) < 10: 
            self.progress.complete_step('No Duplicates Found') 
            return 
        else:  self.progress.complete_step(ps) 
        
        #print(deduper.groups)
        #for g in deduper.groups: 
        #    print(len(g)) 

        self.progress.start_step('Deduping Traits...', STEP=1) 
        for t1,t2 in ordered_pairs: self.traits[t2].fails['DupePair'] = [t1, 'fail']  
        dupes = len(ordered_pairs) 
        group_pass, group_fail = deduper.maximize_group_winners() 
        for g_pass, g_fail in zip(group_pass, group_fail): 
            for ti in g_fail: 
                self.traits[ti].fails['DupeGroup'] = [','.join(g_pass), 'fail']  
                dupes += 1 
        tl = str(len([T for T in self.traits.values() if len(T.fails) == 0]))
        self.progress.complete_step(str(dupes)+' Traits Removed, '+tl+' Traits Remain') 
        return




    def filter(self, filter_string): 
        
        self.progress.start_major_step('Filtering Begins') 
        T1 = [T for T in self.traits.values()][0] 
        self.valid = ['id','group'] + [m for m in vars(T1.misc)]    
        for v in [v for v in vars(T1) if v not in self.valid +['misc','name','fails','dupes']]: 
            for v2 in vars(vars(T1)[v]): self.valid.append(v+'-'+v2)
        self.v_str = ','.join(self.valid)  
        for i,x in enumerate(filter_string.split()): 
            f_name, f_rules = self.parse_filter(x)
            self.progress.start_step('Applying Filter: '+x, STEP=i+1) 
            self.apply_filter(f_name,f_rules,i+1) 
        
        tl = str(len([T for T in self.traits.values() if len(T.fails) == 0]))
        self.progress.end_major_step('Filtering Ends: '+tl+' Traits Remain') 
        





    def parse_filter(self, x): 
        if len(x.split('<=')) == 2:   dX = '<=' 
        elif len(x.split('>=')) == 2: dX = '>=' 
        elif len(x.split('!=')) == 2: dX = '!=' 
        elif len(x.split('=')) == 2:  dX = '=' 
        elif len(x.split('>')) == 2:  dX = '>' 
        elif len(x.split('<')) == 2:  dX = '<' 
        else: self.progress.error('Invalid Filter') 
        a,bX = x.split(dX) 
        if a not in self.valid: self.progress.error('Variable '+a+' does not iExist\nDid you Mean: '+self.v_str+'?') 
        
        if len(a.split('-'))==1: a = 'misc-'+a 
        if bX[0] == '|' and bX[-1] == '|': 
            bX = bX.split('|')[1] 
            if bX[0] == '-': nX = bX[1::] 
            else:            nX = '-'+bX 
            f_rules = [[dX, bX]] 
            if dX == '<': f_rules.append(['>',nX]) 
            elif dX == '>': f_rules.append(['<',nX]) 
            elif dX == '!=': f_rules.append(['!=',nX]) 
            elif dX == '<=': f_rules.append(['>=',nX]) 
            elif dX == '>=': f_rules.append(['<=',nX]) 
            else:            self.progress.error('Invalid Filter') 
            return a, f_rules 
        return a, [[dX,bX]] 


    
    def apply_filter(self, f_name, f_rules, FN=0): 
        fail_cnt = 0

        
        

        for dx,b in f_rules: 
            A1,A2 = f_name.split('-') 
            for t,T in self.traits.items(): 
                if A2 in ['name', 'id', 'category', 'subcategory']: 
                    trait_value = vars(T)[A2] 
                    if dx in ['=','!=']: 
                        if dx == '=' and trait_value == b: continue 
                        elif dx == '!=' and trait_value != b: continue 
                        else:                                   
                            T.fails[f_name] = [dx+b, trait_value]
                            fail_cnt += 1 
                    else: 
                        self.progress.error('Incorrect Filter Comparison [label/numeric: '+A2+'/'+dx+']', ws=20) 
                
                else:
                    try: trait_value = vars(vars(T)[A1])[A2]
                    except KeyError:   self.progress.error('Variable '+A1+'-'+A2+' Does not Exist') 
                    if b == 'NA':
                        if dx in ['=','!=']: 
                            if dx == '!=' and trait_value != 'NA': continue 
                            elif dx == '=' and trait_value == 'NA': continue 
                            else: 
                                T.fails[f_name] = [dx+b, trait_value]
                                fail_cnt += 1 
                        else: self.progress.error('Incorrect Filter') 
                    else:
                        try: 
                            bv, trait_value = float(b), float(trait_value) 
                            trait_value = float(vars(vars(T)[A1])[A2]) 
                            if dx == '=' and trait_value  == bv:    continue 
                            if dx == '!=' and trait_value != bv:    continue 
                            elif dx == '>' and trait_value > bv:    continue 
                            elif dx == '>=' and trait_value >= bv:  continue 
                            elif dx == '<' and trait_value < bv:    continue 
                            elif dx == '<=' and trait_value <= bv:  continue 
                            else:                                   
                                T.fails[f_name] = [dx+b, trait_value]
                                fail_cnt += 1 
                        except: 
                            if dx == '=' and trait_value == b:    continue 
                            elif dx == '!=' and trait_value != b: continue 
                            else: 
                                T.fails[f_name] = [dx+b, trait_value]
                                fail_cnt += 1 
        self.progress.complete_step(str(fail_cnt)+' Traits Removed') 




































        







                

