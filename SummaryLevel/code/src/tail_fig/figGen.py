import sys,os,importlib 
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path: sys.path.insert(0, HERE)
from figures.util.Util import * 
import figProgress as FP
import figTraits as FT

class figGen:
    def __init__(self, args, fig_goals, command_line):
        self.args, self.fig_goals  = args, fig_goals 
        self.progress = FP.Progress(args, command_line)
        self.check_imports() 
        self.traits = FT.Traits(args.infile, args).load(args.vals, args.pts)         
        self.validate_index([str(ti) for ti in args.indexTraits if ti not in self.traits.members.keys()]) 

    def check_imports(self): 
        self.args.missing_modules = [] 
        for m in ['matplotlib','numpy','scipy','statsmodels']: 
            try: mod = importlib.import_module(m)
            except ModuleNotFoundError: self.args.missing_modules.append(m) 
        if len(self.args.missing_modules) > 0: self.progress.warn('The following modules are missing: '+",".join(self.args.missing_modules))

    def validate_index(self, missing): 
        if len(missing) == 0: return 
        e1 = 'Index Trait(s): '+','.join(missing)+', not found in trait input ('+self.args.infile.name.split('/')[-1]+')'
        e2 = '               Choosing four existing index traits is reccommended, eg. (--indexTraits A B C D)' 
        self.progress.warn(e1+'\n'+e2) 
        self.args.indexTraits = [x if str(x) not in missing else 0 for x in self.args.indexTraits] 
        return 

    def go(self):
        for goal in self.fig_goals:
            gn, gm = goal[3::], goal[4::] 
            if goal in ['main1','main2','main3','main4','main5']: 
                gn = goal[-1]  
                mod = importlib.import_module(f"figures.fig{gm}")
                self.progress.start_step('Generating Main Figure '+gm)
                fig = mod.MyFigure(self.args, self.traits, self.progress,figName = goal).draw() 
            elif goal[0:3] == 'csv': 
                import figures.xtdCsv as SF  
                self.progress.start_step('Generating Excel Tables...') 
                fig = SF.MyFigure(self.args, self.traits, self.progress, figName=goal).draw() 
            elif goal[0:3] == 'sup': 
                mod = importlib.import_module(f"figures.sup{gn}")
                self.progress.start_step('Generating Sup Figure '+gn)
                fig = mod.MyFigure(self.args, self.traits, self.progress,figName = goal).draw() 
            else: 
                self.progress.start_step('Generating Extended Data Figure '+gn) 
                if gn in ['5','6','7']: mod = importlib.import_module(f"figures.xtdSnp")
                else: mod = importlib.import_module(f"figures.xtd{gn}")
                fig = mod.MyFigure(self.args, self.traits, self.progress, figName=goal).draw()
        self.progress.finish(NEW=True) 
        return
