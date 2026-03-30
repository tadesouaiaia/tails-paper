import sys 
from figures.util.Util import * 

##################################  PROGRESS STREAM  ########################################
class Progress:
    def __init__(self, args, command_line, MODE='Generate Figures'): 
        self.args, self.out_file = args, 'runLog.txt' 
        self.out1, self.out2, self.out3 = open(self.out_file, 'w'), sys.stderr, None 
        if args.silent: self.ACTIVE = False 
        else:           self.ACTIVE = True 
        self.space, self.spl, self.loc, self.INIT, self.panel, self.SAVESRC = '', '  ', None, True, 'fig', False 
        self.show('\nUKB GEN:  '+command_line+'\n')
        self.show('      Mode:  '+MODE+'\n') 

    
    def dot(self, dots=1): self.show("".join(['.' for i in range(dots)]))

    def show(self, msg, space=''):
        if space == 'NA': myspace = '' 
        else:             myspace = self.space
        self.out1.write(myspace+msg) 
        if self.ACTIVE: 
            self.out2.write(myspace+msg)
            self.out2.flush() 
    
    def start_step(self, msg, STEP=1): 
        ki,kt = '','' 
        if self.INIT and STEP<=0: ki = '\n' 
        if STEP >= 0: kt = '...' 
        self.show(ki+self.spl+msg+kt)  
        self.INIT = False 
        return

    def report_result(self, msg=None): 
        self.show('\n'+self.spl+'   Reporting Result: '+msg) 
        self.INIT = True 

    def error(self, msg = 'FAIL', ws=0):
        self.show('\n\n'+self.spl+'FigureError: '+msg+'\n')
        sys.exit()
    
    def warn(self, msg = 'FAIL', ws=0):  self.show('\n\n'+self.spl+'FigureWarning: '+msg+'\n')
    
    def finish(self, NEW=False): 
        self.show('\n'+self.spl+'Pipeline Finished\n') 

    def update(self, fig): 
        self.fig, self.options, self.SAVESRC, name, opts = fig, fig.options, fig.options.saveSrc, fig.figName, fig.options
        self.fig_prefix,self.src_prefix,self.src_file = opts.out+name,opts.srcPath+name+'-src',opts.srcPath+name+'-src.csv'
        self.figFiles = {ending: self.fig_prefix +'.'+ending for ending in self.options.figFormats} 
        return self 

    def save(self,NULL=False): 
        if self.INIT: self.show('\n'+self.spl+'  Complete (Figure Saved: '+self.fig_prefix+')\n')  
        else:         self.show('....Complete (Figure Saved: '+self.fig_prefix+')\n')  
        if NULL: return 
        for k,fn in self.figFiles.items(): plt.savefig(fn, dpi = self.options.dpi) 
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

    def start_src(self, format_string, start_tuple): 
        if self.out3 is None or self.out3.closed: self.out3 = open(self.src_file,'w') 
        self.format_string = format_string 
        self.out3.write(self.format_string % start_tuple) 
        return 

    def add_to_src(self, src_data): 
        for sd in src_data: 
            self.out3.write(self.format_string % tuple([self.panel]+sd)) 












