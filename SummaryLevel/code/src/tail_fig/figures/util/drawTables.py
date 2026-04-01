import sys, os 

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path: sys.path.insert(0, HERE)
import drawVarious as DV 
from Util import * 




    




class BicTable:
    def __init__(self,options, clr='white'): 
        self.options = options 
        self.rows, self.cols, self.clr  = [], [], clr 
        self.widths = [22,12,10,11,11,17,17,10,10,10]
        self.vwid = [0] + [sum(self.widths[0:i+1]) for i in range(len(self.widths))]   

    def get_loc(self,X,Y):
        x1,x2 = X[0]/100.0 , X[1]/100.0
        y1,y2 = Y[0]/100.0 , Y[1]/100.0
        return (x1,y1,x2-x1,y2-y1)

    def add_row(self,row_data,X=None,Y=None,COLORS=[],WIDTHS=[],FS=13,ALPHA=0.4,TITLE=False, CL = 'center',STYLE='ALL'):  
        if X == None: X = self.X_SPAN
        if Y == None: Y = self.Y_SPAN
        cL,rL,rD,xL = 'center',None,[row_data],len(row_data)  
        bl = self.get_loc(X,Y) 
        while len(WIDTHS) < len(row_data): WIDTHS.append(10) 
        while len(COLORS) < len(row_data): COLORS.append('white') 
        COLORS = ['white' for i in range(len(row_data))] 
        row = self.ax.table(cellText=rD,rowLabels=rL,cellColours = [COLORS[0:xL]],colWidths=WIDTHS[0:xL],bbox=bl,cellLoc=cL, alpha=ALPHA, clip_on=False) 
        row.auto_set_font_size(False)
        row.set_fontsize(FS)
        if STYLE == 'ALL': 
            for cell in row.get_celld().values():
                cell.set_linewidth(0.1)
        elif STYLE == 'BLOCK': 
            for cell in row.get_celld().values():
                cell.visible_edges = 'TRB'
                cell.set_linewidth(0.1)
        elif STYLE == 'BOTTOM': 
            for cell in row.get_celld().values():
                cell.visible_edges = 'B'
                cell.set_linewidth(0.9)
        elif STYLE == 'MID': 
            for cell in row.get_celld().values():
                cell.visible_edges = ''
        else: 
            for cell in row.get_celld().values():
                cell.visible_edges = 'horizontal'
                cell.set_linewidth(0.2)
        
        if STYLE == 'LABS': 
            self.ax.plot([68,68],[72,100], color='k',lw=0.1,zorder=99) 





    def generate_bic_models(self, traits): 
        self.K = dd(list)  
        for ti,T in traits.items(): 
            if str(T.vals['lrs'].altbool) == 'False': continue 
            V = T.vals['lrs'] 
            model1, model2 = V.model, V.altmodel 
            if model1 == 'Y~yInt+X+X2': NESTED=True
            elif model1 in ['Y~yInt+X','Y~yInt+X2'] and model2 == 'Y~yInt': NESTED=True  
            else: NESTED=False 
            s1, s2 = ['+' if p > 0 else '-' for p in V.params[1::]], ['-','-'] 
            if V.altbeta1 != 'NA' and V.altbeta1 > 0: s2[0] = '+' 
            if V.altbeta2 != 'NA' and V.altbeta2 > 0: s2[1] = '+' 
            eqns, dirs = [], []  
            for m,s in zip([model1,model2],[s1,s2]): 
                if m == 'Y~yInt':      eqns.append('Y~X_o')  
                elif m == 'Y~yInt+X':  eqns.append('Y~X_o'+s[0]+'X') 
                elif m == 'Y~yInt+X2': eqns.append('Y~X_o'+s[0]+'X^2') 
                else:                  eqns.append('Y~X_o'+s[0]+'X'+s[1]+'X^2') 
            for i,e in enumerate(eqns): 
                if e == 'Y~X_o': dirs.append('neutral') 
                elif e == 'Y~X_o+X': dirs.append('positive') 
                elif e == 'Y~X_o-X': dirs.append('negative') 
                elif e == 'Y~X_o-X^2': dirs.append('stabilising') 
                elif e == 'Y~X_o+X^2': dirs.append('disruptive') 
                elif e == 'Y~X_o+X-X^2': dirs.append('pos,stabilising') 
                elif e == 'Y~X_o+X+X^2': dirs.append('pos,disruptive') 
                elif e == 'Y~X_o-X-X^2': dirs.append('neg,stabilising') 
                elif e == 'Y~X_o-X+X^2': dirs.append('neg,disruptive') 
                else:                    dirs.append('neutral')                 
            if NESTED: self.K['NESTED'].append([T.name.mini, T, [model1, model2], eqns, dirs, V.altpv])  
            else:      self.K['COMPLEX'].append([T.name.mini, T, [model1, model2], eqns, dirs, round(V.altbic-V.bic,3)])  



    def draw_lead(self,title, fs1=9, fs3=7):  
        if title == 'Nested Alternatives': 
            yA, yB, yC = 74, 93, 100
            labs = ['Model','Selective\nPressure','Model\nConfidence\n(LRT P-Value)','Model','Selective\nPressure'] 
        else:                              
            yA, yB, yC = 72, 91, 100
            labs = ['Model','Selective\nPressure','$\Delta$BIC','Model','Selective\nPressure'] 
        self.add_row(['Trait'], X = (0,self.w1[0]), Y = (yA, yC), FS = fs1, WIDTHS = [self.w1[0]], STYLE='BLOCK')
        self.add_row(['Top Model','Alternate Model'],X=(self.w1[0],100), Y = (yB,yC), FS=fs3, WIDTHS=self.w1[1:3], STYLE="HORZ") 
        self.add_row(labs,  X = (self.w1[0],100), Y = (yA, yB), FS = fs3, WIDTHS = self.w2[1::],  STYLE="LABS") 
        self.ax.set_title(title, fontsize=10, y=0.98) 

    def close_table(self): 
        self.ax.set_xlim(0,100) 
        self.ax.set_ylim(0,100) 
        self.ax.axis('off') 
        x1,x2 = self.ax.get_xlim() 
        y1,y2 = self.ax.get_ylim() 



    def draw_bic_table(self, ax1, ax2, fs1 = 9, fs2 = 8, fs3 = 7): 
        self.y1, self.y2, self.y3 = 2 , 70, 85 
        alp = 0.1 
        self.w1 = [25,43,32] 
        self.w2 = [25,13,20,10,15,17] 
        w1 = [25,43,32] 
        w2 = [25,13,20,10,15,17] 
        self.ax = ax1 
        self.draw_lead('Nested Alternatives') 
        yp, yj = 63, 7
        kD = sorted(self.K['NESTED']) 
        for i,(name,T,models,eqns,dirs,pv) in enumerate(kD): 
            my_eq = '$'+eqns[0].split('~')[0] + '{\sim}' + eqns[0].split('~')[-1]+'$'
            tr = [T.name.mini, my_eq, dirs[0], pv, '$'+eqns[1]+'$', dirs[1]] 
            if i + 1 < len(kD): self.add_row(tr, X = (0,100), Y = (yp, yp+yj), FS = fs3, WIDTHS = w2, STYLE='MID') 
            else:               self.add_row(tr, X = (0,100), Y = (yp, yp+yj), FS = fs3, WIDTHS = w2, STYLE='BOTTOM') 
            yp -= yj
        self.close_table() 
        self.ax = ax2 
        self.draw_lead('Complex Alternatives') 
        yp, yj = 60, 10
        kD = sorted(self.K['COMPLEX']) 
        for i,(name,T,models,eqns,dirs,pv) in enumerate(kD): 
            my_eq = '$'+eqns[0].split('~')[0] + '{\sim}' + eqns[0].split('~')[-1]+'$'
            tr = [T.name.mini, my_eq, dirs[0], pv, '$'+eqns[1]+'$', dirs[1]] 
            if i + 1 < len(kD): self.add_row(tr, X = (0,100), Y = (yp, yp+yj), FS = fs3, WIDTHS = self.w2, STYLE='MID') 
            else:               self.add_row(tr, X = (0,100), Y = (yp, yp+yj), FS = fs3, WIDTHS = self.w2, STYLE='BOTTOM') 
            yp -= yj
        self.close_table() 
        return

            
            













