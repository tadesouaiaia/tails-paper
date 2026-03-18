import sys,os,importlib 
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path: sys.path.insert(0, HERE)
import figProgress as FP
import figTraits as FT


from figures.util.Util import * 





class figGen:
    def __init__(self, args, command_line):
        self.args  = args
        self.progress = FP.Progress(args, command_line)
        self.check_imports() 
        self.traits = FT.Traits(args.infile, args).load(args.vals, args.pts)         
        self.fig_goals = self.parse_instructions(self.args.which.upper()) 
        self.validate_index([str(ti) for ti in args.indexTraits if ti not in self.traits.members.keys()]) 



    def check_imports(self): 
        self.args.missing_modules = [] 
        import importlib 
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


         

    def parse_instructions(self, X): 
        main_out, xtd_out, sup_out, tab_out = ['main'+str(i) for i in [1,2,3,4,5]],['xtd'+str(i+1) for i in range(10)], ['sup1','sup2'], ['csv'] 
        main_in, sup_in= ['MAIN-FIGURES','MAIN-FIGS','MAIN','MAINS','FIGS'],['SUP','SUPS'] 
        xtd_in, tab_in = ['EXTENDED-DATA','XTDS','EXTS','XTD','EXT'], ['TABLES','EXCEL','TABS','CSV'] 
        if X == 'ALL': return main_out + xtd_out + sup_out + tab_out 
        for a,b in [[main_in,main_out],[xtd_in,xtd_out],[tab_in, tab_out],[sup_in,sup_out]]: 
            if X in a: return b 
        if X.lower() in main_out+xtd_out+sup_out: return [X.lower()]
        try: 
            for m in main_in: 
                if X[0:len(m)] == m: a,b = 'MAIN', X[len(m)::] 
            for m in xtd_in: 
                if X[0:len(m)] == m: a,b = 'XTD', X[len(m)::] 
        
        
            b1, b2 = int(b.split('-')[0]), int(b.split('-')[-1]) 
            vals = [i for i in range(11) if i >= b1 and i <= b2] 
            if len(vals) > 0:  
                if a == 'XTD'  and b2 < 11: return ['xtd'+str(v) for v in vals] 
                if a == 'MAIN' and b2 < 6: return ['main'+str(v) for v in vals] 
        except: pass 

        sys.stderr.flush() 
        sys.stdout.write('Invalid Figure Command: Try: ./tails gen all or tails gen fig2\n') 
        sys.exit() 



    def go(self):
        for goal in self.fig_goals:
            if goal in ['main1','main2','main3','main4','main5']: 
                gn = goal[-1]  
                mod = importlib.import_module(f"figures.fig{gn}")
                self.progress.start_step('Generating Main Figure '+gn)
                fig = mod.MyFigure(self.args, self.traits, self.progress,figName = goal).draw() 
            elif goal[0:3] in ['xtd']:
                gn = goal[3::]
                self.progress.start_step('Generating Extended Data Figure '+gn) 
                if gn in ['5','6','7']: 
                    import figures.xtdSnp as SF  
                    fig = SF.MyFigure(self.args, self.traits, self.progress, figName=goal).draw_one(int(gn))
                else:
                    mod = importlib.import_module(f"figures.xtd{gn}")
                    fig = mod.MyFigure(self.args, self.traits, self.progress,figName = goal).draw() 

            elif goal[0:3] == 'csv': 
                import figures.xtdCsv as SF  
                self.progress.start_step('Generating Excel Tables...') 
                fig = SF.MyFigure(self.args, self.traits, self.progress, figName=goal).draw() 
            
            elif goal == 'sup1': 
                import figures.sup1 as SF 
                self.progress.start_step('Generating Sup Figure 1...') 
                fig = SF.MyFigure(self.args, self.traits, self.progress, figName=goal).draw() 
            elif goal == 'sup2': 
                import figures.sup2 as SF 
                self.progress.start_step('Generating Sup Figure 2...') 
                fig = SF.MyFigure(self.args, self.traits, self.progress, figName=goal).draw() 
            else: sys.stdout('Unrecognized Goal') 


        self.progress.complete_all(NEW=True) 
        return





