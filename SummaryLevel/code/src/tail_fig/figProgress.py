import sys 
from figures.util.Util import * 

##################################  PROGRESS STREAM  ########################################
class Progress:
    def __init__(self, args, command_line, MODE='Generate Figures'): 
        self.args, self.out_file = args, args.out+'runLog.txt' 
        self.out1, self.out2, self.out3 = open(self.out_file, 'w'), sys.stderr, None 
        if args.silent: self.ACTIVE = False 
        else:           self.ACTIVE = True 
        self.space, self.spl, self.loc, self.INIT, self.panel, self.SAVESRC = '', '  ', None, True, 'fig', False 
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

    def save2(self, msg, ws = 0): 
        if self.INIT: self.show('\n'+self.spl+'  Complete '+msg+'\n')  
        else:         self.show('....Complete '+msg+'\n')  
        self.INIT = False 

    def error(self, msg = 'FAIL', ws=0):
        self.show('\n\n'+self.spl+'FigureError: '+msg+'\n')
        sys.exit()
    
    def warn(self, msg = 'FAIL', ws=0):  self.show('\n\n'+self.spl+'FigureWarning: '+msg+'\n')
    
    def finish(self, NEW=False): self.show('\n\n'+self.spl+'Pipeline Finished\n\n') 

    def update(self, fig): 
        self.fig, self.options = fig, fig.options   
        self.fig_prefix = self.options.out+fig.figName
        self.pdfPath = self.fig_prefix+'.pdf' 
        if self.options.saveSrc: 
            self.src_prefix = self.options.srcPath+fig.figName+'-src' 
            self.src_file   = self.src_prefix+'.csv' 
            self.SAVESRC = True 
        else:                    
            self.src_prefix = None 
        return self 

    def save(self): 
        if self.INIT: self.show('\n'+self.spl+'  Complete (Figure Saved: '+self.pdfPath+')\n')  
        else:         self.show('....Complete (Figure Saved: '+self.pdfPath+')\n')  
        self.INIT = False 
        plt.savefig(self.pdfPath, dpi = self.options.dpi) 
        plt.clf() 
        if self.out3 is not None: self.out3.close() 
        return 
    
    def set_panel(self, x): 

        if self.src_prefix is None: return 
        self.panel, self.src_file = x, self.src_prefix +'-'+x+'.csv' 
        self.out3 = open(self.src_file, 'w') 
        self.panel, self.out3 = x, open(self.src_prefix+'-'+x+'.csv','w') 
        self.SAVESRC = True 
        return 
















