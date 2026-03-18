#!/usr/bin/python3


from collections import defaultdict as dd
import random
import numpy as np  
import sys,os 

# np
HERE = os.path.dirname(os.path.abspath(__file__))                                                                                                                                                        
if HERE not in sys.path: sys.path.insert(0, HERE)
import qcProgress as QP
import qcIO as IO 


#############################################################################################
##################################     TRAIT CLASS      ####################################
#############################################################################################




class Trait:
    def __init__(self, tId, name=None, group=None): 
        self.id, self.name, self.group, self.misc = tId, name, group, TraitStats([],[]) 
        self.fails, self.dupes = {}, []   

    def add_data(self, group_name, header, vals):
        if group_name == 'misc': self.misc.add_to(header, vals) 
        else:                    vars(self)[group_name] = TraitStats(header, vals)  


class TraitStats: 
    def __init__(self, header, vals):
        self.add_to(header, vals) 
    
    def add_to(self, header, vals): 
        for h,v in zip(header, vals): 
            try: 
                v = float(v) 
                if v == int(v): v = int(v) 
            except: pass 
            vars(self)[h] = v  




































        







                



def main(args, parser, command_line):
    if len(args.qcfiles) > 0: 
        progress = QCProgress(args,command_line, MODE='READ_QC_FILES') 
        qc = TraitQC(args, progress) 
        for i,f in enumerate(args.qcfiles): 
            if f.name.split('.')[-1] == 'csv': print('csv') 
            else:                              qc.io.read_qc_txt(f,f.name.split('/')[-1].split('.')[0],i)  
        qc.io.writeInit() 
    elif args.input is not None: 
        progress = QCProgress(args,command_line, MODE='FILTER_TRAITS') 
        qc = TraitQC(args, progress) 
        if args.removeGroups is None and args.applyFilters is None and args.removeDupes is None: qc.io.showVariables() 
        else:
            qc.remove(args.removeGroups)  
            qc.filter(args.applyFilters)  
            qc.dedupe(args.removeDupes) 
            qc.io.writeResult() 
    else: parser.print_help() 
    
    progress.finish()
    sys.exit() 



#if __name__ == '__main__':
#    import argparse, sys
#    usage = "usage: ./%prog [options] data_file"
#    parser = argparse.ArgumentParser()
#    parser.allow_abbrev=True
#    parser.add_argument('qcfiles',type=argparse.FileType('r'),nargs='*') 
#    parser.add_argument('-i','--input',type=argparse.FileType('r')) 
#    parser.add_argument("-o","--out", type=str,default='out',metavar='',help="Output Prefix")
#    parser.add_argument('--applyFilters',type=str) 
#    parser.add_argument('--removeGroups', type=str, nargs="+") 
#    parser.add_argument('--removeDupes',type=argparse.FileType('r')) 
#    parser.add_argument("--dupeCutoff", type=float,default=0.99,metavar='',help="Output Prefix")
#    parser.add_argument("--allowMissing", action='store_true', default=False,help="Save Plot Distribution")  
#    parser.add_argument("--silent", action='store_true', default=False,help="Suppress Output Stream") 
#    args = parser.parse_args() 
#    main(args, parser, ' '.join(sys.argv)) 






