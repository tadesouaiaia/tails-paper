



class TailName: 
    def __init__(self, ti, basic, group): 
        self.ti, self.basic, self.group = ti, basic, group
        self.list  =  self.choose_list() 
        self.flat  =  self.choose_flat(" ".join([x.capitalize() for x in self.list])) 
        self.mini  =  self.choose_mini() 
        #self.index =  self.choose_index() 
        self.miami =  self.choose_miami() 
        #self.tall  =  self.choose_tall() 
        self.mini  =  self.choose_mini() 
        self.tiny  =  self.choose_tiny() 
        self.snp  =  self.choose_snp() 
        self.box   =  self.choose_box() 
        self.best  =  self.choose_best() 
        self.aou   = self.choose_aou(self.ti)  
        self.forest = self.choose_forest() 

        self.cornerStyle  =  self.choose_corner_style() 


    def choose_corner_style(self):  
        if self.ti == 30070: return 'Red Blood Cell\nDist. Width'
        if self.ti == 50: return 'Height' 
        elif self.ti in [30020, 20015]: return self.flat.split()[0]+'\n'+self.flat.split()[1]
        else:                           return self.flat 
        

    def choose_flat(self, cand): 
        if self.ti == 3761: return 'Age Hay Fever, Rhinitis or Eczema Diagnosed'
        if self.ti == 20156: return 'Duration To Complete Numeric Path'
        if self.ti == 20157: return 'Duration To Complete Alphanumeric Path'
        return cand










    def choose_list(self): 
        if self.ti == 30010: return ["Red","Blood","Cell","Count"]
        if self.ti == 3581: return ["Age","At","Menopause"]
        if self.ti == 20153: return ["Forced","Expiratory","Volume","In","1-second","Predicted"]
        if self.ti == 47: return ["Hand","Grip","Strength","(right)",]
        if self.ti == 20154: return ["Forced","Expiratory","Volume","In","1-second","Predicted","Percentage"]
        if self.ti == 23123: return ["Left","Arm","Fat","Percentage"] 
        if self.ti == 30070: return ["Red","Blood","Cell","Dist","Width"]
        if self.ti == 30750: return ["Glycated","Haemoglobin"]
        if self.ti == 30100: return ["Mean","Platelet","Volume"]
        if self.ti == 30000: return ["White","Blood","Cell","Count"]
        if self.ti == 3148: return  ["Heel","Bone","Mineral","Density"]
        if self.ti == 20151: return ["Forced","Vital","Capacity","Best","Measure"]
        if self.ti == 20150: return ["Forced","Expiratory","Volume","In","1-second","Best","Measure"]
        if self.ti == 20257: return ["Forced","Vital","Capacity","Z-score"]
        if self.ti == 20256: return ["Forced","Expiratory","Volume","In","1-second","Z-score"]
        if self.ti == 23115: return ["Left","Leg","Fat","Percentage"]
        if self.ti == 23107: return ["Right","Impedance","Of","Leg"]
        if self.ti == 23116: return ["Left","Leg","Fat","Mass"]
        if self.ti == 1070: return ["Time","Spent","Watching","Television"] 
        return self.basic.split('_') 

    

    def choose_box(self, maxLen = 25): 
        return self.mini
    

    def choose_best(self, maxLen = 25): 
        return self.basic 
    
    def choose_index(self, maxLen = 25): 
        if self.ti == 30070: return 'Red Blood Cell Dist Width'       
        if self.ti == 20015: return 'Sitting Height' 
        if self.ti == 30020: return 'Haemoglobin Concentration'                                                                                                                                                                                                 
        return self.flat 

    
    def choose_tiny(self): 
        if self.ti == 30070: return 'RBC DW' 
        if self.ti == 3581: return 'Menopause'
        if self.ti == 20151: return 'FVC' 
        return self.mini 

    def choose_snp(self): 
        
        if self.ti == 23099: return 'Body-Fat' 
        if self.ti == 30180: return 'Lymphocytes' 
        if self.ti == 30190: return 'Monocytes' 
        if self.ti == 30200: return 'Neutrophills'
        if self.ti == 30210: return 'Eosinophills'
        if self.ti == 30240: return 'Reticulocytes'


        if self.ti == 30070: return 'RBCDW'
        if self.ti == 30090: return 'Platelet Crit'
        if self.ti == 30260: return 'RT Vol'
        if self.ti == 30280: return 'RT Frac'
        if self.ti == 30270: return 'Cell Vol'
        if self.ti == 30860: return 'T-Protein'

        if self.ti == 30040: return "CP Vol" 
        if self.ti == 30050: return 'CP Heme' 
        if self.ti == 30060: return 'CP Heme' 

        return self.mini


    def choose_mini2(self):
        if self.ti == 46:    return    "Grip Strength" 
        if self.ti == 30060: return 'Mean CP Heme'  
        if self.ti == 77: return "HBU T-Score" 
        if self.ti == 3084: return "Heel BMD Manual Entry"
        if self.ti == 4105: return "Left Heel BMD" 
        if self.ti == 4106: return "Left Heel BMD TS" 
        if self.ti == 4124: return "Right Heel BMD" 
        if self.ti == 4125: return "Right Heel BMD TS" 
        if self.ti == 23433: return "Avg Hdl Diameter"
        if self.ti == 23432: return "Avg Ldl Diameter"
        if self.ti == 23431: return "Avg Vldl Diameter"
        if self.ti == 23484: return "Chol In Chylomicrons"
        if self.ti == 23561: return "Chol In Large Hdl"
        if self.ti == 23533: return "Chol In Large Ldl"
        if self.ti == 23498: return "Chol In Large Vldl"
        if self.ti == 23568: return "Chol In Medium Hdl"
        if self.ti == 23540: return "Chol In Medium Ldl"
        if self.ti == 23505: return "Chol In Medium Vldl"
        if self.ti == 23575: return "Chol In Small Hdl"
        if self.ti == 23547: return "Chol In Small Ldl"
        if self.ti == 23512: return "Chol In Small Vldl"
        if self.ti == 23554: return "Chol In Very Large Hdl"
        if self.ti == 23491: return "Chol In Very Large Vldl"
        if self.ti == 23519: return "Chol In Very Small Vldl"
        if self.ti == 23580: return "Chol to Lipids (C-And)"
        if self.ti == 23610: return "Chol to Lipids (Idl)"
        if self.ti == 23635: return "Chol to Lipids (L-Hdl)"
        if self.ti == 23615: return "Chol to Lipids (L-Ldl)"
        if self.ti == 23590: return "Chol to Lipids (L-Vldl)"
        if self.ti == 23640: return "Chol to Lipids (M-Hdl)"
        if self.ti == 23620: return "Chol to Lipids (M-Ldl)"
        if self.ti == 23595: return "Chol to Lipids (M-Vldl)"
        if self.ti == 23645: return "Chol to Lipids (S-Hdl)"
        if self.ti == 77: return "HBD UATS Manual Entry"
        if self.ti == 3882: return "Age At Oophorectomy"
        if self.ti == 3872: return "Age At Childbirth"
        if self.ti == 2754: return "Age At First Birth"
        if self.ti == 2764: return "Age At Last Birth"
        if self.ti == 2794: return "Age Started Contraceptive"
        if self.ti == 3680: return "Age Last Ate Meat"
        if self.ti == 2744: return "Child Birth Weight" 
        if self.ti == 1737: return "Childhood Sunburns" 
        if self.ti == 3084: return "Heel BMD Manual Entry"
        if self.ti == 78: return "Heel BMD T-score Automated"
        if self.ti == 3083: return "Heel QUI Manual Entry"
        if self.ti == 23129: return "FF Trunk Mass" 
        if self.ti == 23107: return "Leg Impedance" 
        if self.ti == 48:    return "Waist Circum" 
        if self.ti == 49:    return "Hip Circum" 
        if self.ti == 2714: return  "Menarche Age" 
        if self.ti == 2217: return  "Glasses Age" 
        if self.ti == 20159: return "SD Matches" 
        if self.ti == 3536: return  "HRT Age"
        if self.ti == 1050: return "Outdoor Time" 
        if self.ti == 845: return   "Education Age" 
        if self.ti == 30150: return "Eosinophills" 
        if self.ti == 30140: return "Neutrophills"
        if self.ti == 20157: return "Alphanum. Trail" 
        if self.ti == 30020: return 'Haemoglobin Conc.'                                                                                                                                                                                                 
        if self.ti == 30040: return "Mean CP Vol"
        if self.ti == 30260: return "Mean RT Vol"
        if self.ti == 30280: return "Imm. RT Frac"
        if self.ti == 30060: return "CP Heme Conc."
        if self.ti == 30050: return 'Mean CP Heme' 
        if self.ti == 30250: return "Reticulocytes" 
        if self.ti == 30270: return "Sphered Cell Vol"
        if self.ti == 30130: return "Monocytes" 
        if self.ti == 30010: return "RBCs" 
        if self.ti == 30120: return "Lymphocytes" 
        if self.ti == 30000: return "WBCs"
        if self.ti == 20016: return 'Fluid Intellect' 
        if self.ti == 30010: return 'RBC Count'
        if self.ti == 22501: return 'Year End Edu' 
        if self.ti == 30760: return 'HDL' 
        if self.ti == 50: return 'Height' 
        if self.ti == 30070: return 'RBC Dist. Width'
        if self.ti == 20023: return 'Match ID Time'
        if self.ti == 3148:  return 'Heel BMD' 
        if self.ti == 46:    return 'Hand Grip Strength' 
        if self.ti == 30280: return 'Imm. Reticulocyte Frac'
        if self.ti == 2139:  return 'First Sexual Intercourse'
        if self.ti == 23102:  return 'Water Mass' 
        if self.ti == 30100:  return 'Platelet Vol' 
        if self.ti == 21001:  return 'BMI' 
        if self.ti == 30000:  return 'WBC Count' 
        if self.ti == 2714:   return 'Age At Menarche'
        if self.ti == 3144:   return 'Heel BUA'  
        if self.ti == 30300:   return 'HLS Reticulocyte Count' 
        if self.ti == 20150: return 'FEV Best' 
        if self.ti == 20151: return 'FVC Best'                                                                                                                                                                                                                         
        if self.ti == 30290: return "HLS Reticulocyte Vol"                                                                                                                                                                                                             
        if self.ti == 20256: return "FEV Z-score"                                                                                                                                                                                                                         
        if self.ti == 20257: return "FVC Z-score" 
        if self.ti == 30770: return "IGF-1" 
        if self.ti == 30830: return "SHBG" 
        if self.ti == 20258: return 'FEV/FVC Z-score'
        if self.ti == 1070: return 'TV Watching' 
        if self.ti == 30110: return 'Platelet Dist Width' 
        if self.ti == 26414: return 'Education Score' 
        if self.ti == 21001: return 'BMI' 
        if self.ti == 23107: return 'Right Leg Impedance' 
        if self.ti == 20019: return 'L-SRT' 
        if self.ti == 20127: return 'Neuroticism' 
        if self.ti == 20154: return 'Pred FEV %' 
        if self.ti == 20156: return 'Numeric Trail'  # numeric 
        if self.ti == 20157: return 'Alphanumeric Trail' 
        if self.ti == 1050: return 'Summer Outdoor Time'
        if self.ti == 1060: return 'Winter Outdoor Time' 
        if self.ti == 136: return   'Operations' # 0.11702 0
        if self.ti == 20023: return 'Match Time'
        if self.ti == 20159: return 'Correct SD Matches' 
        if self.ti == 20195: return 'Attempted SD Matches' 
        if self.ti == 20434: return 'Age at Last Depression' 
        if self.ti == 22033: return 'Days Activity' 
        if self.ti == 22034: return 'Minutes Activity' # 0 0
        if self.ti == 22037: return 'Walking Minutes' 
        if self.ti == 22038: return 'Moderate Activity Minutes' 
        if self.ti == 22040: return 'All Activity Minutes' 
        if self.ti == 30750: return 'Glycated Haem.' 
        if self.ti == 22599: return 'Jobs Held' 
        if self.ti == 23101: return 'Lean Body Mass' 
        if self.ti == 23105: return 'BMR' 
        if self.ti == 23106: return 'Body Impedance' 
        if self.ti == 26427: return 'Dep Idx (Scotland)' 
        if self.ti == 26428: return 'Income Score (Scotland)'
        if self.ti == 26431: return 'Education Score (Scotland)' 
        if self.ti == 26433: return 'Access Score (Scotland)' 
        if self.ti == 2714: return 'Age At Menarche' # 0.1807 0
        if self.ti == 2824: return 'Age At Hysterectomy' # 0 0
        if self.ti == 2966: return 'Age HPD Diagnosed' # 0 0
        if self.ti == 3: return    'Interview Duration' 
        if self.ti == 3143: return 'Ankle Spacing'
        if self.ti == 3146: return 'Sound Thru Heel'
        if self.ti == 3536: return 'Age Started HRT' 
        if self.ti == 3546: return 'Age Used HRT' 
        if self.ti == 3581: return 'Menopause Age'
        if self.ti == 3761: return 'Age Hay Fever' # 0 0 negative
        if self.ti == 3786: return 'Age of Asthma'
        if self.ti == 3872: return 'Age At Birth of Child' 
        if self.ti == 4120: return 'R-Heel BUA' 
        if self.ti == 4195: return 'PW Reflection Idx' 
        if self.ti == 4196: return 'PW P2P Time' 
        if self.ti == 4198: return 'PW Position' 
        if self.ti == 4199: return 'PW Notch' 
        if self.ti == 5256: return 'R Corneal Hys'
        if self.ti == 5257: return 'R Corneal Res.' 
        if self.ti == 5265: return 'L Corneal Res' 
        if self.ti == 6033: return 'Max Heart Rate' 
        if self.ti == 6032: return 'Max Work Load' 
        if self.ti == 23110: return 'Arm Impedance' 
        if self.ti == 20128: return "Int. Questions Attempted" 
        if self.ti == 20248: return "Errors On Alphanumeric Path"
        if self.ti == 23411: return "Phospholipids In Lipoprotein"
        if self.ti == 23441: return "Apolipoprotein B:A1 Ratio" 
        if self.ti == 23451: return "Omega-3 %" 
        if self.ti == 23452: return "Omega-6 %" 
        if self.ti == 23453: return "Polyunsaturated %" 
        if self.ti == 23454: return "Monounsaturated %" 
        if self.ti == 23455: return "Saturated Fatty Acids %" 
        if self.ti == 23457: return "Docosahexaenoic Acids %" 
        if self.ti == 23458: return "Polyunsaturated Fatty Acid Ratio" 
        if self.ti == 23459: return "Omega-6 Ratio" 
        if self.ti == 23464: return "BCAA Conc" 
        if self.ti == 23481: return "Chylomicrons and Vldl" 
        if self.ti == 23482: return "Lipids In Chylomicrons" 
        if self.ti == 23483: return "Phospholipids In Chylomicrons" #And Extremely Large Vldl"
        if self.ti == 23484: return "Cholesterol In Chylomicrons" #And Extremely Large Vldl"
        if self.ti == 23485: return "Cholesteryl Esters In Chylomicrons" # And Extremely Large Vldl"
        if self.ti == 23486: return "Free Cholesterol In Chylomicrons" # And Extremely Large Vldl"
        if self.ti == 23487: return "Triglycerides In Chylomicrons" # And Extremely Large Vldl"
        if self.ti == 4200: return "Shoulder Pos On Pulse Waveform"#
        if self.ti == 4283: return "Rounds Of Numeric Memory Test" #Performed"
        if self.ti == 5386: return "Unenthusiastic Episodes"
        if self.ti == 77: return "HBD UATS Manual Entry"
        if self.ti == 23423: return "Lipids In Lipoprotein Particles"
        if self.ti == 23435: return "Triglycerides-Phosphoglycerides Ratio"
        if self.ti == 23456: return "Linoleic Acid %"
        if self.ti == 23492: return "Cholesteryl Esters In L-Vldl"
        if self.ti == 23520: return "Cholesteryl Esters In S-Vldl"
        if self.ti == 23555: return "Cholesteryl Esters In Hdl"
        if self.ti == 3085: return "Heel Broadband UA"
        if self.ti == 3086: return "Speed Of Sound Through Heel" 
        nl = [] 
        for x in self.miami.split(): 
            if x == 'Volume': nl.append('Vol') 
            elif x[0:4] == 'Perc': nl.append('%') 
            elif x[0:4] == 'Conc': nl.append('Conc') 
            else: nl.append(x) 
        
        fn = " ".join(nl) 
        if len(fn) <= 20: 
            return fn
        fn = fn.split('(')[0] 
        if len(fn) < 20: 
            return fn 
        if len(fn.split('To Total Lipids In')) == 2: 
            a,b = fn.split(' To Total Lipids In ')[0],fn.split(' To Total Lipids In ')[1].split()[0:2] 
            if '%' not in b: fn = a+' to Lipids ('+b[0][0].upper()+'-'+b[1]+')'  
            else:            fn = a+' to Lipids ('+b[0]+')'  
            return fn 
        if len(fn) < 31 and len(fn)>20: 
            print('if self.ti == '+str(self.ti)+': return \"'+self.miami+'\"') 
        return fn 




    def choose_miami(self, maxLen = 25): 
        
        if self.ti == 4122: return 'Sound Through Right Heel'
        if self.ti == 4101: return 'Heel Broadband UA'
        if self.ti == 23113: return 'Right Leg Lean Mass'
        if self.ti == 30060: return 'Mean Corpuscular Heme'                                                                                                                                                                                                            
        if self.ti == 20153: return 'Predicted FEV' 
        if self.ti == 20154: return 'Predicted FEV %' 
        if self.ti == 47: return 'Right Hand Grip Strength'
        if self.ti == 45: return 'Hand Grip Strength'
        if self.ti == 2217: return 'Age Wearing Glasses' 
        if self.ti == 20023: return 'Match Identification Time' 
        if self.ti == 23115: return 'Leg Fat %' 
        if self.ti == 845: return "Age Complete Edu "                                                                                                                                                                                                            
        if self.ti == 20150: return 'FEV Best' 
        if self.ti == 20151: return 'FVC Best'                                                                                                                                                                                                                         
        if self.ti == 30290: return "HLS Reticulocyte Vol"                                                                                                                                                                                                             
        if self.ti == 20256: return "FEV Z-score"                                                                                                                                                                                                                         
        if self.ti == 20257: return "FVC Z-score" 
        if self.ti == 30770: return "IGF-1" 
        if self.ti == 30830: return "SHBG" 
        if self.ti == 20258: return 'FEV/FVC Z-score'
        if self.ti == 1070: return 'TV Watching' 
        if self.ti == 30110: return 'Platelet Dist Width' 
        if self.ti == 26414: return 'Education Score' 
        if self.ti == 21001: return 'BMI' 
        if self.ti == 23106: return 'Whole Body Impedance' 
        if self.ti == 23107: return 'Right Leg Impedance' 
        return self.flat 
        

    def choose_aou(self, x):
        if x == 30600: return  'Albumin [M/v] in Serum or Plasma'
        elif x == 30680: return  'Calcium [M/v] in Serum or Plasma'
        elif x == 30690: return  'Cholesterol [M/v] in Serum or Plasma' #| 145,940   
        elif x == 30700: return  'Creatinine [M/v] in Serum or Plasma'# | 202,520   
        elif x == 30150: return  'Eosinophils [#/v] in Blood by AC' # 151,120  
        elif x == 30210: return  'Eosinophils/100 leukocytes in Blood by AC' # | 152,340  
        elif x == 30030: return  'Hematocrit [Volume Fraction] of Blood by AC' # | 182,400 
        elif x == 30020: return  'Hemoglobin [M/v] in Blood' # | 199,540     
        elif x == 30760: return  'Cholesterol in HDL [Mass/volume] in Serum or Plasma' # | 140,800
        elif x == 30120: return  'Lymphocytes [#/v] in Blood by AC' # | 155,840  
        elif x == 30180: return  'Lymphocytes [#/v] in Blood by AC' # | 155,840  
        elif x == 30060: return  'Hemoglobin [M/v] in Blood' # | 199,540     
        elif x == 30100: return  'Platelet mean volume [Entitic volume] in Blood by AC' # |
        elif x == 30130: return  'Monocytes [#/v] in Blood by Automated count' # | 148,600  
        elif x == 30140: return  'Neutrophils [#/v] in Blood by Automated count' # | 155,120  
        elif x == 30200: return  'Neutrophils/100 leukocytes in Blood by AC' # | 124,760  
        elif x == 30810: return  'Phosphate [Mass/v] in Serum or Plasma' # | 81,700   
        elif x == 30080: return  'Platelets [#/v] in Blood by AC' # | 189,460  
        elif x == 30010: return  'Erythrocytes [#/v] in Blood by AC' # | 196,740  
        elif x == 30530: return  'Sodium [Moles/v] in Urine' #  | 10,900     
        elif x == 30850: return  'Testosterone [M/v] in Serum or Plasma' # | 17,860   
        elif x == 30860: return  'Protein [M/v] in Serum or Plasma' #  | 191,440   
        elif x == 30870: return  'Triglycerides [M/v] in Serum or Plasma' # | 142,360   
        elif x == 30670: return  'Urea nitrogen [M/v] in Serum or Plasma' #  | 204,300  
        elif x == 30890: return  '25-hydroxyvitamin D3 [M/v] in Serum or Plasma' # | 63,180  
        elif x == 30000: return  'Leukocytes [#/v] in Blood by AC' #  | 191,860  elif x == 30600: 
        elif x == 21001: return  'BMI-mean'
        elif x == 50: return  'Height-mean'
        elif x == 30750: return 'Hemoglobin A1c/Hemoglobin.total in Blood'
        elif x == 30090: return 'Platelets [#/v] in Blood by Automated count'
        elif x == 30190: return 'Monocytes [#/v] in Blood by Automated count'
        elif x == 30070: return 'Erythrocyte distribution width [Ratio] by AC'
        elif x == 49:    return 'Hip Circumference (Mean)'
        elif x == 48:    return 'Waist Circumference (Mean)'
        elif x == 21002:    return 'Weight (Mean)'
        elif x == 30240:   return 'Reticulocytes [#/volume] in Blood'
        elif x == 4194:    return 'Computed heart rate (mean)'
        #print('wtf', x) 
        return 'NA'




    def choose_tall(self, maxLen = 15): 
        
        
        if self.ti == 20023: return 'Match\nIdentification\nTime' 
        if self.ti == 22501: return 'Year Ended\nFull Time\nEducation'
        if self.ti == 23099: return 'Body Fat\nPercent'
        if self.ti == 21001: return 'BMI' 
        if len(self.miami) < maxLen: return self.miami 
        cands = self.miami.split() 

        if len(cands) == 2: return cands[0]+'\n'+cands[1] 
        else:
            nl, tl = [cands[0]],len(cands[0])   
            for i,c in enumerate(cands[1::]): 
                if tl > 8: 
                    nl.append('\n'+c) 
                    tl = len(c) 
                else: 
                    nl.append(c) 
                    tl += len(c) 

        return " ".join(nl) 


        return self.miami

    
    def choose_forest(self): 
        return self.mini 











    def choose_mini(self):
        if self.ti == 46: return "Grip Strength" 
        if self.ti == 47: return "Grip Strength"
        if self.ti == 48: return "Waist Circum" 
        if self.ti == 49: return "Hip Circum" 
        if self.ti == 50: return 'Height' 
        if self.ti == 51: return "Seated height"
        if self.ti == 77: return "HBU T-Score" 
        if self.ti == 78: return "Heel BMD TS" 
        if self.ti == 845: return "Edu Age" 
        if self.ti == 1050: return "Outdoor Time" 
        if self.ti == 1070: return 'TV Watching' 
        if self.ti == 1080: return "Computer Time"
        if self.ti == 1160: return "Sleep duration"
        if self.ti == 1309: return "Fresh fruit intake"
        if self.ti == 1458: return "Cereal intake"
        if self.ti == 1528: return "Water intake"
        if self.ti == 1737: return "Childhood Sunburns" 
        if self.ti == 2139: return 'First Sexual' 
        if self.ti == 2149: return "Sexual Partners"
        if self.ti == 2217: return "Glasses Age" 
        if self.ti == 2714: return "Menarche Age" 
        if self.ti == 2744: return "Child Birth Weight" 
        if self.ti == 2754: return "Age At First Birth" 
        if self.ti == 2764: return "Age At Last Birth" 
        if self.ti == 2794: return "Contraceptive Age" 
        if self.ti == 2824: return 'Hysterectomy Age' 
        if self.ti == 3083: return "Heel QUI Manual Entry" 
        if self.ti == 3084: return "Heel BMD ME" 
        if self.ti == 3085: return "Heel Broadband UA" 
        if self.ti == 3086: return "Speed Of Sound Through Heel" 
        if self.ti == 3143: return 'Ankle Spacing' 
        if self.ti == 3144: return 'Heel BUA' 
        if self.ti == 3146: return 'Sound Thru Heel' 
        if self.ti == 3147: return "Heel QUI-DE" 
        if self.ti == 3148: return 'Heel BMD' 
        if self.ti == 3536: return "HRT Age" 
        if self.ti == 3581: return 'Menopause Age' 
        if self.ti == 3680: return "Age Last Ate Meat" 
        if self.ti == 3710: return "Length Of Menstrual Cycle"
        if self.ti == 3761: return 'Age Hay Fever' 
        if self.ti == 3786: return 'Age of Asthma' 
        if self.ti == 3872: return "Age At Childbirth" 
        if self.ti == 3882: return "Age At Oophorectomy" 
        if self.ti == 4100: return "Ankle spacing (L)"
        if self.ti == 4101: return "L Heel BUA" 
        if self.ti == 4103: return "Sound Through Heel (L)"
        if self.ti == 4104: return "L Heel QUI-DE"
        if self.ti == 4105: return "Left Heel BMD" 
        if self.ti == 4106: return "Left Heel BMD TS" 
        if self.ti == 4119: return "Ankle spacing (R)"
        if self.ti == 4120: return 'R-Heel BUA' 
        if self.ti == 4122: return "Sound Through Heel (R)"
        if self.ti == 4123: return "R Heel QUI-DE" 
        if self.ti == 4124: return "Right Heel BMD" 
        if self.ti == 4125: return "Right Heel BMD TS" 
        if self.ti == 4194: return "Pulse Rate"
        if self.ti == 4198: return 'PW Position' 
        if self.ti == 4199: return 'PW Notch' 
        if self.ti == 4200: return "Shoulder Pos On Pulse Waveform" 
        if self.ti == 4283: return "Numeric Memory Rounds"
        if self.ti == 4288: return "Time To Answer"
        if self.ti == 4290: return "Duration Screen Displayed"
        if self.ti == 5386: return "Unenthusiastic Episodes" 
        if self.ti == 6032: return 'Max Work Load' 
        if self.ti == 6033: return 'Max Heart Rate' 
        if self.ti == 20015: return "Sitting Height"
        if self.ti == 20016: return 'Fluid Intellect' 
        if self.ti == 20022: return "Birth Weight"
        if self.ti == 20023: return 'Match Time' 
        if self.ti == 20127: return 'Neuroticism' 
        if self.ti == 20128: return "Int. Questions Attempted" 
        if self.ti == 20150: return 'FEV Best' 
        if self.ti == 20151: return 'FVC Best' 
        if self.ti == 20153: return "FEV1 Pred" 
        if self.ti == 20154: return 'Pred FEV %' 
        if self.ti == 20156: return 'Numeric Trail' 
        if self.ti == 20157: return "Alphanum. Trail" 
        if self.ti == 20159: return "SD Matches" 
        if self.ti == 20195: return 'Attempted SD Matches' 
        if self.ti == 20240: return "Digits Remembered" 
        if self.ti == 20248: return "Alphanumeric Errors" 
        if self.ti == 20256: return "FEV Z-score" 
        if self.ti == 20257: return "FVC Z-score" 
        if self.ti == 20258: return 'FEV/FVC Z-score' 
        if self.ti == 21001: return 'BMI' 
        if self.ti == 21002: return "Weight"
        if self.ti == 23099: return "Body Fat %"
        if self.ti == 23100: return "Whole body fat mass"
        if self.ti == 23101: return 'Lean Body Mass' 
        if self.ti == 23102: return 'Water Mass' 
        if self.ti == 23105: return 'BMR' 
        if self.ti == 23106: return 'Body Impedance' 
        if self.ti == 23107: return "Leg Impedance" 
        if self.ti == 23108: return "Impedance Of Leg "
        if self.ti == 23109: return "Impedance Of Arm "
        if self.ti == 23110: return 'Arm Impedance' 
        if self.ti == 23111: return "Leg fat percentage (right)"
        if self.ti == 23112: return "Leg fat mass (right)"
        if self.ti == 23113: return "Leg fat-free mass (right)"
        if self.ti == 23114: return "Leg Predicted Mass "
        if self.ti == 23115: return "Leg Fat %"
        if self.ti == 23116: return "Leg fat mass (left)"
        if self.ti == 23117: return "Leg Fat-free Mass "
        if self.ti == 23118: return "Leg Predicted Mass "
        if self.ti == 23119: return "Arm Fat %"
        if self.ti == 23120: return "Arm Fat Mass"
        if self.ti == 23121: return "Arm FF Mass"
        if self.ti == 23122: return "Arm Predicted Mass "
        if self.ti == 23123: return "Arm fat percentage (left)"
        if self.ti == 23124: return "Arm fat mass (left)"
        if self.ti == 23125: return "Arm Fat-free Mass "
        if self.ti == 23126: return "Arm Predicted Mass "
        if self.ti == 23127: return "Trunk fat percentage"
        if self.ti == 23128: return "Trunk fat mass"
        if self.ti == 23129: return "FF Trunk Mass" 
        if self.ti == 23130: return "Trunk predicted mass"
        if self.ti == 23400: return "Total Cholesterol"
        if self.ti == 23401: return "Total Cholesterol Minus Hdl-c"
        if self.ti == 23402: return "Remnant Cholesterol" 
        if self.ti == 23403: return "VLDL Cholesterol"
        if self.ti == 23404: return "Clinical Ldl Cholesterol"
        if self.ti == 23405: return "LDL Cholesterol"
        if self.ti == 23406: return "HDL Cholesterol"
        if self.ti == 23407: return "Total Triglycerides"
        if self.ti == 23408: return "Triglycerides In Vldl"
        if self.ti == 23409: return "Triglycerides in LDL"
        if self.ti == 23410: return "Triglycerides in HDL"
        if self.ti == 23411: return "Phospholipids In Lipoprotein" 
        if self.ti == 23412: return "Phospholipids In Vldl"
        if self.ti == 23413: return "Phospholipids in LDL"
        if self.ti == 23414: return "Phospholipids in HDL"
        if self.ti == 23415: return "Total Esterified Cholesterol"
        if self.ti == 23416: return "Cholesteryl Esters In Vldl"
        if self.ti == 23417: return "Cholesteryl Esters In Ldl"
        if self.ti == 23418: return "Cholesteryl Esters In Hdl"
        if self.ti == 23419: return "Total Free Cholesterol"
        if self.ti == 23420: return "Free Cholesterol In Vldl"
        if self.ti == 23421: return "Free Cholesterol In Ldl"
        if self.ti == 23422: return "Free Cholesterol In Hdl"
        if self.ti == 23423: return "Lipids In Lipoprotein Particles" 
        if self.ti == 23424: return "Total Lipids in VLDL"
        if self.ti == 23425: return "Total Lipids in LDL"
        if self.ti == 23426: return "Total Lipids in HDL"
        if self.ti == 23427: return "Lipoprotein Conc"
        if self.ti == 23428: return "Concentration Of Vldl Particles"
        if self.ti == 23429: return "Concentration Of Ldl Particles"
        if self.ti == 23430: return "Concentration Of Hdl Particles"
        if self.ti == 23431: return "Avg Vldl Diameter" 
        if self.ti == 23432: return "Avg Ldl Diameter" 
        if self.ti == 23433: return "Avg Hdl Diameter" 
        if self.ti == 23434: return "Phosphoglycerides"
        if self.ti == 23435: return "Triglycerides-Phosphoglycerides Ratio" 
        if self.ti == 23436: return "Total Cholines"
        if self.ti == 23437: return "Phosphatidylcholines"
        if self.ti == 23438: return "Sphingomyelins"
        if self.ti == 23440: return "Apolipoprotein A1"
        if self.ti == 23441: return "Apolipoprotein B:A1 Ratio" 
        if self.ti == 23442: return "Total Fatty Acids"
        if self.ti == 23443: return "Degree Of Unsaturation"
        if self.ti == 23444: return "Omega-3 Fatty Acids"
        if self.ti == 23445: return "Omega-6 Fatty Acids"
        if self.ti == 23446: return "Polyunsaturated Fatty Acids"
        if self.ti == 23447: return "Monounsaturated Fatty Acids"
        if self.ti == 23448: return "Saturated Fatty Acids"
        if self.ti == 23449: return "Linoleic Acid"
        if self.ti == 23450: return "Docosahexaenoic Acid"
        if self.ti == 23451: return "Omega-3 %" 
        if self.ti == 23452: return "Omega-6 %" 
        if self.ti == 23453: return "Polyunsaturated %" 
        if self.ti == 23454: return "Monounsaturated %" 
        if self.ti == 23455: return "Saturated Fatty Acids %" 
        if self.ti == 23456: return "Linoleic Acid %" 
        if self.ti == 23457: return "Docosahexaenoic Acids %" 
        if self.ti == 23458: return "Polyunsaturated Fatty Acid Ratio" 
        if self.ti == 23459: return "Omega-6 Ratio" 
        if self.ti == 23460: return "Alanine"
        if self.ti == 23461: return "Glutamine"
        if self.ti == 23462: return "Glycine"
        if self.ti == 23464: return "BCAA Conc" 
        if self.ti == 23466: return "Leucine"
        if self.ti == 23467: return "Valine"
        if self.ti == 23469: return "Tyrosine"
        if self.ti == 23473: return "Citrate"
        if self.ti == 23480: return "Glycoprotein Acetyls"
        if self.ti == 23481: return "Chylomicrons and Vldl" 
        if self.ti == 23482: return "Lipids In Chylomicrons" 
        if self.ti == 23483: return "Phospholipids In Chylomicrons" 
        if self.ti == 23484: return "Chol In Chylomicrons" 
        if self.ti == 23485: return "Cholesteryl Esters In Chylomicrons" 
        if self.ti == 23486: return "Free Cholesterol In Chylomicrons" 
        if self.ti == 23487: return "Triglycerides In Chylomicrons" 
        if self.ti == 23488: return "Very Large Vldl Conc" 
        if self.ti == 23489: return "Total Lipids In Very Large Vldl"
        if self.ti == 23490: return "Phospholipids In Very Large Vldl"
        if self.ti == 23491: return "Chol In Very Large Vldl" 
        if self.ti == 23492: return "Cholesteryl Esters In L-Vldl" 
        if self.ti == 23493: return "Free Cholesterol In Very Large Vldl"
        if self.ti == 23494: return "Triglycerides In Very Large Vldl"
        if self.ti == 23495: return "Concentration Of Large Vldl Particles"
        if self.ti == 23496: return "Total Lipids In Large Vldl"
        if self.ti == 23497: return "Phospholipids In Large Vldl"
        if self.ti == 23498: return "Chol In Large Vldl" 
        if self.ti == 23499: return "Cholesteryl Esters In Large Vldl"
        if self.ti == 23500: return "Free Cholesterol In Large Vldl"
        if self.ti == 23501: return "Triglycerides In Large Vldl"
        if self.ti == 23502: return "Med Vldl Conc" 
        if self.ti == 23503: return "Total Lipids In Medium Vldl"
        if self.ti == 23504: return "Phospholipids In Medium Vldl"
        if self.ti == 23505: return "Chol In Medium Vldl" 
        if self.ti == 23506: return "Cholesteryl Esters In Medium Vldl"
        if self.ti == 23507: return "Free Cholesterol In Medium Vldl"
        if self.ti == 23508: return "Triglycerides In Medium Vldl"
        if self.ti == 23509: return "Concentration Of Small Vldl Particles"
        if self.ti == 23510: return "Total Lipids In Small Vldl"
        if self.ti == 23511: return "Phospholipids In Small Vldl"
        if self.ti == 23512: return "Chol In Small Vldl" 
        if self.ti == 23513: return "Cholesteryl Esters In Small Vldl"
        if self.ti == 23514: return "Free Cholesterol In Small Vldl"
        if self.ti == 23515: return "Triglycerides In Small Vldl"
        if self.ti == 23516: return "Very Small Vldl Conc" 
        if self.ti == 23517: return "Total Lipids In Very Small Vldl"
        if self.ti == 23518: return "Phospholipids In Very Small Vldl"
        if self.ti == 23519: return "Chol In Very Small Vldl" 
        if self.ti == 23520: return "Cholesteryl Esters In S-Vldl" 
        if self.ti == 23521: return "Free Cholesterol In Very Small Vldl"
        if self.ti == 23522: return "Triglycerides In Very Small Vldl"
        if self.ti == 23523: return "Concentration Of Idl Particles"
        if self.ti == 23524: return "Total Lipids in IDL"
        if self.ti == 23525: return "Phospholipids in IDL"
        if self.ti == 23526: return "Cholesterol in IDL"
        if self.ti == 23527: return "Cholesteryl Esters In Idl"
        if self.ti == 23528: return "Free Cholesterol In Idl"
        if self.ti == 23529: return "Triglycerides in IDL"
        if self.ti == 23530: return "Concentration Of Large Ldl Particles"
        if self.ti == 23531: return "Total Lipids In Large Ldl"
        if self.ti == 23532: return "Phospholipids In Large Ldl"
        if self.ti == 23533: return "Chol In Large Ldl" 
        if self.ti == 23534: return "Cholesteryl Esters In Large Ldl"
        if self.ti == 23535: return "Free Cholesterol In Large Ldl"
        if self.ti == 23536: return "Triglycerides In Large Ldl"
        if self.ti == 23537: return "Concentration Of Medium Ldl Particles"
        if self.ti == 23538: return "Total Lipids In Medium Ldl"
        if self.ti == 23539: return "Phospholipids In Medium Ldl"
        if self.ti == 23540: return "Chol In Medium Ldl" 
        if self.ti == 23541: return "Cholesteryl Esters In Medium Ldl"
        if self.ti == 23542: return "Free Cholesterol In Medium Ldl"
        if self.ti == 23543: return "Triglycerides In Medium Ldl"
        if self.ti == 23544: return "Concentration Of Small Ldl Particles"
        if self.ti == 23545: return "Total Lipids In Small Ldl"
        if self.ti == 23546: return "Phospholipids In Small Ldl"
        if self.ti == 23547: return "Chol In Small Ldl" 
        if self.ti == 23548: return "Cholesteryl Esters In Small Ldl"
        if self.ti == 23549: return "Free Cholesterol In Small Ldl"
        if self.ti == 23550: return "Triglycerides In Small Ldl"
        if self.ti == 23551: return "Very Large Hdl Conc" 
        if self.ti == 23552: return "Total Lipids In Very Large Hdl"
        if self.ti == 23553: return "Phospholipids In Very Large Hdl"
        if self.ti == 23554: return "Chol In Very Large Hdl" 
        if self.ti == 23555: return "Cholesteryl Esters In Hdl" 
        if self.ti == 23556: return "Free Cholesterol In Very Large Hdl"
        if self.ti == 23557: return "Triglycerides In Very Large Hdl"
        if self.ti == 23558: return "Concentration Of Large Hdl Particles"
        if self.ti == 23559: return "Total Lipids In Large Hdl"
        if self.ti == 23560: return "Phospholipids In Large Hdl"
        if self.ti == 23561: return "Chol In Large Hdl" 
        if self.ti == 23562: return "Cholesteryl Esters In Large Hdl"
        if self.ti == 23563: return "Free Cholesterol In Large Hdl"
        if self.ti == 23564: return "Triglycerides In Large Hdl"
        if self.ti == 23565: return "Concentration Of Medium Hdl Particles"
        if self.ti == 23566: return "Total Lipids In Medium Hdl"
        if self.ti == 23567: return "Phospholipids In Medium Hdl"
        if self.ti == 23568: return "Chol In Medium Hdl" 
        if self.ti == 23569: return "Cholesteryl Esters In Medium Hdl"
        if self.ti == 23570: return "Free Cholesterol In Medium Hdl"
        if self.ti == 23571: return "Triglycerides In Medium Hdl"
        if self.ti == 23572: return "Concentration Of Small Hdl Particles"
        if self.ti == 23573: return "Total Lipids In Small Hdl"
        if self.ti == 23574: return "Phospholipids In Small Hdl"
        if self.ti == 23575: return "Chol In Small Hdl" 
        if self.ti == 23576: return "Cholesteryl Esters In Small Hdl"
        if self.ti == 23577: return "Free Cholesterol In Small Hdl"
        if self.ti == 23578: return "Triglycerides In Small Hdl"
        if self.ti == 23579: return "Phospholipids to Lipids (C-And)"
        if self.ti == 23580: return "Chol to Lipids (C-And)" 
        if self.ti == 23581: return "Cholesteryl Esters to Lipids (C-And)"
        if self.ti == 23582: return "Free Cholesterol to Lipids (C-And)"
        if self.ti == 23583: return "Triglycerides to Lipids (C-And)"
        if self.ti == 23584: return "Phospholipids to Lipids (V-Large)"
        if self.ti == 23585: return "Cholesterol to Lipids (V-Large)"
        if self.ti == 23586: return "Cholesteryl Esters to Lipids (V-Large)"
        if self.ti == 23587: return "Free Cholesterol to Lipids (V-Large)"
        if self.ti == 23588: return "Triglycerides to Lipids (V-Large)"
        if self.ti == 23589: return "Phospholipids to Lipids (L-Vldl)"
        if self.ti == 23590: return "Chol to Lipids (L-Vldl)" 
        if self.ti == 23591: return "Cholesteryl Esters to Lipids (L-Vldl)"
        if self.ti == 23592: return "Free Cholesterol to Lipids (L-Vldl)"
        if self.ti == 23593: return "Triglycerides to Lipids (L-Vldl)"
        if self.ti == 23594: return "Phospholipids to Lipids (M-Vldl)"
        if self.ti == 23595: return "Chol to Lipids (M-Vldl)" 
        if self.ti == 23596: return "Cholesteryl Esters to Lipids (M-Vldl)"
        if self.ti == 23597: return "Free Cholesterol to Lipids (M-Vldl)"
        if self.ti == 23598: return "Triglycerides to Lipids (M-Vldl)"
        if self.ti == 23599: return "Phospholipids to Lipids (S-Vldl)"
        if self.ti == 23600: return "Cholesterol to Lipids (S-Vldl)"
        if self.ti == 23601: return "Cholesteryl Esters to Lipids (S-Vldl)"
        if self.ti == 23602: return "Free Cholesterol to Lipids (S-Vldl)"
        if self.ti == 23603: return "Triglycerides to Lipids (S-Vldl)"
        if self.ti == 23604: return "Phospholipids to Lipids (V-Small)"
        if self.ti == 23605: return "Cholesterol to Lipids (V-Small)"
        if self.ti == 23606: return "Cholesteryl Esters to Lipids (V-Small)"
        if self.ti == 23607: return "Free Cholesterol to Lipids (V-Small)"
        if self.ti == 23608: return "Triglycerides to Lipids (V-Small)"
        if self.ti == 23609: return "Phospholipids to Lipids (Idl)"
        if self.ti == 23610: return "Chol to Lipids (Idl)" 
        if self.ti == 23611: return "Cholesteryl Esters to Lipids (Idl)"
        if self.ti == 23612: return "Free Cholesterol to Lipids (Idl)"
        if self.ti == 23613: return "Triglycerides to Lipids (Idl)"
        if self.ti == 23614: return "Phospholipids to Lipids (L-Ldl)"
        if self.ti == 23615: return "Chol to Lipids (L-Ldl)" 
        if self.ti == 23616: return "Cholesteryl Esters to Lipids (L-Ldl)"
        if self.ti == 23617: return "Free Cholesterol to Lipids (L-Ldl)"
        if self.ti == 23618: return "Triglycerides to Lipids (L-Ldl)"
        if self.ti == 23619: return "Phospholipids to Lipids (M-Ldl)"
        if self.ti == 23620: return "Chol to Lipids (M-Ldl)" 
        if self.ti == 23621: return "Cholesteryl Esters to Lipids (M-Ldl)"
        if self.ti == 23622: return "Free Cholesterol to Lipids (M-Ldl)"
        if self.ti == 23623: return "Triglycerides to Lipids (M-Ldl)"
        if self.ti == 23624: return "Phospholipids to Lipids (S-Ldl)"
        if self.ti == 23625: return "Cholesterol to Lipids (S-Ldl)"
        if self.ti == 23626: return "Cholesteryl Esters to Lipids (S-Ldl)"
        if self.ti == 23627: return "Free Cholesterol to Lipids (S-Ldl)"
        if self.ti == 23628: return "Triglycerides to Lipids (S-Ldl)"
        if self.ti == 23629: return "Phospholipids to Lipids (V-Large)"
        if self.ti == 23630: return "Cholesterol to Lipids (V-Large)"
        if self.ti == 23631: return "Cholesteryl Esters to Lipids (V-Large)"
        if self.ti == 23632: return "Free Cholesterol to Lipids (V-Large)"
        if self.ti == 23633: return "Triglycerides to Lipids (V-Large)"
        if self.ti == 23634: return "Phospholipids to Lipids (L-Hdl)"
        if self.ti == 23635: return "Chol to Lipids (L-Hdl)" 
        if self.ti == 23636: return "Cholesteryl Esters to Lipids (L-Hdl)"
        if self.ti == 23637: return "Free Cholesterol to Lipids (L-Hdl)"
        if self.ti == 23638: return "Triglycerides to Lipids (L-Hdl)"
        if self.ti == 23639: return "Phospholipids to Lipids (M-Hdl)"
        if self.ti == 23640: return "Chol to Lipids (M-Hdl)" 
        if self.ti == 23641: return "Cholesteryl Esters to Lipids (M-Hdl)"
        if self.ti == 23642: return "Free Cholesterol to Lipids (M-Hdl)"
        if self.ti == 23643: return "Triglycerides to Lipids (M-Hdl)"
        if self.ti == 23644: return "Phospholipids to Lipids (S-Hdl)"
        if self.ti == 23645: return "Chol to Lipids (S-Hdl)" 
        if self.ti == 23646: return "Cholesteryl Esters to Lipids (S-Hdl)"
        if self.ti == 23647: return "Free Cholesterol to Lipids (S-Hdl)"
        if self.ti == 23648: return "Triglycerides to Lipids (S-Hdl)"
        if self.ti == 30000: return "WBCs" 
        if self.ti == 30010: return "RBCs" 
        if self.ti == 30020: return 'Haemoglobin Conc.' 
        if self.ti == 30030: return "Haematocrit %"
        if self.ti == 30040: return "Mean CP Vol" 
        if self.ti == 30050: return 'Mean CP Heme' 
        if self.ti == 30060: return 'Mean CP Heme' 
        if self.ti == 30070: return 'RBC Dist. Width' 
        if self.ti == 30080: return "Platelet count"
        if self.ti == 30090: return "Platelet Crit"
        if self.ti == 30100: return 'Platelet Vol' 
        if self.ti == 30110: return 'Platelet Dist Width' 
        if self.ti == 30120: return "Lymphocytes" 
        if self.ti == 30130: return "Monocytes" 
        if self.ti == 30140: return "Neutrophills" 
        if self.ti == 30150: return "Eosinophills" 
        if self.ti == 30180: return "Lymphocyte %"
        if self.ti == 30190: return "Monocyte %"
        if self.ti == 30200: return "Neutrophill %"
        if self.ti == 30210: return "Eosinophill %"
        if self.ti == 30240: return "Reticulocyte %"
        if self.ti == 30250: return "Reticulocytes" 
        if self.ti == 30260: return "Mean RT Vol" 
        if self.ti == 30270: return "Sphered Cell Vol" 
        if self.ti == 30280: return "Imm. RT Frac" 
        if self.ti == 30290: return "HLS Reticulocyte Vol" 
        if self.ti == 30300: return 'HLS Reticulocyte Count' 
        if self.ti == 30530: return "Sodium In Urine"
        if self.ti == 30600: return "Albumin"
        if self.ti == 30610: return "Alkaline phosphatase"
        if self.ti == 30620: return "Alanine Aminotransferase"
        if self.ti == 30630: return "Apolipoprotein A"
        if self.ti == 30640: return "Apolipoprotein B"
        if self.ti == 30650: return "Aspartate Aminotransferase"
        if self.ti == 30660: return "Direct bilirubin"
        if self.ti == 30670: return "Urea"
        if self.ti == 30680: return "Calcium"
        if self.ti == 30690: return "Cholesterol"
        if self.ti == 30700: return "Creatinine"
        if self.ti == 30710: return "C-reactive protein"
        if self.ti == 30720: return "Cystatin C"
        if self.ti == 30730: return "Gamma Glutamyltransferase"
        if self.ti == 30740: return "Glucose"
        if self.ti == 30750: return 'Glycated Haem.' 
        if self.ti == 30760: return 'HDL' 
        if self.ti == 30770: return "IGF-1" 
        if self.ti == 30780: return "LDL direct"
        if self.ti == 30790: return "Lipoprotein A"
        if self.ti == 30810: return "Phosphate"
        if self.ti == 30830: return "SHBG" 
        if self.ti == 30840: return "Total bilirubin"
        if self.ti == 30850: return "Testosterone"
        if self.ti == 30860: return "Total Protein"
        if self.ti == 30870: return "Triglycerides"
        if self.ti == 30880: return "Urate"
        if self.ti == 30890: return "Vitamin D"
        return self.flat



    def __repr__(self): return self.basic 
    
    def __str__(self): return self.basic 
    


