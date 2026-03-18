#!/usr/bin/python3

import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path: sys.path.insert(0, HERE)

from util.Util   import * 
from util import drawScatter as SP 
from util import drawTables as DT
from util import drawVarious as DV 




# try



LK = {} 
LK["trait"]= "UKB Trait ID"
LK["full-name"] = "UKB Trait Name" 
LK["short-name"] = "Shortened Version of UKB Trait Name used for Figures" 
LK["aou-name"] = "Name of Corresponding Trait in All Of Us (When Available)" 
LK["targetSize"] = "Number of samples in the primary UKB Target Set" 
LK["sibSize"] = "Number of Sibling Pairs in the primary UKB data" 
LK["h2"] = "SNP-Based Heritability Estimate"
LK["r2"] = "R-squared PRS Estimate" 
LK["sib-h2"] = "Sibling Based Total Heritability Estimate" 
LK["selection-estimate"] = "Estimate of Selection Direction" 
LK["annos"]= "ClinVar Annotation (When Available)"
LK["beta"]= "SNP-Effect-Size"
LK["DRAGEN-ID"]= "DRAGEN-SNP-Identifier"
LK["gene"]= "Gene Annotation (When Available)"
LK["lower-0.1%-pop-effect"]= "Lower Tail (0.1%) Common Variant PRS POPout effect size"
LK["lower-0.1%-pop-fdr"]= "Lower Tail (0.1%) Common Variant PRS POPout pvalue 5%-FDR Test"
LK["lower-0.1%-recSig"]= "Lower Tail (0.1%) Common+Rare Variant PRS POPout % reduction pvalue (>0)"
LK["lower-0.1%-reduction"]= "Lower Tail (0.1%) Common+Rare Variant PRS POPout % reduction to POPOut effect"
LK["lower-1%-pop-effect"]= "Lower Tail (1%) Common Variant PRS POPout effect size"
LK["lower-1%-pop-fdr"]= "Lower Tail (1%) Common Variant PRS POPout pvalue 5%-FDR Test"
LK["lower-1%-reduction"]= "Lower Tail (1%) Common+Rare Variant PRS POPout % reduction to POPOut effect"
#LK["lower-OR"]= "Lower Tail (1%) Odds Ratio: Odds of 1% Trait Value, Given 1% Common PRS Value"
#LK["lower-OR-CI"]= "Lower Tail (1%) 95% Confidence Interval for Common PRS Odds Ratio"
LK["lower-OR-CI-combinedPRS"]= "Lower Tail (1%) 95% Confidence Interval for Common+Rare PRS Odds Ratio"
LK["lower-OR-CI-commonPRS"]= "Lower Tail (1%) 95% Confidence Interval for Common PRS Odds Ratio"
LK["lower-OR-combinedPRS"]= "Lower Tail (1%) Odds Ratio: Odds of 1% Trait Value, Given 1% Common+Rare PRS Value"
LK["lower-OR-commonPRS"]= "Lower Tail (1%) Odds Ratio: Odds of 1% Trait Value, Given 1% Common PRS Value"
LK["lower-pop-CI"]= "Lower Tail (1%) Common Variant PRS POPout effect 95% Confidence Interval"
LK["lower-pop-effect"]= "Lower Tail (1%) Common Variant PRS POPout effect size"
LK["lower-pop-fdr"]= "Lower Tail (1%) Common Variant PRS POPout pvalue 5%-FDR Test"
LK["lower-pop-pv"]= "Lower Tail (1%) Common Variant PRS POPout pvalue"
LK["lower-pop-QC"]= "Lower Tail (1%) Common Variant PRS POPout QC"
LK["lower-recSig"]= "Lower Tail (1%) Common+Rare Variant PRS POPout % reduction pvalue (>0)"
LK["lower-standout-pv"]= "Lower Tail (1%) Sibling Standout Pvalue"
LK["maf"]= "Minor Allele Fraction Bin"
LK["pv"]= "SNP-pvalue (from gwas on normalized trait)"
LK["RS-ID"]= "RS-Identifier (When Available)"
LK["type"]= "Functional SNP Description (When Availble)"
LK["upper-0.1%-pop-effect"]= "Upper Tail (0.1%) Common Variant PRS POPout effect size"
LK["upper-0.1%-pop-fdr"]= "Upper Tail (0.1%) Common Variant PRS POPout pvalue 5%-FDR Test"
LK["upper-0.1%-recSig"]= "Upper Tail (0.1%) Common+Rare Variant PRS POPout % reduction pvalue (>0)"
LK["upper-0.1%-reduction"]= "Upper Tail (0.1%) Common+Rare Variant PRS POPout % reduction to POPOut effect"
LK["upper-1%-pop-effect"]= "Upper Tail (1%) Common Variant PRS POPout effect size"
LK["upper-1%-pop-fdr"]= "Upper Tail (1%) Common Variant PRS POPout pvalue 5%-FDR Test"
LK["upper-1%-reduction"]= "Upper Tail (1%) Common+Rare Variant PRS POPout % reduction to POPOut effect"
#LK["upper-OR"]= "Upper Tail (1%) Odds Ratio: Odds of 1% Trait Value, Given 1% Common PRS Value"
#LK["upper-OR-CI"]= "Upper Tail (1%) 95% Confidence Interval for Common PRS Odds Ratio"
LK["upper-OR-CI-combinedPRS"]= "Upper Tail (1%) 95% Confidence Interval for Common+Rare PRS Odds Ratio"
LK["upper-OR-CI-commonPRS"]= "Upper Tail (1%) 95% Confidence Interval for Common PRS Odds Ratio"
LK["upper-OR-combinedPRS"]= "Upper Tail (1%) Odds Ratio: Odds of 1% Trait Value, Given 1% Common+Rare PRS Value"
LK["upper-OR-commonPRS"]= "Upper Tail (1%) Odds Ratio: Odds of 1% Trait Value, Given 1% Common PRS Value"
LK["upper-pop-CI"]= "Upper Tail (1%) Common Variant PRS POPout effect 95% Confidence Interval"
LK["upper-pop-effect"]= "Upper Tail (1%) Common Variant PRS POPout effect size"
LK["upper-pop-fdr"]= "Upper Tail (1%) Common Variant PRS POPout pvalue 5%-FDR Test"
LK["upper-pop-pv"]= "Upper Tail (1%) Common Variant PRS POPout pvalue"
LK["upper-pop-QC"]= "Upper Tail (1%) Common Variant PRS POPout QC"
LK["upper-recSig"]= "Upper Tail (1%) Common+Rare Variant PRS POPout % reduction pvalue (>0)"
LK["upper-standout-pv"]= "Upper Tail (1%) Sibling Standout Pvalue"


