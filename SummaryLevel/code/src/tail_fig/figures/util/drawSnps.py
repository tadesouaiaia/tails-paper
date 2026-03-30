import sys, os 
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path: sys.path.insert(0, HERE)
import drawVarious as DV 
from Util import * 



 
MK = {'0.1%-1%':'<1%','0.01%-0.1%':'<0.01%','~0.1%':'~0.1%','~0.01%':'~0.01%','~1%':'~1%'} 
SK = {'3_prime_utr':'3pUTR','5_prime_utr':'5pUTR','missense-snp':'missense','synonymous-snp':'synonymous','missense-indel':'missense'} 


class RareSnp:
    def __init__(self, loc, s, group = 'rare'): 
        #self.loc, self.group = loc, group
        self.loc, self.group, self.hits, self.genes, self.annos = loc, group, [], s.gene.split(';'), s.annos.split(';') 
        s.maf = MK[s.maf]        
        if len(self.genes) > 1: self.genes = ',\n'.join(self.genes) 
        else:                   self.genes = self.genes[0] 
        for i in range(len(self.annos)): 
            if len(self.annos[i].split('_')) == 1: continue 
            x = self.annos[i].split("_") 
            if 'related_disorder' in self.annos[i] and x[-1] == 'disorder': self.annos[i] = self.annos[i].split('_disorder')[0]  
            elif x[0] in ['familial','hereditary','recessive']: self.annos[i] = "_".join(x[1::])
            else: continue 
        #self.annos = sorted(list(set(self.annos)) , key = lambda X: len(X)) 
        #self.annos = [a.capitalize() for a in self.annos] 
        self.annos = [a.capitalize() for a in sorted(list(set(self.annos)) , key = lambda X: len(X))]
        if self.group == 'burden': 
            self.add, self.masks, self.mafs = self.add_burden, [s.type], [s.maf] 
        else:                     
            self.add = self.add_rare 
            self.rs, self.type, self.maf = s.rs, s.type, s.maf
            if self.type in SK: self.type = SK[self.type] 
            if len(self.type.split(';')) > 1: self.type = '\n'.join(self.type.split(';')) 

    def add_burden(self, T, k): 
        self.hits.append([k.beta, k.pv, T])  
        self.masks.append(k.type) 
        self.mafs.append(k.maf) 
    
    def add_rare(self, T, k): self.hits.append([k.beta, k.pv, T])  













