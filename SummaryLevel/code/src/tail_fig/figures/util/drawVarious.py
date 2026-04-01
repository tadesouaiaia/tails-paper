from Util import * 




def draw_square(ax,x1,x2,y1,y2,clr='k',lw=0.4): 
    ax.plot([x1,x2],[y1,y1],clip_on=False,color=clr,lw=lw) 
    ax.plot([x1,x2],[y2,y2],clip_on=False,color=clr,lw=lw)
    ax.plot([x1,x1],[y1,y2],clip_on=False,color=clr,lw=lw)
    ax.plot([x2,x2],[y1,y2],clip_on=False,color=clr,lw=lw)


def draw_blank(ax): 
    draw_square(ax, 0,1,0,1,lw=1) 
    rect = Rectangle((0, 0 ), 1,1,facecolor='lightgrey', edgecolor='k', linewidth=1, alpha=0.15) 
    ax.add_patch(rect)
    lms = AxLims(ax, xt=[], yt=[], xLim=[0,1], yLim=[0,1]) 
    return


def add_scatter_corr(ax, X, Y, fs=9, clr ='k', lw=0.8, INTERCEPT=True, EXTEND=0, REP=None): 
    
    lms = AxLims(ax) 
    x1, x2 = lms.xMin, lms.xMax 
    if x2 < EXTEND: x2 = EXTEND
    R,pv = stats.pearsonr(X,Y)
    if INTERCEPT: 
        lr = stats.linregress(X,Y)
        b0, b1, be  =  lr.intercept, lr.slope , lr.stderr*1
        yP = [b0 + x1*b1, b0+ x2*b1] 
    else: 
        model = statsmodels.api.OLS(endog=Y, exog=X).fit()
        beta = model.params[0]
        yP = [x1*beta, x2*beta] 
    
    
    ax.plot([x1, x2],yP, color=clr,linestyle='--',lw=lw, zorder=0)



    rstr = str(round(R,2))
    if R > 0 and len(rstr) == 3: rstr += '0'
    try:
        a,b = str(pv).split('e')
        pstr = '$P='+a.split('.')[0]+' \\times 10^{'+b+'}$'
    except: 
        if pv < 0.001:
            try:
                pm, z= str(pv).split('.')[-1], 0
                while pm[z] == '0': z+= 1
                pstr = '$P='+str(pm[z])+' \\times 10^{-'+str(z+1)+'}$'
            except: pstr = '$P='+str(round(pv,5))+'$'
        else:  pstr = '$P='+str(round(pv,5))+'$'

    if REP is None:  
        ax.text(lms.xMin+lms.xHop, lms.yMax - lms.yHop, '$R= '+rstr+'$\n'+pstr, fontsize=fs, va='top', ha='left') 
    else: 
        if REP == 'rep':     ax.text(x2-lms.xStep,yP[-1]+lms.yHop,'$UKB$ $Repeated$\n($R='+rstr+'$)',ha='center',color=clr,fontsize=fs) 
        elif REP == 'poc':   ax.text(x2+1.9*lms.xStep,yP[-1]-lms.yHop*4,'$UKB$\n$Multi$-$Ancestry$\n($R='+rstr+'$)',ha='center',color=clr,fontsize=fs) 
        else:                ax.text(x2+2*lms.xHop,yP[-1]-lms.yStep*2,'$All$ $Of$ $Us$\n($R='+rstr+'$)',ha='center',color=clr,fontsize=fs) 
    return R,pv 









class AxLims:
    def __init__(self,ax, xLim = [], yLim = [], xt = None, yt = None, xlab = None, ylab = None, ystretch = 0, xstretch=0, fs = 9, CORNERS=[], COMMANDS=[]): 
        self.ax = ax 
        if len(xLim) == 2: ax.set_xlim(xLim[0], xLim[1]) 
        if len(yLim) == 2: ax.set_ylim(yLim[0], yLim[1]) 
        self.yMin, self.yMax = ax.get_ylim() 
        self.xMin, self.xMax = ax.get_xlim() 
        if type(ystretch) in [float,int]: 
            self.yMin -= ystretch * ((self.yMax-self.yMin)/10.0)
            self.yMax += ystretch * ((self.yMax-self.yMin)/10.0)
        else: 
            self.yMin -= ystretch[0] * ((self.yMax-self.yMin)/10.0)
            self.yMax += ystretch[-1] * ((self.yMax-self.yMin)/10.0)
        if type(xstretch) in [float,int]: 
            self.xMin -= xstretch * ((self.xMax-self.xMin)/10.0)
            self.xMax += xstretch * ((self.xMax-self.xMin)/10.0)
        else: 
            self.xMin -= xstretch[0] * ((self.xMax-self.xMin)/10.0)
            self.xMax += xstretch[-1] * ((self.xMax-self.xMin)/10.0)
        ax.set_xlim(self.xMin, self.xMax) 
        ax.set_ylim(self.yMin, self.yMax) 
        self.xRange, self.yRange = self.xMax - self.xMin, self.yMax - self.yMin 
        self.xStep, self.yStep, self.xHop, self.yHop= self.xRange/10.0, self.yRange / 10.0 , self.xRange/50.0, self.yRange/50.0
        self.xMid, self.yMid = self.xMin + self.xRange/2.0, self.yMin + self.yRange/2.0 
        

        if xt != None: ax.set_xticks(xt) 
        if yt != None: ax.set_yticks(yt) 
        if xlab != None: ax.set_xlabel(xlab, fontsize=fs) 
        if ylab != None: ax.set_ylabel(ylab, fontsize=fs) 

        for xx in CORNERS: 
            if len(xx) == 2: nloc,nstr,ns = xx[0].upper(), xx[1], fs 
            elif len(xx) == 3: nloc, nstr, ns = xx[0].upper(), xx[1], xx[2] 
            else:              continue
            if nloc == 'TOPLEFT': ax.text(self.xMin + self.xStep/10.0, self.yMax - self.yStep/10.0, nstr, ha='left', va='top', fontsize=ns)       
            elif nloc == 'TOPRIGHT': ax.text(self.xMax - self.xStep*0.5, self.yMax - self.yStep*1.5, nstr, ha='right', va='top', fontsize=ns)       
            elif nloc == 'BOTTOMRIGHT': ax.text(self.xMax - self.xStep/10.0, self.yMin + self.yStep/10.0, nstr, ha='right', va='bottom', fontsize=ns)       
            elif nloc == 'BOTTOMLEFT': ax.text(self.xMin + self.xStep/10.0, self.yMin + self.yStep/10.0, nstr, ha='left', va='bottom', fontsize=ns)       
            else: continue 
        for x in COMMANDS: 
            if x.upper() == 'NOSPINES': 
                  ax.spines[['top','right']].set_visible(False) 