class SummaryTable:
    def __init__(self, plot, clr='white', PETT=False): 
        self.plot, self.options = plot, plot.options 
        self.rows, self.cols, self.clr  = [], [], clr 

    def get_loc(self,X,Y):
        x1,x2 = X[0]/100.0 , X[1]/100.0
        y1,y2 = Y[0]/100.0 , Y[1]/100.0
        return (x1,y1,x2-x1,y2-y1)

    def add_row(self,row_data,X=None,Y=None,COLORS=[],WIDTHS=[],FS=13,ALPHA=-1,LINECOLOR='k',TITLE=False, CL = 'center',CLEAR=False): 
        if X == None: X = self.X_SPAN
        if Y == None: Y = self.Y_SPAN
        if ALPHA == -1: ALPHA=1
        cL,rL,rD,xL = CL,None,[row_data],len(row_data)  
        bl = self.get_loc(X,Y) 
        while len(WIDTHS) < len(row_data): WIDTHS.append(10) 
        while len(COLORS) < len(row_data): COLORS.append('white') 
        if CL != 'center': row = self.ax.table(cellText=rD,rowLabels=rL,cellColours = [COLORS[0:xL]],colWidths=WIDTHS[0:xL],bbox=bl,loc = cL, cellLoc=cL, alpha=ALPHA, clip_on=False) 
        else:              row = self.ax.table(cellText=rD,rowLabels=rL,cellColours = [COLORS[0:xL]],colWidths=WIDTHS[0:xL],bbox=bl,cellLoc=cL, alpha=ALPHA, clip_on=False) 
        row.auto_set_font_size(False)
        row.set_fontsize(FS)
        table_props = row.properties()
        self.rows.append(row) 
        for cell in row.get_celld().values():
            cell.set_linewidth(0.2)
        if ALPHA > -1: 
            for cell in row._cells: 
                row._cells[cell].set_alpha(ALPHA)
                if LINECOLOR != 'k':
                    cw, ch = row._cells[cell]._width, row._cells[cell]._height
                    cx, cy = row._cells[cell]._x0, row._cells[cell]._y0
                    rect = matplotlib.patches.Rectangle((cx+0.1 , 2 ), cw-0.2, 97,facecolor='white', edgecolor=LINECOLOR, linewidth=1) 
        self.rows.append(row) 


    def initalize(self,ax1,ax2, c1 = 'gray', c2 = 'red', fs1=10, fs2=7, fs3 = 6, fs4=5):
        headers = [['Trait'],['Plots']]
        labs = [['Abbreviated Name\n[UKB ID]\nCategory'],['PRS on\nPhenotype\nQuantile Plot','Conditional\nSibling\nDistribution','Selection\nInference\nDistribution']] 
        for i,(h,ax) in enumerate(zip(headers,[ax1,ax2])): 
            self.ax = ax 
            self.add_row(h, COLORS=[c2],X=(0,100), Y=(65,100), FS=fs2, WIDTHS=[100], TITLE=False)
            self.add_row(labs[i], X=(0,100), Y=(0,65), FS=fs4, WIDTHS=[100/float(len(labs[i])) for x in labs[i]], TITLE=False)
            self.ax.axis('off') 
            self.ax.set_xlim(0,100) 
            self.ax.set_ylim(0,100) 
        return self


    def add_trait(self, ax, T, clr = 'white',ALP=0.3, fs1=10,fs2=8, fs3=7,fs4=6,fs5=5): 
        self.ax, self.clr = ax, clr 
        self.add_row([''],COLORS=[self.clr],X=(0,100),LINECOLOR=T.group_color,Y=(0,100),FS=0,WIDTHS=[100],TITLE=False,ALPHA=1) 
        mn = str(T.name.mini)+'\n['+str(T.id)+']'
        self.add_row([mn],COLORS=[self.clr],X=(0,100),Y=(35,90),FS=fs4,WIDTHS=[100],TITLE=False,ALPHA=0.0)  
        self.add_row([T.group],COLORS=[self.clr],X=(0,100),Y=(0,25),FS=fs5,WIDTHS=[100],TITLE=False,ALPHA=0.0)  
        self.ax.axis('off') 
        self.ax.set_xlim(0,100) 
        self.ax.set_ylim(0,100) 
        return [] 
        


