class SnpTable:
    def __init__(self, fig, kind, clr='white', PETT=False): 
        self.fig, self.type, self.options = fig, kind, fig.options 
        

        self.rows, self.cols, self.clr  = [], [], clr 
        self.widths = [75,25] 
        self.vwid = [0] + [sum(self.widths[0:i+1]) for i in range(len(self.widths))]   

        if kind == 'annotated_rares':
            self.add_snp = self.add_rare_snp 
            self.initialize = self.initialize_rare 
        elif kind == 'annotated_burdens':                         
            self.add_snp = self.add_burden_snp 
            self.initialize = self.initialize_burden
        else: 
            self.add_snp = self.add_novel_snp 
            self.initialize = self.initialize_unannotated_burden




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
                cell.set_linewidth(0.4)
        if STYLE == 'LABS':
            self.ax.plot([68,68],[72,100], color='k',lw=0.1,zorder=99)
        if TITLE:  
            r = len(rD) - 1
            for c in range(xL):
                    row[(r, c)].get_text().set_weight('bold')
        return



    def add_hits(self, ax, hits, MAX_HITS=3): 
        self.ax = ax 
        
        i, j, h1, h2 = 0,0, [], []  
        
        if len(hits[0]) > 0: 
            while i < len(hits[0]) and len(h1) < MAX_HITS: 
                if hits[0][i] not in h1: h1.append(hits[0][i]) 
                i+= 1 
        if len(hits[1]) > 0: 
            while j < len(hits[1]) and len(h2) < MAX_HITS: 
                if hits[1][j] not in h2: h2.append(hits[1][j]) 
                j+= 1

        dstr, ustr  = ",".join(h1), ",".join(h2)  
        dText, uText = [r'$\downarrow$'+dstr], [r'$\uparrow$'+ustr] 
        if len(hits[0]) > 0 and len(hits[1]) > 0: 
            self.add_row(uText, X=(0,100), Y=(52,80), FS=6.5, WIDTHS=[100], STYLE=self.STYLE)
            self.add_row(dText, X=(0,100), Y=(20,48), FS=6.5, WIDTHS=[100], STYLE=self.STYLE)
            self.DOUBLE = True 
        else: 
            self.DOUBLE = False 
            if len(hits[1]) > 0: self.add_row(uText, X=(0,100), Y=(0,100), FS=6.5, WIDTHS=[100], STYLE=self.STYLE)
            if len(hits[0]) > 0: self.add_row(dText, X=(0,100), Y=(0,100), FS=6.5, WIDTHS=[100], STYLE=self.STYLE)
        return  

    def add_annos(self, ax, annos, MAX_LEN=33): 
        self.ax = ax
        aL = [len(a) for a in annos] 
        if len(annos) > 0: 
            if len(annos) == 1: self.add_row([annos[0]], X=(0,100), Y=(0,100), FS=6.5, WIDTHS=[100], STYLE=self.STYLE)
            elif not self.DOUBLE: 
                if aL[0] + aL[1] < MAX_LEN: self.add_row([annos[0]+', '+annos[1]], X=(0,100), Y=(0,100), FS=6.5, WIDTHS=[100], STYLE=self.STYLE)
                else:                  self.add_row([annos[0]], X=(0,100), Y=(0,100), FS=6.5, WIDTHS=[100], STYLE=self.STYLE) 
            else: 
                if len(annos) == 2: self.add_row([annos[0]+',\n'+annos[1]], X=(0,100), Y=(0,100), FS=6.5, WIDTHS=[100], STYLE=self.STYLE)
                else: 
                    if aL[0] + aL[1] < MAX_LEN: 
                        aInit = annos[0]+', '+annos[1]+',\n'+annos[2] 
                        if len(annos) == 3 or (aL[2] + aL[3] > 33): self.add_row([aInit], X = (0, 100), Y=(0,100), FS=6.5, WIDTHS=[100], STYLE=self.STYLE) 
                        else:                                       self.add_row([aInit+', '+annos[3]], X = (0, 100), Y=(0,100), FS=6.5, WIDTHS=[100], STYLE=self.STYLE) 
                    else:                                           self.add_row([annos[0]+',\n'+annos[1]], X = (0, 100), Y=(0,100), FS=6.5, WIDTHS=[100], STYLE=self.STYLE) 
        return 



                
    def add_rare_snp(self, axes, snp_data, idx, tLen, MAX_LEN=16): 
        sd, hits, annos = snp_data[0] 
        self.ax = axes[0]
        if idx + 1 < tLen: self.STYLE = 'MID' 
        else:              self.STYLE = 'BOTTOM' 
        self.add_row(snp_data[0][0], X=(0,100), Y=(0,100), FS=6.5, WIDTHS=self.snp_widths, STYLE=self.STYLE)
        self.add_hits(axes[1], hits) 
        self.add_annos(axes[2], annos)        
        for ax in axes: ax.axis('off') 

    def add_burden_snp(self, axes, snp_data, idx, tLen, MAX_LEN=16): 
        sd, hits, annos = snp_data[0] 
        self.ax = axes[0]
        if idx + 1 < tLen: self.STYLE = 'MID' 
        else:              self.STYLE = 'BOTTOM' 
        self.add_row(snp_data[0][0], X=(0,100), Y=(0,100), FS=7, WIDTHS=self.snp_widths, STYLE=self.STYLE)
        self.add_hits(axes[1], hits, MAX_HITS=4) 
        self.add_annos(axes[2], annos)        
        for ax in axes: ax.axis('off') 



    def add_novel_snp(self, axes, snp_data, idx, tLen, MAX_HITS=4): 
        sd, hits, annos = snp_data[0] 
        self.ax = axes[0]
        if idx + 1 < tLen: self.STYLE = 'MID' 
        else:              self.STYLE = 'BOTTOM' 
        self.add_row(snp_data[0][0], X=(0,100), Y=(0,100), FS=7, WIDTHS=self.snp_widths, STYLE=self.STYLE)

        dstr, ustr  = ",".join(hits[0][0:MAX_HITS]), ",".join(hits[1][0:MAX_HITS])  
        if len(dstr) == 0: dstr = '-' 
        if len(ustr) == 0: ustr = '-' 
        self.ax = axes[1]  
        self.add_row([ustr], X=(0,100), Y=(0,100), FS=7, WIDTHS=[100], STYLE=self.STYLE)
        self.ax = axes[2]  
        self.add_row([dstr], X=(0,100), Y=(0,100), FS=7, WIDTHS=[100], STYLE=self.STYLE)
        for ax in axes: ax.axis('off') 


    


    def initialize_rare(self,axes, c1 = 'gray', c2 = 'red', fs1=9, fs2=7, fs3 = 18):
        h2 = ['DRAGEN-POS','rsId','MAF','Type','Genes(s)'] 
        self.snp_widths = [28,20,13,21,18] 
        for i,ax in enumerate(axes): 
            self.ax = ax 
            if i == 0:   self.add_row(h2, COLORS=[c2 for h in h2],X=(0,100), Y=(0,100), FS=7, WIDTHS=self.snp_widths, STYLE='HORZ',TITLE=True)
            elif i == 1: self.add_row(['Traits with Genome-Wide Sig-Effects'], COLORS=[c2],X=(0,100), Y=(0,100), FS=7, WIDTHS=[100], STYLE='HORZ', TITLE=True)
            elif i == 2: self.add_row(['ClinVar Phenotypes'], COLORS=[c2],X=(0,100), Y=(0,100), FS=7, WIDTHS=[100], STYLE='HORZ', TITLE=True)
            self.ax.axis('off') 
        #axes[1].set_title('Annotated Rare Variants', ha = 'center', fontsize = 8, fontweight='bold',y=0.95,x=0.05) 
        return self 
    
    def initialize_burden(self,axes, c1 = 'gray', c2 = 'red', fs1=9, fs2=7, fs3 = 18):
        h2 = ['DRAGEN-ID','Genes(s)'] 
        self.snp_widths = [70,30] 
        for i,ax in enumerate(axes): 
            self.ax = ax 
            if i == 0:   self.add_row(h2, COLORS=[c2 for h in h2],X=(0,100), Y=(0,100), FS=7, WIDTHS=self.snp_widths, STYLE='HORZ',TITLE=True)
            elif i == 1: self.add_row(['Traits with Genome-Wide Sig-Effects'], COLORS=[c2],X=(0,100), Y=(0,100), FS=7, WIDTHS=[100], STYLE='HORZ', TITLE=True)
            elif i == 2: self.add_row(['ClinVar Phenotypes'], COLORS=[c2],X=(0,100), Y=(0,100), FS=7, WIDTHS=[100], STYLE='HORZ', TITLE=True)
            self.ax.axis('off') 
        #axes[1].set_title('Annotated Burden Variants', ha = 'center', fontsize = 8, fontweight='bold',x=0.5, y=0.90) 
        return self


    def initialize_unannotated_burden(self,axes, c1 = 'gray', c2 = 'red', fs1=9, fs2=7, fs3 = 18):
        h2 = ['DRAGEN-ID','Genes(s)'] 
        self.snp_widths = [70,30] 
        for i,ax in enumerate(axes): 
            self.ax = ax 
            if i == 0:   self.add_row(h2, COLORS=[c2 for h in h2],X=(0,100), Y=(0,100), FS=7, WIDTHS=self.snp_widths, STYLE='HORZ',TITLE=True)
            elif i == 1: self.add_row(['Traits with GWS Increasing Alleles'], COLORS=[c2],X=(0,100), Y=(0,100), FS=7, WIDTHS=[100], STYLE='HORZ', TITLE=True)
            elif i == 2: self.add_row(['Traits with GWS Descreasing Alleles'], COLORS=[c2],X=(0,100), Y=(0,100), FS=7, WIDTHS=[100], STYLE='HORZ', TITLE=True)
            self.ax.axis('off') 
        
        #axes[1].set_title('Unannotated Burden Variants', ha = 'center', fontsize = 8, fontweight='bold',x=0.05, y=0.90) 
        return self



