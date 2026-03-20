#!/usr/bin/python3
import sys 
##################################  PROGRESS STREAM  ########################################
class Progress:
    def __init__(self, args, command_line, MODE='Generate Figures'): 
        self.args, self.out_file = args, args.out+'runLog.txt' 
        self.out1, self.out2 = open(self.out_file, 'w'), sys.stderr
        if args.silent: self.ACTIVE = False 
        else:           self.ACTIVE = True 
        self.space, self.spl, self.loc, self.INIT = '', '  ', None, True 
        self.show('\nUKB GEN:  '+command_line+'\n')
        self.show('      Mode:  '+MODE+'\n') 

    def show(self, msg, space=''):
        if space == 'NA': myspace = '' 
        else:             myspace = self.space
        self.out1.write(myspace+msg) 
        if self.ACTIVE: 
            self.out2.write(myspace+msg)
            self.out2.flush() 
    
    def start_step(self, msg, STEP=1): 
        if self.ACTIVE: 
            if self.INIT: 
                if STEP<0: self.show('\n'+self.spl+msg)  
                elif STEP==0: self.show('\n'+self.spl+msg+'...')  
                else: self.show(self.spl+msg+'...')  
                self.INIT = False
            else:
                if STEP<0: self.show(self.spl+msg)  
                else: self.show(self.spl+msg+'...')  

    def report_result(self, msg=None): 
        self.show('\n'+self.spl+'   Reporting Result: '+msg) 
        self.INIT = True 

    def save(self, msg, ws = 0): 
        if self.INIT: self.show('\n'+self.spl+'  Complete '+msg+'\n')  
        else:         self.show('....Complete '+msg+'\n')  
        self.INIT = False 

    def error(self, msg = 'FAIL', ws=0):
        self.show('\n\n'+self.spl+'FigureError: '+msg+'\n')
        sys.exit()
    
    def warn(self, msg = 'FAIL', ws=0):  self.show('\n\n'+self.spl+'FigureWarning: '+msg+'\n')
    
    def finish(self, NEW=False): self.show('\n\n'+self.spl+'Pipeline Finished\n\n') 