class SnpTable:
    def __init__(self, plot, kind, clr='white', PETT=False): 
        self.plot, self.type, self.options = plot, kind, plot.options 
        

        self.rows, self.cols, self.clr  = [], [], clr 
        self.widths = [75,25] 
        self.vwid = [0] + [sum(self.widths[0:i+1]) for i in range(len(self.widths))]   

    def get_loc(self,X,Y):
        x1,x2 = X[0]/100.0 , X[1]/100.0
        y1,y2 = Y[0]/100.0 , Y[1]/100.0
        return (x1,y1,x2-x1,y2-y1)

    def add_row(self,row_data,X=None,Y=None,COLORS=[],WIDTHS=[],FS=13,ALPHA=-1,LINECOLOR='k',TITLE=False, CL = 'center',CLEAR=False): 
        if X == None: X = self.X_SPAN
        if Y == None: Y = self.Y_SPAN
        if ALPHA == -1: ALPHA=1
        cL,rL,rD,xL = CL,None,[row_data],len(row_data)  
        bl = self.get_loc(X,Y) 
        while len(WIDTHS) < len(row_data): WIDTHS.append(10) 
        while len(COLORS) < len(row_data): COLORS.append('white') 
        if CL != 'center': row = self.ax.table(cellText=rD,rowLabels=rL,cellColours = [COLORS[0:xL]],colWidths=WIDTHS[0:xL],bbox=bl,loc = cL, cellLoc=cL, alpha=ALPHA, clip_on=False) 
        else:              row = self.ax.table(cellText=rD,rowLabels=rL,cellColours = [COLORS[0:xL]],colWidths=WIDTHS[0:xL],bbox=bl,cellLoc=cL, alpha=ALPHA, clip_on=False) 
        row.auto_set_font_size(False)
        row.set_fontsize(FS)
        table_props = row.properties()
        if ALPHA > -1: 
            for cell in row._cells: 
                row._cells[cell].set_alpha(ALPHA)
                if LINECOLOR != 'k':
                    cw, ch = row._cells[cell]._width, row._cells[cell]._height
                    cx, cy = row._cells[cell]._x0, row._cells[cell]._y0
                    rect = matplotlib.patches.Rectangle((cx+0.1 , 2 ), cw-0.2, 97,facecolor='white', edgecolor=LINECOLOR, linewidth=6) 
        self.rows.append(row) 






    def initalize(self,axes, c1 = 'gray', c2 = 'red', fs1=9, fs2=7, fs3 = 18):
        self.y1, self.y2 = 1 , 60

        if self.type == 'annotated_rares': 
            h1 = ['Variant Information'] 
            h2 = ['DRAGEN-ID','rsId','MAF','Type','Genes(s)'] 
            self.snp_widths = [28,20,13,21,18] 
        else: 
            h1 = ['Burden Variant'] 
            h2 = ['DRAGEN-ID','Masks','MAF','Type','Genes(s)'] 
            self.snp_widths = [30,16,13,21,20] 



        for i,ax in enumerate(axes): 
            self.ax = ax 
            if i == 0: 
                self.add_row(h1, COLORS=[c2],X=(0,100), Y=(self.y2,100), FS=fs1, WIDTHS=[100], TITLE=True)
                self.add_row(h2, COLORS=[c2 for h in h2],X=(0,100), Y=(0,self.y2), FS=fs1, WIDTHS=self.snp_widths, TITLE=True)
            elif i == 1: 
                h1 = ['Genome Wide Significant Effects'] 
                h2 = ['Trait Decreasing','Trait Increasing'] 
                self.add_row(h1, COLORS=[c2],X=(0,100), Y=(self.y2,100), FS=fs1, WIDTHS=[100], TITLE=True)
                self.add_row(h2, COLORS=[c2 for h in h2],X=(0,100), Y=(0,self.y2), FS=fs1, WIDTHS=[50,50], TITLE=True)
            elif i == 2: 
                h1 = ['ClinVar Annotations'] 
                h2 = ['Reported Phenotype(s)'] 
                self.add_row(h1, COLORS=[c2],X=(0,100), Y=(self.y2,100), FS=fs1, WIDTHS=[100], TITLE=True)
                self.add_row(h2, COLORS=[c2 for h in h2],X=(0,100), Y=(0,self.y2), FS=fs1, WIDTHS=[100], TITLE=True)


            self.ax.set_xlim(0,100) 
            self.ax.set_ylim(0,100) 
            ek = 'darkslategray'
            self.ax.axis('off') 
        if self.type == 'annotated_rares': axes[1].set_title('Annotated Rare Variants', ha = 'center', fontsize = fs1, fontweight='bold',x=0.35) 
        elif self.type == 'annotated_burdens': axes[1].set_title('Annotated Burden Variants', ha = 'center', fontsize = fs1, fontweight='bold',x=0.35) 
        else:                                  axes[1].set_title('Unannotated Burden Variants', ha = 'center', fontsize = fs1, fontweight='bold',x=0.35) 
        return self 


    def double_up(self, X): 
        X.sort() 
        if len(X) > 3: 
            if len(X) < 5: end = 2 
            elif len(X) < 7: end = 3 
            elif len(X) < 9: end = 4
            else:            end = 5 
            
            x1, x2 = X[0:end], X[end::] 
            ML = max(len(x1),len(x2)) 
            return ML, ",".join(x1)+',\n'+','.join(x2) 
        return len(X), ','.join(X)  

                





    def add_snp(self, axes, s, clr = 'white',ALP=0.3, fs1=30, fs2=24):         
        self.clr = clr 
        if s.group == 'rare': d1 = [s.loc,s.rs, s.maf, s.type, s.genes] 
        else:                 d1 = [s.loc,len(s.masks), s.mafs[0], 'Burden',s.genes]             
        self.ax = axes[0]  
        wx = 0 
        fzd = [fs1+2, fs1+5, fs1+5, fs1+4, fs1+6] 
        for i,(fs, d,w) in enumerate(zip(fzd, d1,self.snp_widths)): 
            if len(str(d)) * 2 > w: 
                if i < 3: 
                    if len(str(d))*1.4 > w:   fs -= 4
                    elif len(str(d))*1.6 > w:   fs -= 3
                    elif len(str(d))*1.8 > w: fs -= 2
                    else:                     fs -=  1
                else: 
                    if i == 3:  
                        if self.type == 'annotated_rares': 
                            if len(d.split(';')) > 1: d = '\n'.join(d.split(';')) 
                            else:                     fs -= 2
                    else: fs -= 2
            fs = 7 
            self.add_row([d], COLORS=[self.clr],X=(wx,wx+w), Y=(0,100), FS=fs, WIDTHS=[w], TITLE=True)
            wx += w 




        self.ax = axes[1]  
        clins = [list(set([T.name.snp for v,p,T in s.hits if v < 0])),list(set([T.name.snp for v,p,T in s.hits if v>0]))]
        c1,d1 = self.double_up(clins[0])
        c2,d2 = self.double_up(clins[1]) 
        self.add_row([d1,d2], COLORS=[self.clr, self.clr],X=(0,100), Y=(0,100), FS=7, WIDTHS=[50,50], TITLE=True)        

        self.ax = axes[2] 
        

         

        sA = [" ".join(sa.split('_')) for sa in s.annos]
        sNew = ",\n".join([",".join(sA[j:j+3]) for j in range(0,len(sA),3)]) 
        if len(sNew) > 100:  self.add_row([sNew], COLORS=[self.clr],X=(0,100), Y=(0,100), FS=7, WIDTHS=[100], TITLE=True)        
        elif len(sNew) > 50: self.add_row([sNew], COLORS=[self.clr],X=(0,100), Y=(0,100), FS=7, WIDTHS=[100], TITLE=True)        
        else:                self.add_row([sNew], COLORS=[self.clr],X=(0,100), Y=(0,100), FS=7, WIDTHS=[100], TITLE=True)        

        for ax in axes: ax.axis('off') 

        return

        self.ax, self.clr = ax, clr 
        fs0,fs1, fs2, fs3 = 25,20, 18, 15
        self.y0, self.y1, self.y2 = 1, 0, 70 
        name1, name2 = str(T.name.flat), str(T.name.aou) 
        fs1, fs2 = self.get_fontsize(len(str(name1))), self.get_fontsize(len(str(name2))) 
        d0 = T.name.mini+' ['+str(T.id)+']\n'+T.group
        self.add_row([''],COLORS=[self.clr],X=(0,self.widths[0]),LINECOLOR=T.group_color,Y=(self.y1,100),FS=0,WIDTHS=[self.widths[0]],TITLE=True,ALPHA=1) 
        mn = str(T.name.mini)+' ['+str(T.id)+']'
        if   len(mn) > 35: fz = 22
        elif len(mn) > 32: fz = 25
        elif len(mn) > 30: fz = 27
        elif len(mn) > 28: fz = 29
        elif len(mn) > 24: fz = 32 
        elif len(mn) > 21: fz = 35
        elif len(mn) > 19: fz = 37
        else:              fz = 40 

        self.add_row([mn],COLORS=[self.clr],X=(0,self.widths[0]),Y=(70,96),FS=fz,WIDTHS=[self.widths[0]],TITLE=True,ALPHA=0.0)  
        self.add_row([T.group],COLORS=[self.clr],X=(0,self.widths[0]),Y=(46,66),FS=28,WIDTHS=[self.widths[0]],TITLE=True,ALPHA=0.0)  
        


        self.add_row([name1[0:48]],COLORS=[self.clr],X=(0,self.widths[0]),Y=(22,40),FS=fs1,WIDTHS=[self.widths[0]],TITLE=True,ALPHA=0.0)  
        self.add_row([name2],COLORS=[self.clr],X=(0,self.widths[0]),Y=(1,18),FS=fs2,WIDTHS=[self.widths[0]],TITLE=True,ALPHA=0.0)  
        
        d2 = self.get_smart_str(T) 
        self.add_row([d2],COLORS=[self.clr],X=(self.vwid[1],self.vwid[2]),Y=(self.y1,100),FS=fs0+7,WIDTHS=[self.widths[1]],TITLE=True)       
        self.ax.set_xlim(0,100) 
        self.ax.set_ylim(0,100) 
        self.ax.axis('off') 
        return [] 
        


