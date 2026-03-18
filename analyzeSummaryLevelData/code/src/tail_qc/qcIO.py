#!/usr/bin/python3


from collections import defaultdict as dd
import numpy as np  
import argparse, sys,os 

HERE = os.path.dirname(os.path.abspath(__file__))                                                                                                                                                        
if HERE not in sys.path: sys.path.insert(0, HERE)
import qcProgress as QP
import qcTraits as QT 


class qcIO: 
    def __init__(self, qc): 
        self.args, self.progress, self.qc = qc.args, qc.progress, qc 
        self.passFile, self.failFile = self.get_uniq_filenames() 
        self.qc_names = [] 

    def get_uniq_filenames(self): 
        
        if self.args.qc_cmd == 'filter': failFile, passFile = self.args.out+'.fail.txt', self.args.out+'.pass.txt'
        else:                            failFile, passFile = self.args.out+'.missing.txt', self.args.out+'.merged.txt'
        #if self.args.infile.name in [failFile, passFile]: self.progress.error('Input/Output names must be unique')  
        return passFile, failFile 


    def update_filenames(self): 
        self.args.infile = argparse.FileType("r")(self.passFile)
        self.passFile, self.failFail = self.args.out+'.pass.txt', self.args.out+'.fail.txt'
        return
    

    ### READING FUNCTIONS ### 

    def read_in(self, f): 
        traits = {} 
        self.progress.start_step('Reading Input-File('+f.name.split('/')[-1]+')',STEP=0) 
        for line in f: 
            line = line.split()
            if line[0] not in traits: traits[line[0]] = QT.Trait(line[0]) 
            T = traits[line[0]] 
            K = {x: y for x,y in zip(line[2].split(','), line[3].split(','))} 
            if line[1] in ['info']: 
                for k,v in K.items(): 
                    try: vars(T)[k] = float(v) 
                    except: vars(T)[k] = v 
            else: T.add_data(line[1], [k for k in K.keys()], [v for v in K.values()]) 
        self.progress.complete_step(str(len(traits))+' Read In') 
        return traits 



    # READ QC FILES # 


    def read_qc(self, f, step): 
        ess1, ess2 = 'Invalid File Format: ', ' ('+f.name.split('/')[-1]+')' 
        self.progress.start_step('Reading QC-File('+f.name.split('/')[-1]+')',STEP=step) 
        file_prefix, ext  = f.name.split('/')[-1].split('.')[0], f.name.split('.')[-1].lower() 
        if ext == 'csv':   sep, CSV = ',', True 
        elif ext == 'txt': sep, CSV = ' ', False 
        else:              self.progress.error('Invalid File Extension: txt or csv required'+ess2) 
        line1 = f.readline().strip().split(sep) 
        while line1[0][0] == '#': line1 = f.readline().strip().split(sep) 
        len1, line = len(line1), f.readline().strip().split(sep) 
        added = 0 
        try: 
            # NO HEADER # 
            t1 = int(line1[0]) 
            if len1 != len(line): self.progress.error(ess1+'Unequal Number of Columns'+ess2) 
            if len1 == 2: my_prefix, my_header = 'misc', [file_prefix] 
            else:         my_prefix, my_header = 'misc', [file_prefix + 'j' for j in range(1,len1)] 
            if line1[0] in self.qc.traits: 
                added += 1 
                self.qc.traits[line1[0]].add_data(my_prefix, my_header, line1[1::]) 
        except ValueError: 
            # HEADER EXISTS # 
            if len(line)<2 or len1>len(line) or len1<len(line)-1: self.progress.error(ess1+'At Least Two Columns (TraitID,Value) Required'+ess2) 
            if len(line) == len1:                             my_prefix, my_header = file_prefix, line1[1::] 
            elif file_prefix == line1[0] and len(line1) == 1: my_prefix, my_header = 'misc', line1 
            else:                                             my_prefix, my_header = file_prefix, line1  
        while len(line) > 1: 
            if line[0] in self.qc.traits: 
                added += 1 
                self.qc.traits[line[0]].add_data(my_prefix, my_header, line[1::]) 
            line = f.readline().strip().split(sep) 
        self.progress.complete_step(str(added)+' Traits Added')  
        return 

    def read_dupes(self, f):
        for line in f: 
            line = line.split()
            if len(line) < 2: continue
            t1,t2 = line[0],line[1]
            try:    T1, T2, val  = self.qc.traits[line[0]], self.qc.traits[line[1]], float(line[-1]) 
            except: continue
            if val < self.args.dupeCutoff: continue  
            if len(T1.fails)+len(T2.fails) > 0: continue
            T1.dupes.append(t2)
            T2.dupes.append(t1)
        return {ti: T for ti,T in self.qc.traits.items() if len(T.dupes) > 0}  





    def read_custom_specification(self, f):
        custom_key = dd(lambda: dd(list)) 
        for line in f:
            if line[0] == '#': continue 
            line = line.split('#')[0].split()  
            if len(line) < 2: continue 
            r1, r2 = line[0].upper(), line[1].upper()  
            traits = [ti for ti in line[-1].split(',') if ti in self.qc.traits]
            if len(traits) == 0 or r1 not in ['REMOVE','KEEP']: continue 
            if r1 == 'KEEP': 
                if r2 == 'PRE': self.progress.error('CustomConfigFileError: "keep" & "pre" are incompatible (all traits are kept initially)')  
                else:           custom_key['POST']['KEEP'].extend(traits) 
            else: 
                if r2 != 'PRE':  custom_key['POST'][r1].extend(traits) 
                if r2 != 'POST': custom_key['PRE'][r1].extend(traits) 
        return custom_key 
        

        
    def showVariables(self):
        self.progress.start_step('Displaying Variables:', STEP=-1) 
        traits = [t for t in self.qc.traits.values()]
        T1 = traits[0] 
        w = sys.stderr
        w.write('\n') 
        w.write('%-20s %25s %25s %25s %50s\n' % ('  category', 'name', 'type','avg/mode','example'))  
        
        valid_opts = ['id','group','misc'] + [v for v in vars(T1) if v not in ['misc','id','name','group','fails','name','dupes']] 

        #for v in vars(T1): 
        for v in valid_opts: 
            
            if v in ['fails','name','dupes']: continue #,'name','category','subcategory','fails']: continue
            elif v in ['id','name','group']: 
                t_val = vars(T1)[v] 
                w.write('%-20s %25s %25s %25s %50s\n' % ('  None', v, 'attribute','NA',v+'!='+t_val)) 
            else: 
                V = vars(vars(T1)[v]) 
                opts = [k for k in V.keys()] 
                for opt in opts: 
                    X = [vars(vars(t)[v])[opt] for t in traits]
                    missing = len([x for x in X if x == 'NA']) 
                    if v == 'misc': eStart = opt
                    else:           eStart = v+'-'+opt 
                    try: 
                        Y = sorted([float(x) for x in X if x != 'NA']) 
                        yAvg = round(sum(Y)/len(Y),5) 
                        yLo = str(round((Y[0] + yAvg)/2.0,3))
                        yHi = str(round((Y[-1] + yAvg)/2.0,3))
                        my_ex = eStart +'>' + yLo 
                        w.write('%-20s %25s %25s %25s %50s\n' % ('  '+v, opt, 'numerical',str(yAvg),my_ex)) 
                    except: 
                        Xk = sorted(list(set(X)))  
                        if len(Xk) == 2 and Xk[0] == 'False' and Xk[1] == 'True': 
                            w.write('%-20s %25s %25s %25s %50s\n' % ('  '+v, opt, 'boolean','True/False',eStart+'=True')) 
                        else: 
                            Xstr = '/'.join(Xk[0:3]) 
                            if len(Xk) > 3: Xstr += '...' 
                            w.write('%-20s %25s %25s %25s %50s\n' % ('  '+v, opt, 'categorical',Xstr,eStart+'='+Xk[0])) 











    def writeInit(self): 
        passTraits, missTraits = [], []  
        for ti,T in self.qc.traits.items(): 
            tv = [v for v in vars(T)] 
            if self.args.allowMissing or all(x in tv for x in self.qc_names): passTraits.append(T) 
            else:                           missTraits.append([ti, ','.join([x.split('_misc_')[-1] for x in self.qc_names if x not in tv])]) 
        if len(missTraits) > 0: self.writeMissing(missTraits) 
        if len(passTraits) > 0: self.writePassed(passTraits) 
    
    def writeResult(self): 
        passTraits = [T for T in self.qc.traits.values() if len(T.fails) == 0] 
        failTraits = [T for T in self.qc.traits.values() if len(T.fails) > 0] 
        if len(failTraits) > 0: self.writeFailed(failTraits) 
        if len(passTraits) > 0: self.writePassed(passTraits) 
                
            







    def writeMissing(self, failTraits): 
        w = open(self.failFile, 'w') 
        w.write('%-15s %40s %40s\n' % ('---', 'filter','value')) 
        for ti,tf in sorted(failTraits): w.write('%-15s %40s %40s\n' % (ti, 'REQUIRED:'+tf, 'MISSING')) 
        w.close() 
        return 

    def writeFailed(self, failTraits): 
        w= open(self.failFile, 'w') 
        w.write('%-10s %30s %40s %40s %40s\n' % ('---', 'name','filter;value','filter;value','filter;value')) 
        for T in failTraits: 
            if len(T.name) < 31: w.write('%-10s %30s ' % (T.id, T.name[0:30])) 
            else:                w.write('%-10s %30s ' % (T.id, T.name[0:27]+'...')) 
            for k,v in T.fails.items():
                if type(v[1]) == float and v[1] == int(v[1]): vstr = k.split('.misc-')[-1].strip()+v[0].strip()+';'+str(int(v[1]))
                else:                                         vstr = k.split('.misc-')[-1].strip()+v[0].strip()+';'+str(v[1])
                w.write('%40s ' % vstr) 
            w.write('\n') 
        w.close() 
        return  

    def writePassed(self, passTraits): 
        self.progress.start_step('Printing Valid Traits', STEP=1) 
        w = open(self.passFile, 'w') 
        for T in passTraits:     
            KP = dd(list) 
            w.write('%-10s %25s %50s %75s\n' % (T.id, 'info', 'name,group', T.name+','+T.group))  
            for v in vars(T):
                if v[0:6] == '_misc_': KP['misc'].append([v[6::], vars(vars(T)[v])[v[6::]]])  
                elif v not in ['id','name','group','fails','dupes']:   KP[v] = [item for item in vars(vars(T)[v]).items()]
                else: continue 
            misc_opts = KP.pop('misc') 
            w.write('%-10s %25s %50s %75s\n' % (T.id, 'misc',",".join([mo[0] for mo in misc_opts]), ",".join([str(mo[1]) for mo in misc_opts])))  
            for v,v_opts in KP.items(): w.write('%-10s %25s %50s %75s\n' % (T.id, v,",".join([mo[0] for mo in v_opts]), ",".join([str(mo[1]) for mo in v_opts])))  
        w.close() 
        self.progress.complete_step(str(len(passTraits))+' Traits Remain') 










    