#print(LK.keys()) 










class CsvOut:
    def __init__(self, traits, fname): 
        self.traits, self.w = traits, open(fname, 'w') 
    

    def write_full_glossary(self): 

        for k,v in LK.items(): 
            self.w.write(k+',\"'+v+'\"\n') 


    def write_rares(self): 
        header = ['loc', 'pv', 'beta', 'rs', 'type', 'maf', 'gene', 'annos'] 
        names = ['trait', 'DRAGEN-ID', 'pv', 'beta', 'RS-ID', 'type', 'maf', 'gene', 'annos'] 
        self.w.write('%s\n' % ",".join(names)) 
        for ti,T in self.traits.items(): 
            if 'snp' in T.lists: 
                for snp in T.lists['snp']: 
                    snp_data = [ti] + [snp.key[k] for k in header] 
                    snp_data = ",".join([str(s) for s in snp_data]) 
                    self.w.write(snp_data+'\n') 


    def write_summaries(self): 


        header = ['trait'] + ['full-name','short-name','aou-name']
        header += ['targetSize','sibSize','h2','r2','sib-h2','selection-estimate'] 
        self.w.write(','.join(header)+'\n') 
        for ti,T in self.traits.items(): 
            X = {} 
            X['trait'] = ti 
            X['aou-name']  = T.name.aou 
            X['full-name'] = T.name.flat  
            X['short-name'] = T.name.mini  
            X['h2'], X['r2'] = [T.qc['misc'].key[k] for k in ['h2','r2']] 
            X['targetSize'], X['sibSize'] = [T.qc['sampleSize'].key[k] for k in ['target','sibs']] 
            X['selection-estimate'] =  T.vals['lrs'].evo  
            X['sib-h2'] = T.vals['sib'].h2 
            t_data = ",".join([str(X[h]) for h in header]) 
            self.w.write(t_data+'\n') 
        return




    def write_common_tests(self): 
        pop_keys = [['p1','e1','j1','f1','QC'],['p2','e2','j2','f2','QC']]
        sib_keys = [['meta1'],['meta2']]
        #odd_keys = [['odds-1','ci-1'],['odds-99','ci-99']]
        pop_names = ['pop-pv','pop-effect','pop-CI','pop-fdr','pop-QC'] 
        sib_names = ['standout-pv'] 
        #odd_names = ['OR','OR-CI'] 
        all_names = pop_names + sib_names 
        header = ['trait'] + ['lower-'+n for n in all_names]+['upper-'+n for n in all_names] 
        self.w.write(','.join(header)+'\n') 
        for ti, T in self.traits.items(): 
            td = [str(ti)] 
            for i in range(2): 
                pd = [T.vals['pop']['common-snp'].key[k] for k in pop_keys[i]] 
                pd[2] = str(round(pd[1]-pd[2],3))+';'+str(round(pd[1]+pd[2],3))
                pd = [str(p) for p in pd] 
                try: sd = [str(T.vals['sib'].key[k]) for k in sib_keys[i]] 
                except: sd = ['NA' for k in sib_keys[i]] 
                td.extend(pd+sd) 
            self.w.write(','.join(td)+'\n')  
        return 

    def write_rare_tails(self): 
        pop_names = ['1%-pop-effect','1%-pop-fdr'] 
        rec_names = ['1%-reduction','recSig'] 
        odd_names = ['OR-commonPRS','OR-CI-commonPRS'] 
        odd_names2 = ['OR-combinedPRS','OR-CI-combinedPRS'] 
        pop_names2 = ['0.1%-pop-effect','0.1%-pop-fdr'] 
        rec_names2 = ['0.1%-reduction','0.1%-recSig'] 
        pop_keys = [['e1','f1'],['e2','f2']]
        rec_keys = [['total1','sig1'],['total2','sig2']]
        odd_keys = [['odds-1','ci-1'],['odds-99','ci-99']]
        all_names = pop_names + rec_names + odd_names + odd_names2 + pop_names2 + rec_names2 
        header = ['trait'] + ['lower-'+n for n in all_names]+['upper-'+n for n in all_names] 
        self.w.write(','.join(header)+'\n') 
        for ti, T in self.traits.items(): 
            if 'recovery' not in T.vals: continue  
            td = [str(ti)] 
            for i in range(2): 
                xp= [str(T.vals['pop']['common-snp'].key[k]) for k in pop_keys[i]] 
                rp = [str(T.vals['recovery']['combo'].key[k]) for k in rec_keys[i]] 
                xo = [T.vals['odds']['common'].key[k] for k in odd_keys[i]] 
                xo[1] = str(round(xo[0]-xo[1],3))+';'+str(round(xo[0]+xo[1],3))
                xo = [str(x) for x in xo] 
                ro = [T.vals['odds']['combo'].key[k] for k in odd_keys[i]] 
                ro[1] = str(round(ro[0]-ro[1],3))+';'+str(round(ro[0]+ro[1],3))
                ro = [str(x) for x in xo] 
                XP = [str(T.vals['pop']['common@0.1'].key[k]) for k in pop_keys[i]]  
                RP = [str(T.vals['recovery']['combo@0.1'].key[k]) for k in rec_keys[i]] 
                td.extend(xp+rp+xo+ro+XP+RP) 
            self.w.write(','.join(td)+'\n')  















            

class MyFigure:
    def __init__(self, options, traits, progress, figName='Csv'): 
        self.options, self.traits, self.data, self.progress, self.figName = options, traits.members, traits, progress, figName
        self.C1 = 'xkcd:very light blue' 
        self.C1 = 'xkcd:very light pink' 
        self.C2 = 'xkcd:off white' 
        self.E1, self.E2 = 'darkslategray','gray' 


    
    def draw(self): 
        names = ['table-glossary.csv', 'table-traitSummaries.csv','table-commonTails.csv', 'table-rareTails.csv', 'table-rareSNPs.csv'] 
        paths = [self.options.out + n for n in names] 
        csv_key      = CsvOut(self.traits, paths[0]).write_full_glossary() 
        summaries      = CsvOut(self.traits, paths[1]).write_summaries() 
        common_tails = CsvOut(self.traits, paths[2]).write_common_tests() 
        rare_tails   = CsvOut(self.traits, paths[3]).write_rare_tails() 
        snps         = CsvOut(self.traits, paths[4]).write_rares() 
        
        self.progress.save('(Csv Tables Saved: '+",".join([p for p in paths])+')')
                                                        

        







   



















