#!/usr/bin/python3
import sys 





#############################################################################################
##################################  PROGRESS STREAM  ########################################
#############################################################################################


class qcProgress:
    def __init__(self, args, command_line, MODE='Generate Results', dots=50): 
        self.args, self.dotlen = args, dots 
        if args.silent: self.ACTIVE = False 
        else:           self.ACTIVE = True 
        self.MAJOR_START = False  
        if args.cmd == 'qc': 
            if args.qc_cmd == 'load':           MODE = 'LOAD_QC_FILES' 
            elif args.qc_cmd == 'filter':       MODE = 'FILTER_TRAITS' 
            else:                               MODE = 'LOAD_AND_FILTER_TRAITS' 
        self.out2  = sys.stderr 
        self.space = '' 
        self.show('\nUKB QC:  '+command_line+'\n')
        self.show('      Mode:  '+MODE+'\n') 
        self.show('      Trait Input:  '+args.infile.name+'\n') 
        if self.args.qc_cmd == 'load':  self.show('      QC Files:  '+",".join([sf.name.split('/')[-1] for sf in args.qcFiles])+'\n') 
        else: 

            if 'useStandardFilters' in args and args.useStandardFilters is True:
                args.applyFilters = "sampleSize-target>50000 h2>0.05 snpmax<0.02 dist-skew<|2| uniq50>2 popQC-pass=True"    
                self.show('      Using Standard Filter Settings: '+args.applyFilters)
            elif args.applyFilters is not None: 
                self.show('      Using Custom Filter Settings: '+args.applyFilters)



        #else: self.show('TraitInput:  '+args.input.name+'\n') 
        self.loc = None
        self.spl = '  ' 
        self.INIT=True



    def show(self, msg, space=''):
        if space == 'NA': myspace = '' 
        else:             myspace = self.space
        if self.ACTIVE: 
            self.out2.write(myspace+msg)
            self.out2.flush() 

    
    def start_step(self, msg, STEP=0): 
        dots = ''.join(['.' for j in range(max(self.dotlen-len(msg),5))]) 
        if self.ACTIVE: 
            if self.INIT: 
                if STEP <= 0: m_out = '\n'+self.spl+msg 
                else:         m_out = self.spl+msg 
                if m_out[-1] != ':': m_out += dots 
                self.show(m_out) 
                self.INIT = False
            else:
                if not self.MAJOR_START: self.complete_step() 
                self.MAJOR_START = False 
                m_out = self.spl+msg 
                if m_out[-1] != ':': m_out += dots 
                self.show(m_out) 



    def start_major_step(self, msg, STEP=0): 
        dots = ''.join(['.' for j in range(max(self.dotlen-len(msg),5))]) 
        self.MAJOR_START = True 
        if self.ACTIVE: 
            if self.INIT: 
                if STEP <= 0: m_out = '\n'+self.spl+msg 
                else:         m_out = self.spl+msg 
                #if m_out[-1] != ':': m_out += dots 
                self.show(m_out+':\n') 
                self.INIT = False
            else:
                self.complete_step() 
                m_out = self.spl+msg 
                self.show(m_out+':\n') 
    
    def end_major_step(self, msg, STEP=0): 
        dots = ''.join(['.' for j in range(max(self.dotlen-len(msg),5))]) 
        self.MAJOR_START = True 
        if self.ACTIVE: 
            m_out = self.spl+msg 
            self.show(m_out+'\n\n') 
    
         












    def complete_step(self, msg=None): 
        if msg is not None: self.show('...Complete ('+msg+')\n') 
        else: self.show('...Complete\n') 
        self.INIT = True 

    def finish(self): 
        self.show('\n'+self.spl+'Finished\n\n') 


    def warn(self, msg): sys.stderr.write('QCWarning- '+msg+'\n')

    def error(self, msg, ws=0):
        wj = ' '.join(['' for x in range(ws)])
        sys.stderr.write('\n\n'+wj+'QCError: '+msg+'\n')
        sys.exit()