class CompTable:
    def __init__(self, ax, options, clr='white'): 
        self.options = options 
        self.ax, self.rows, self.cols, self.clr  = ax, [], [], clr 

    def get_loc(self,X,Y):
        x1,x2 = X[0]/100.0 , X[1]/100.0
        y1,y2 = Y[0]/100.0 , Y[1]/100.0
        return (x1,y1,x2-x1,y2-y1)

    def add_row(self,row_data,X=None,Y=None,COLORS=[],WIDTHS=[],FS=13,ALPHA=0.4,TITLE=False, STYLE='NA'): 
        if X == None: X = self.X_SPAN
        if Y == None: Y = self.Y_SPAN
        cL,rL,rD,xL = 'center',None,[row_data],len(row_data)  
        bl = self.get_loc(X,Y) 
        while len(WIDTHS) < len(row_data): WIDTHS.append(10) 
        while len(COLORS) < len(row_data): COLORS.append('white') 
        COLORS = ['white' for i in range(len(row_data))] 
        row = self.ax.table(cellText=rD,rowLabels=rL,cellColours = [COLORS[0:xL]],colWidths=WIDTHS[0:xL],bbox=bl,cellLoc=cL, alpha=ALPHA, clip_on=False) 
        row.auto_set_font_size(False)
        row.set_fontsize(FS)
        if STYLE == 'ALL': 
            for cell in row.get_celld().values():
                cell.set_linewidth(0.1)

        elif STYLE == 'BOTTOM': 
            for cell in row.get_celld().values():
                cell.visible_edges = 'B'
                cell.set_linewidth(0.4)
        elif STYLE == 'MID': 
            for cell in row.get_celld().values():
                cell.visible_edges = ''
        else: 
            for cell in row.get_celld().values():
                cell.visible_edges = 'horizontal'
                cell.set_linewidth(0.2)
        


    def initialize(self, fs1 = 10, fs2 = 9, fs3 = 8, fs4=7, c1='white', c2='white'): 
        self.y1, self.y2, self.y3 = 2 , 70, 85 
        alp = 0.1 
        self.widths = [20,12,10,10,10,10,7,7,7,7]
        self.vwid = [0] + [sum(self.widths[0:i+1]) for i in range(len(self.widths))]   
        self.add_row(['Trait Name\n[UKB ID]'], X = (0,self.widths[0]), Y = (90, 100), FS = fs1, WIDTHS = [self.widths[0]], TITLE=True, ALPHA=alp)
        x1, xl = 12, 20
        self.add_row(['Model Selection'], X = (self.vwid[1],self.vwid[4]), Y = (97, 100), FS = fs1, WIDTHS = [xl], STYLE='ALL')
        my_labs = ['Top Model','Linear\nParameter\n($\\beta$)','Quadratic\nParameter \n($\gamma$)'] 
        self.add_row(my_labs,  X = (self.vwid[1],self.vwid[4]), Y = (90, 97), FS = fs3, WIDTHS = self.widths[1:4], STYLE='ALL',ALPHA=alp)
        self.add_row(['Sanjak et al'], X = (self.vwid[4],100), Y = (97, 100), FS = fs1, WIDTHS = [44], TITLE=True, ALPHA=alp)
        self.add_row(['Aggregate Result','Males','Females'], X = (self.vwid[4],100), Y = (93, 97), FS = fs1, WIDTHS = [20, 14, 14], TITLE=True, ALPHA=0.1)
        self.add_row(['$\\beta$','$\gamma$','$\\beta$','$\gamma$','$\\beta$','$\gamma$'],  X = (self.vwid[4],100), Y = (90, 93), FS = fs1, WIDTHS = self.widths[4::], TITLE=True,ALPHA=alp) 
        yp, yj = 85, 4.70
        return self 




    def add_data(self, reg_traits, sex_diffs, fs1=10, fs2=8, fs3=7, alp=0.2): 

        yp, yj = 85, 4.70
        self.add_row(['Traits Without Sex Differences'], COLORS = ['purple'], X = (0,100), Y = (yp+yj/2.0, yp+yj+0.3), FS = fs3, WIDTHS = [12], STYLE='BOTTOM') 
        yp -= yj/2.0
        K = self.get_my_key(reg_traits+ sex_diffs) 
        reg_traits.sort(key = lambda X: X.name.mini) 
        for T in reg_traits: 
            L,S = T.vals['lrs'], T.vals['sanjak'] 
            s_data = [str(S.key[k]) for k in ['beta-dir','gamma-dir','beta-male','gamma-male','beta-female','gamma-female']] 
            sig_data = ['False','False'] + [S.key[k] for k in ['beta-male-sig','gamma-male-sig','beta-female-sig','gamma-female-sig']] 
            for i,sig in enumerate(sig_data): 
                if sig == 'True': s_data[i]+='*' 
            full_data = K[T.ti] + s_data 
            self.add_row(full_data,  X = (0,100), Y = (yp, yp+yj), FS = fs3, WIDTHS = self.widths, STYLE='MID') 
            yp -= yj 

        self.add_row(['Traits With Sex Differences'], COLORS = ['purple'], X = (0,100), Y = (yp+yj/2.0, yp+yj), FS = fs3, WIDTHS = [12], STYLE="HORZ") 
        yp -= yj/2.0
        sex_diffs.sort(key = lambda X: X.name.mini) 
        for T in sex_diffs: 
            L,S = T.vals['lrs'], T.vals['sanjak'] 
            s_data = [str(S.key[k]) for k in ['beta-dir','gamma-dir','beta-male','gamma-male','beta-female','gamma-female']] 
            sig_data = ['False','False'] + [S.key[k] for k in ['beta-male-sig','gamma-male-sig','beta-female-sig','gamma-female-sig']] 
            for i,sig in enumerate(sig_data): 
                if sig == 'True': s_data[i]+='*' 
            
                elif i == 0 and len(s_data[i].split(',')) > 1: 
                    s_data[i] = ",\n".join(s_data[i].split(',')) 
            full_data = K[T.ti] + s_data 
            self.add_row(full_data,  X = (0,100), Y = (yp, yp+yj), FS = fs3, WIDTHS = self.widths, STYLE="MID") 
            yp -= yj 

        self.ax.set_xlim(0,100) 
        self.ax.set_ylim(0,100) 
        x1,x2 = self.ax.get_xlim() 
        y1,y2 = self.ax.get_ylim() 

        self.ax.plot([x1,x2],[y2,y2],color='k',lw=1) 
        self.ax.plot([x1,x2],[y2-10,y2-10],color='k',lw=1) 
        self.ax.plot([x1,x1],[y2-10,y2],color='white',lw=2) 
        self.ax.plot([x2,x2],[y2-10,y2],color='white',lw=2) 
        self.ax.plot([x1,x2],[y1+10,y1+10],color='k',lw=1) 
        self.ax.axis('off') 
        return
            

    def get_my_key(self, traits): 
        K = {} 
        for T in traits: 
            my_data = [T.name.flat+'\n('+str(T.ti)+')']
            if len(T.name.flat) < 33: my_data = [T.name.flat+'\n('+str(T.ti)+')']
            else: my_data = [T.name.mini+'\n('+str(T.ti)+')']
            L,S = T.vals['lrs'], T.vals['sanjak'] 
            if L.model  == 'Y~yInt': tm = '$Y{\sim}X_o$' 
            elif L.model == 'Y~yInt+X': tm = '$Y{\sim}X_o{+}X$' 
            elif L.model == 'Y~yInt+X2': tm = '$Y{\sim}X_o{+}X^2$' 
            elif L.model == 'Y~yInt+X+X2': tm = '$Y{\sim}X_o{+}X{+}X^2$' 
            my_data.append(tm) 
            for i,p in enumerate(L.params[1::]): 
                if p == 0:  my_data.append('0\n(neutral)') 
                elif i == 0: 
                    if p > 0:   my_data.append(str(round(p,3))+'\n(positive)') 
                    else:       my_data.append(str(round(p,3))+'\n(negative)') 
                else: 
                    if p > 0:   my_data.append(str(round(p,3))+'\n(disruptive)') 
                    else:       my_data.append(str(round(p,3))+'\n(stabilising)') 
            K[T.ti] = my_data
        return K




        
