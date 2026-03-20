
process extract_quantitative_traits{
    module 'R/4.3.0'
    label 'normal'
    input:
        path(showcase)
    output:
        path "selected_fields", emit: nonblood
        path "blood_biochemistry", emit: blood
    script:
    """
    #!/usr/bin/env Rscript
    library(magrittr)
    library(data.table)
    dat <- fread("${showcase}") %>%
        # Only extract numerical traits
        .[ValueType %in% c("Integer", "Continuous")] %>%
        .[Participants > 10000] %>%
        .[Array == 1] %>%
        .[ItemType == "Data"] %>%
        # Exclude all reception related traits
        .[Category != 100024] %>%
        #Exclude all alcohol related traits
        .[Category != 100051] %>%
        #Exclude all smoking related traits
        .[Category != 100058] %>%
        # Exclude all genotyping QC metrics
        .[Category != 100313] %>%
        # Exclude traits that we are not interested in
        # e.g. country of birth & birth coordinates
        .[!FieldID %in% c(20115, 130, 129)] %>%
        #skip age of t2d, CAD, 
        .[!FieldID %in% c(2976, 3894)] %>%
        .[Stability %in% c("Accruing", "Complete")] %>%
        # If there are duplicate field name, only keep one with maximum number
        # of samples 
        .[, .SD[Participants == max(Participants)], Field] %>%
        .[,Field:=gsub(",","", Field)]
    dat[Category != 17518 & Category != 100081, c("Category", "FieldID", "Field", "Coding")] %>%
        fwrite(., "selected_fields")
    dat[Category == 17518 | Category == 100081, c("Category", "FieldID", "Field", "Coding")] %>%
        fwrite(., "blood_biochemistry")
    """
}


process extract_fecundity_from_sql{
     publishDir "result", mode: 'copy', overwrite: true
    label 'normal'
    input:
        path(db)
    output:
        path("Fecundity.csv")
    script:
    """
    echo "
    .mode csv
    .header on
    .output Fecundity.csv
    SELECT  s.sample_id AS FID,
            s.sample_id AS IID,
            sex.pheno AS Sex,
            age.pheno AS Age,
            birth.pheno AS YearOfBirth,
            fathered.pheno AS NumFathered,
            live.pheno AS NumLiveBirth,
            primiparous.pheno AS AgePrimiparous,
            still.pheno AS NumStillBirths,
            miscarriage.pheno AS NumMiscarriages,
            MAX(illness.pheno) AS Illness,
            SUM(adopted.Pheno) AS Adopted,
            ses.pheno AS SES,
            centre.pheno AS Centre,
            MAX(
                CASE WHEN edu.instance = 0 THEN 
                    CASE
                    WHEN
                        edu.pheno = 1
                    THEN 1
                    ELSE 0
                    END
                END
            ) AS Education,
            fatherAge.pheno AS FatherAge
    FROM    Participant s
            LEFT JOIN   f6138 edu ON 
                        s.sample_id=edu.sample_id 
            LEFT JOIN   f31 sex ON
                        s.sample_id=sex.sample_id
                        AND sex.instance = 0
            LEFT JOIN   f21003 age ON 
                        s.sample_id=age.sample_id 
                        AND age.instance = 0
            LEFT JOIN   f34 birth ON
                        s.sample_id=birth.sample_id
                        AND birth.instance = 0
            LEFT JOIN   f2405 fathered ON
                        s.sample_id=fathered.sample_id
                        AND fathered.instance = 0
            LEFT JOIN   f135 illness ON
                        s.sample_id = illness.sample_id
            LEFT JOIN   f2734 live ON
                        s.sample_id=live.sample_id
                        AND live.instance = 0
            LEFT JOIN   f3872 primiparous ON
                        s.sample_id=primiparous.sample_id
                        AND primiparous.instance = 0
            LEFT JOIN   f3829 still ON
                        s.sample_id=still.sample_id
                        AND still.instance = 0
            LEFT JOIN   f3839 miscarriage ON
                        s.sample_id=miscarriage.sample_id
                        AND miscarriage.instance = 0
            LEFT JOIN   f2946 fatherAge ON
                        s.sample_id = fatherAge.sample_id
                        AND fatherAge.instance = 0
            LEFT JOIN   f1767 adopted ON 
                        s.sample_id=adopted.sample_id 
                        AND adopted.pheno >=0
            LEFT JOIN   f189 ses ON 
                        s.sample_id=ses.sample_id 
                        AND ses.instance = 0
            LEFT JOIN   f54 centre ON
                        s.sample_id=centre.sample_id
                        AND centre.instance = 0
    WHERE s.withdrawn = 0
    GROUP BY s.sample_id;
    .quit
    " > sql
    sqlite3 ${db} < sql
    """
}



process adjust_fecundity{
    publishDir "result", mode: 'copy', overwrite: true
    label 'normal'
    module 'R/4.3.0'
    input: 
        path(fecundity)
        path(withdrawn)
    output:
        tuple   path("Paternal_age"),
                path("Fecundity.adj.csv"),
                path("NonCancerIllness.csv")
    script:
    """
    #!/usr/bin/env Rscript
    library(magrittr)
    library(data.table)
    withdrawn <- fread("${withdrawn}", header = F)
    dat <- fread("${fecundity}")[!IID %in% withdrawn[, V1]]
    dat[,c("FID", "IID", "Age", "SES", "Education", "Illness", "Age", "Sex", "Centre")] %>%
        na.omit %>%
        .[, IllnessEdu := resid(lm(Illness~SES+Age+Education, data=.SD))] %>%
        .[, Illness := resid(lm(Illness~SES+Age, data=.SD))] %>% 
        .[,c("FID", "IID", "Illness", "IllnessEdu", "Age", "Sex", "Centre")] %>%
        fwrite(., "NonCancerIllness.csv")

    paternal_age <-
        dat[, c("FID", "IID", "Age", "FatherAge", "Adopted", "Education", "SES")] %>%
        na.omit %>%
        .[Adopted == 0 & FatherAge > 0] %>%
        .[, FatherAge := FatherAge - Age] %>%
        .[FatherAge > 10] %>%
        setnames(., "FatherAge", "PaternalAge") %>%
        .[, PaternalAgeEdu :=  resid(lm(PaternalAge~Education, data=.SD))] %>% 
        #.[, PaternalAge := resid(lm(PaternalAge~SES, data=.SD))] %>%
        .[, c("FID", "IID", "PaternalAge", "PaternalAgeEdu")] %>%
        fwrite(., "Paternal_age")
        
    scale_this <- function(x) {
        (x - mean(x, na.rm = TRUE)) / sd(x, na.rm = TRUE)
    }
    mean_centre <- function(x) {
        x / mean(x, na.rm = TRUE)
    }
    phenotypes <- c(
        "NumFathered",
        "NumLiveBirth",
        "Fecundity",
        "AgePrimiparous",
        "NumStillBirths",
        "NumMiscarriages"
    )
    adjustments <- c(
        "Fathered.adj",
        "LiveBirth.adj",
        "Fecundity.adj",
        "AgePrimiparous.adj",
        "NumStillBirths.adj",
        "NumMiscarriages.adj"
    )

    # 1 is male, 0 is female
    male <- 1
    female <- 0
    fecundity <- dat %>%
        # define cohorts
        .[YearOfBirth <= 1965 & YearOfBirth >= 1934] %>%
        .[, Cohort := 0] %>%
        .[YearOfBirth >= 1956, Cohort := Cohort + 1] %>%
        .[YearOfBirth >= 1949, Cohort := Cohort + 1] %>%
        .[YearOfBirth >= 1943, Cohort := Cohort + 1] %>%
        .[(Age > 50 & Sex == male) | (Age > 45 & Sex == female)] %>%
        # Remove abnormal inputs
        .[Sex == female, NumFathered := NA] %>%
        .[Sex == male,
        c("NumLiveBirth",
            "AgePrimiparous",
            "NumStillBirths",
            "NumMiscarriages") := NA] %>%
        # Remove not answer, don't know
        .[NumFathered < 0, NumFathered := NA] %>%
        .[NumLiveBirth < 0, NumLiveBirth := NA] %>%
        .[AgePrimiparous < 0, AgePrimiparous := NA] %>%
        .[NumStillBirths < 0, NumStillBirths := NA] %>%
        .[NumMiscarriages < 0, NumMiscarriages := NA] %>%
        # Fecundity = live birth and number fathered
        .[, Fecundity := sum(NumLiveBirth, NumFathered, na.rm = T), by = IID] %>%
        # Divide by cohort mean
        .[, (adjustments) := lapply(.SD, mean_centre), .SDcols = phenotypes, by =
            Cohort] %>%
        # Scale within each sex
        .[, (adjustments) := lapply(.SD, scale_this),
        .SDcols = adjustments,
        by = Sex] %>%
        .[, c("FID", "IID", adjustments, "SES", "Education"), with = F]
    # Start doing the regression on each column one by one
    valid.samples <- fecundity[,c("FID", "IID")]   
    for(i in adjustments){
        valid.samples <- fecundity[,c("FID", "IID", i, "SES", "Education"), with=F] %>%
            na.omit %>%
            .[,pheno:=paste(i,"~SES+Education") %>%
                lm(., data=.SD) %>%
                resid] %>%
            .[,c("FID", "IID", "pheno")] %>%
            setnames(., "pheno",i) %>%
            .[valid.samples, on=c("FID", "IID")]
    }
    fwrite(valid.samples, "Fecundity.adj.csv")
    """
}

process r_extract_phenotype_from_sql{
    label 'normal'
    module 'R/4.3.0'
    input:
        tuple   val(type), 
                val(fieldID),
                val(coding),
                path(db)
    output:
        tuple   val(fieldID),
                val(type),
                path("${fieldID}.csv") optional true
    script:
    """
    #!/usr/bin/env Rscript
    library(data.table)
    library(DBI)
    library(dplyr)
    con <- DBI::dbConnect(RSQLite::SQLite(), dbname = "${db}")    
    statin <- c(1141146234, 1141192414, 1140910632,
            1140888594, 1140864592, 1141146138,
            1140861970, 1140888648, 1141192410,
            1141188146, 1140861958, 1140881748,
            1141200040, 1140861922)
    valid <- as.data.table(tbl(con, "Participant"))[withdrawn == 0]
    valid[,FID := sample_id]
    valid[,IID := sample_id]
    valid <- valid[,.(FID, IID, sample_id)]
    code_id_tbl  <- tbl(con, "data_meta") %>%
        as.data.table()
    target_code_id <- code_id_tbl[field_id==${fieldID}, code_id]
    code <- NULL
    if(length(target_code_id) != 0){
        code_tbl <- tbl(con, "code") %>%
            as.data.table()
        code <- code_tbl[code_id == target_code_id]
    }
    tryCatch({
        pheno_tbl <-tbl(con, "f${fieldID}")
        pheno <- as.data.table(pheno_tbl)[instance < 2] %>%
            setnames("pheno", "Phenotype")
        age <- as.data.table(tbl(con, "f21003")) %>%
            setnames("pheno", "Age") %>%
            .[, Age := as.numeric(Age)]
        centre <- as.data.table(tbl(con, "f54")) %>%
            setnames("pheno", "Centre") 
        fasting <- as.data.table(tbl(con, "f74")) %>%
            setnames("pheno", "Fasting") %>%
            .[, Fasting := as.numeric(Fasting)]
        dilution <- as.data.table(tbl(con, "f30897")) %>%
            setnames("pheno", "Dilution") %>%
            .[, Dilution := as.numeric(Dilution)]
        phenotype <- merge(valid, pheno) %>%
            merge(age, all.x = TRUE, by = c("sample_id", "instance")) %>%
            merge(centre, all.x = TRUE, by = c("sample_id", "instance"))%>%
            merge(fasting, all.x = TRUE, by = c("sample_id", "instance")) %>%
            merge(dilution, all.x = TRUE, by = c("sample_id", "instance")) %>%
            .[, sample_id:= NULL]
        if(!is.null(code)){
            code[,code_id := NULL]
            code[, value := as.character(value)]
            phenotype <- merge(phenotype, code, by.x = "Phenotype", by.y = "value", all.x = TRUE) %>%
                .[, Phenotype := as.numeric(Phenotype)] %>%
                .[is.na(meaning)] %>%
                .[, meaning:= NULL]
            new_order <- c(c("FID", "IID"), setdiff(names(phenotype), c("FID", "IID")))
            setcolorder(phenotype, new_order)
        }
        new_order <- c(c("FID", "IID"), setdiff(names(phenotype), c("FID", "IID")))
        setcolorder(phenotype, new_order)
        fwrite(phenotype, "${fieldID}.csv")
    }, error = function(cond){
        # Do nothing
        NA
    })
    """
}

process extract_phenotype_from_sql{
    label 'normal'
    publishDir "result/rawpheno"
    input:
        tuple   val(type), 
                val(fieldID),
                val(coding),
                val(instance),
                path(db)
    output:
        tuple   val(fieldID),
                val(type),
                val(instance),
                path("${fieldID}-${instance}.csv") optional true
    script:
    """
    echo "
    .mode csv
    .header on 
    CREATE  TEMP TABLE pheno_code
    AS
    SELECT  cm.value AS value,                 
            cm.meaning AS meaning                 
    FROM    code cm                               
    JOIN    data_meta dm ON dm.code_id=cm.code_id  
    WHERE   dm.field_id=${fieldID};                   

    .output ${fieldID}-${instance}.csv
    SELECT  s.sample_id AS FID,
            s.sample_id AS IID, 
            age.pheno AS Age,
            sex.pheno AS Sex,
            centre.pheno AS Centre,
            fasting.pheno AS Fasting,
            dilution.pheno AS Dilution,
            COALESCE(
               pheno_code.meaning, 
               trait.pheno) AS Phenotype${instance},
            MAX(
                CASE WHEN med.instance = ${instance} THEN 
                    CASE
                    WHEN
                        med.pheno in (1141146234, 1141192414, 1140910632,
                                        1140888594, 1140864592, 1141146138,
                                        1140861970, 1140888648, 1141192410,
                                        1141188146, 1140861958, 1140881748,
                                        1141200040, 1140861922)
                    THEN 1
                    ELSE 0
                    END
                END
            ) AS Statin
    FROM    f${fieldID} trait 
            LEFT JOIN   pheno_code ON 
                        pheno_code.value=trait.pheno 
            LEFT JOIN   Participant s  ON
                        s.withdrawn = 0 AND
                        s.sample_id = trait.sample_id
            LEFT JOIN   f20003 med ON 
                        s.sample_id=med.sample_id 
            LEFT JOIN   f31 sex ON
                        s.sample_id=sex.sample_id 
                        AND sex.instance = ${instance}
            LEFT JOIN   f21003 age ON 
                        s.sample_id=age.sample_id 
                        AND age.instance = ${instance}
            LEFT JOIN   f54 centre ON 
                        s.sample_id=centre.sample_id 
                        AND centre.instance = ${instance}
            LEFT JOIN   f74 fasting ON
                        s.sample_id=fasting.sample_id
                        AND fasting.instance = ${instance}
            LEFT JOIN   f30897 dilution ON
                        s.sample_id=dilution.sample_id
                        AND dilution.instance = ${instance}
    WHERE trait.instance = ${instance}
    GROUP BY trait.sample_id;
    .quit
    " > sql;
    sqlite3 ${db} < sql  || echo "skip"
    line=`wc -l ${fieldID}-${instance}.csv | cut -f 1 -d " "`
    if [[ \${line} -eq 0 ]];
    then
        rm ${fieldID}-${instance}.csv
    fi
    """
}

process get_blood_trait_name_from_will{
    module 'R/4.3.0'
    label 'normal'
    input:
        path(pheno)
    output: 
        path("blood_pheno")
    script:
    """
    #!/usr/bin/env Rscript
    library(data.table)
    dat <- fread("${pheno}",  nrows = 0)
    # Assume the format is the one we have from Will
    pheno <- colnames(dat)
    pheno <- pheno[!pheno %in% c("ID_1","Sex","Age","Centre","missing")]
    fwrite(data.table(trait = pheno, type = "Will_Blood",normalize = ifelse(pheno%like% "normalised", "normalised", "adj")), "blood_pheno")
    """
}
process extract_blood_traits{
    publishDir "result/pheno/resid/${normalize}/blood", mode: 'symlink'
    module 'R/4.3.0'
    label 'normal'
    input:
        tuple   val(fieldName),
                val(type),
                val(normalize),
                path(pheno),
                path(withdrawn),
                path(sibs),
                path(fam),
                path(covariate)
    output:
    tuple   val(fieldName),
            val(type),
            val(normalize),
            val("all"),
            path("${fieldName}.pheno"),
            path("${fieldName}-${normalize}.sibs"), emit: dat, optional: true
    
    tuple   path("${fieldName}.resid.norm.test"),
            path("${fieldName}-resid.hist.rds"),
            path("${fieldName}.raw.norm.test"),
            path("${fieldName}-raw.hist.rds"), emit: junk, optional: true
    
    script:
    """
    #!/usr/bin/env Rscript
    library(magrittr)
    library(data.table)
    library(moments)
    withdrawn <- fread("${withdrawn}", header = F)
    sibs <- fread("${sibs}") %>%
        .[!ID1 %in% withdrawn[, V1]] %>%
        .[!ID2 %in% withdrawn[, V1]]
    fam <- fread("${fam}") %>%
        .[!V2 %in% withdrawn[, V1]]
    cov <- fread("${covariate}") %>%
        .[IID %in% fam[, V2] |
            IID %in% sibs[, ID2] |
            IID %in% sibs[, ID1]]

    pheno <- fread("${pheno}") %>%
        .[, Phenotype := as.numeric(as.character(${fieldName}))] %>%
        setnames("ID_1", "IID") %>%
        .[, FID := IID]
    covariates <- c(paste0("PC", 1:40), "Batch")
    resid.form <- paste(c(covariates, "Centre"), collapse = "+") %>%
        paste0("Phenotype~", .)
    
    pheno <- merge(pheno[,.(FID, IID, Phenotype, Centre)], cov[, c("FID", "IID", covariates), with = FALSE], by = c("FID", "IID")) %>%
        na.omit %>%
        .[, Centre := as.factor(Centre)] %>%
        .[, Batch := as.factor(Batch)]
    
    # Now that we have identity of samples with phenotype we can 
    # Remove duplicated siblings
    sibs <- sibs[ID1 %in% pheno[,IID] | ID2 %in% pheno[,IID]] %>%
        .[,.SD[sample(.N)[1]], ID1]
    fwrite(sibs, "${fieldName}-${normalize}.sibs")

    if (nrow(pheno) < 10000 | length(unique(pheno[, Phenotype])) < 10) {
        
    } else{
        pheno %<>%
            .[Phenotype > mean(Phenotype) - 6 * sd(Phenotype) &
                Phenotype < mean(Phenotype) + 6 * sd(Phenotype)]
        #tade test
        test1=data.frame(           Mean=mean(pheno[,Phenotype], na.rm = T ), 
                                    Var=var(pheno[,Phenotype], na.rm = T ), 
                                    skew=skewness(pheno[,Phenotype], na.rm = T ), 
                                    kurtosis = kurtosis(pheno[,Phenotype], na.rm = T),
                                    Trait= "${fieldName}"

                        )
        saveRDS(object = hist(pheno[,Phenotype]), file = "${fieldName}-raw.hist.rds")
        fwrite(test1, "${fieldName}.raw.norm.test", sep = "\\t")
        if (!(nrow(pheno) < 10000 | length(unique(pheno[, Phenotype])) < 10)) {
           # if("${normalize}" == "inverse"){
           #     pheno[, Phenotype := qnorm((rank(Phenotype) - 0.5) / .N)]
           # }

            res <- pheno[,Phenotype := resid.form %>%
                    as.formula %>%
                    lm(., data = .SD) %>%
                    resid] %>%
                .[, c("FID", "IID", "Phenotype")] %>%
                na.omit

            #tade request
            test2=data.frame(           Mean=mean(res[,Phenotype], na.rm = T ), 
                                        Var=var(res[,Phenotype], na.rm = T ), 
                                        skew=skewness(res[,Phenotype], na.rm = T ), 
                                        kurtosis = kurtosis(res[,Phenotype], na.rm = T),
                                        Trait= "${fieldName}"

                            )
            saveRDS(object = hist(res[,Phenotype]), file = "${fieldName}-resid.hist.rds")
            fwrite(test2, "${fieldName}.resid.norm.test", sep = "\\t")

            # lastly, do inverse normal transformation 
            if("${normalize}" == "inverse"){
                res[, Phenotype := qnorm((rank(Phenotype) - 0.5) / .N)]
            }


            fwrite(res, "${fieldName}.pheno", sep = "\\t")
            
           
        }
    }
    """
}
process residualize_phenotype{
    publishDir "result/pheno/resid/${normalize}/${followUp_type}", mode: 'symlink'
    module 'R/4.3.0'
    label 'normal'
    input:

        tuple   val(fieldID),
                val(type),
                path(pheno),
                val(followUp_type),
                path(withdrawn),
                path(sibs),
                path(fam),
                path(covariate),
                val(normalize)
    output:
    tuple   val(fieldID),
            val(type),
            val(normalize),
            val(followUp_type),
            path("${fieldID}.pheno"),
            path("${fieldID}-${normalize}.sibs"), emit: dat, optional: true
    
    tuple   val(followUp_type), 
            path("${fieldID}.resid.norm.test"),
            path("${fieldID}-resid.hist.rds"),
            path("${fieldID}.raw.norm.test"),
            path("${fieldID}-raw.hist.rds"), emit: junk, optional: true
    script:
    """
    #!/usr/bin/env Rscript
    library(magrittr)
    library(data.table)
    library(moments)
    withdrawn <- fread("${withdrawn}", header = F)
    sibs <- fread("${sibs}") %>%
        .[!ID1 %in% withdrawn[, V1]] %>%
        .[!ID2 %in% withdrawn[, V1]]
    fam <- fread("${fam}") %>%
        .[!V2 %in% withdrawn[, V1]]
    cov <- fread("${covariate}") %>%
        .[IID %in% fam[, V2] |
            IID %in% sibs[, ID2] |
            IID %in% sibs[, ID1]] 

    #to remove

   
    pheno <- fread("${pheno}") %>%
        .[, Phenotype := as.numeric(as.character(Phenotype))]
    pheno <-  pheno[,FLAG := nrow(.SD) > 1, by = IID]

    resid.form <- paste("PC", 1:40, sep = "", collapse = "+") %>%
        paste0("Phenotype~Age+Age_Sq+Age_Cu+", .) 
    cov <- cov[!(pregnant ==1 | insulin_drug == 1) & IID %in% pheno[,IID],]


    if("${followUp_type}" == "second"){
        no_follow <- pheno[FLAG == FALSE][,instance := 1]
        pheno <- rbind(no_follow, pheno[instance == 1])
    }else if("${followUp_type}" == "base" || "${followUp_type}" == "all"){
        pheno <- pheno[instance == 0]
    }else{
        no_follow <- pheno[FLAG == FALSE][,instance:= 1]
        pheno <- rbind(no_follow, pheno)
    }
    pheno <- pheno[, Age_Sq := Age * Age] %>%
        .[, Age_Cu := Age * Age * Age] %>%
        merge(., cov) %>%
        .[, Centre := as.factor(Centre)] %>%
        .[, Batch := as.factor(Batch)]


    # remove menopause for female specific traits
    if("${fieldID}" %in% c("2674","2684","2694","2704","2714","2724","3581","3700","3710","3720","2734","2744","3872","2754","2764","2774","3829","3839","3849","2784","10132","2794","2804","2814","3536","3546","3591","2824","2834","3882")){
        categorical <- c("t2d", "CAD", "smoke_amount", "smoke_status", "alcohol_amount","alcohol_status", "Batch", "Centre", "Sex")
        for(i in categorical){
            if(length(unique(pheno[,get(i)])) > 1){
                resid.form <- paste0(resid.form, "+as.factor(",i, ")")
            }
        }
        
    }else{
        categorical <- c("t2d", "CAD", "menopause", "smoke_amount", "smoke_status", "alcohol_amount","alcohol_status", "Batch", "Centre", "Sex")
        for(i in categorical){
            if(length(unique(pheno[,get(i)])) > 1){
                resid.form <- paste0(resid.form, "+as.factor(",i, ")")
            }
        }
    }

    

    if("${type}" == "Blood"){
        # Remove samples on Statin
        pheno <- pheno[statin == 0][,-c("statin")]
        pheno <- pheno[chol_drug == 0]
        resid.form <- paste(resid.form, "Fasting+Dilution", sep="+")
    }else{
        # Ignore statin use, dilution and fasting
        pheno <- pheno[, -c("statin", "Fasting", "Dilution")]
    }
    #for pulse rate trait, remove people who took heart rate meds
    if("${fieldID}" == "4194"){
        pheno<- pheno[hr_drug == 0]
    }
   
    #for people who took blood pressure med, change phenotype value
    # Diastolic
    if("${fieldID}" == "4079" | "${fieldID}" == "94"){
        pheno<- pheno[bp_drug ==1, Pheno:=Pheno+10]
    }
    # SBP
    if("${fieldID}" == "4080" | "${fieldID}" == "93"){
        pheno<- pheno[bp_drug ==1, Pheno:=Pheno+15]
    }

    
    # Now that we have identity of samples with phenotype we can 
    # Remove duplicated siblings
    sibs <- sibs[ID1 %in% pheno[,IID] | ID2 %in% pheno[,IID]] %>%
        .[,.SD[sample(.N)[1]], ID1]
    fwrite(sibs, "${fieldID}-${normalize}.sibs")
    
    if (nrow(pheno) < 10000 | length(unique(pheno[, Phenotype])) < 10) {
        
    } else{
        pheno <- na.omit(pheno)
        if("${followUp_type}" != "mean"){
            pheno[, c("m", "s") := list(mean(Phenotype), sd(Phenotype)), by = instance]
            pheno <- pheno[Phenotype > m - 6 * s & Phenotype < m + 6 * s]
            pheno[,c("m", "s") := NULL]
        }
            #tade test
            test1=data.frame(           Mean=mean(pheno[,Phenotype], na.rm = T ), 
                                        Var=var(pheno[,Phenotype], na.rm = T ), 
                                        skew=skewness(pheno[,Phenotype], na.rm = T ), 
                                        kurtosis = kurtosis(pheno[,Phenotype], na.rm = T), 
                                        Trait= "${fieldID}"

                            )
            saveRDS(object = hist(pheno[,Phenotype]), file = "${fieldID}-raw.hist.rds")
            fwrite(test1, "${fieldID}.raw.norm.test", sep = "\\t")

        
        if (!(nrow(pheno) < 10000 | length(unique(pheno[, Phenotype])) < 10)) {
 #           if("${normalize}" == "inverse"){
 #               pheno[, Phenotype := qnorm((rank(Phenotype) - 0.5) / .N), by = instance]
 #           }
            res <- pheno[,Phenotype := resid.form %>%
                    as.formula %>%
                    lm(., data = .SD) %>%
                    resid, by = instance] %>%
                .[, .(Phenotype = mean(Phenotype, na.rm = TRUE)), by = c("FID", "IID", "FLAG")] %>%
                .[, c("FID", "IID", "FLAG", "Phenotype")] %>%
                na.omit
            
            #tade test
            test2=data.frame(           Mean=mean(res[,Phenotype], na.rm = T ), 
                                        Var=var(res[,Phenotype], na.rm = T ), 
                                        skew=skewness(res[,Phenotype], na.rm = T ), 
                                        kurtosis = kurtosis(res[,Phenotype], na.rm = T), Trait= "${fieldID}"

                            )
            saveRDS(object = hist(res[,Phenotype]), file = "${fieldID}-resid.hist.rds")
            fwrite(test2, "${fieldID}.resid.norm.test", sep = "\\t")

            # lastely, do inverse normal transformation
            if("${normalize}" == "inverse"){
                res[, Phenotype := qnorm((rank(Phenotype) - 0.5) / .N)]
            }

            fwrite(res, "${fieldID}.pheno", sep = "\\t")
            
            
        }
    }
    """
}



process split_base_target{
    module 'R/4.3.0'
    label 'normal'
    publishDir "pheno/${normalize}/${followUp_type}", mode: 'link', overwrite: true
    input:
        tuple   val(fieldID),
                val(type),
                val(normalize),
                val(followUp_type),
                path(pheno),
                path(sibs)
    output:
        tuple   val(fieldID),
                val(type),
                val(normalize),
                val(followUp_type),
                path("${fieldID}.base"), emit: base, optional: true
        tuple   val(fieldID),
                val(type),
                val(normalize),
                val(followUp_type),
                path("${fieldID}.target"), emit: target, optional: true
    script:
    """
    #!/usr/bin/env Rscript
    library(magrittr)
    library(data.table)
    sibs <- fread("${sibs}")
    dat <- fread("${pheno}")
    # To maximize our samples, try to include as much of the index samples in
    # the target
    if("${followUp_type}" == "all" || ("FLAG" %in% colnames(dat) && any(dat[,FLAG]))){
        dat[, Base := sample(c(rep(0, floor(.N/2)), rep(1, .N-floor(.N/2))))]
        if("${followUp_type}" != "all"){
            num.secondary <- nrow(dat[Base == 0 & FLAG == TRUE])
            dat[Base==0 & FLAG == TRUE, Base := 1]
            move <- dat[Base == 1 & FLAG == FALSE][sample(.N, num.secondary)]
            dat[IID %in% move[, IID], Base := 0]
        }else{
            dat[,FLAG := FALSE]
        }

   
        # count number of sibing data in base
        num.sib.in.base <-
            nrow(dat[Base == 0 &
                        (IID %in% sibs[, ID1] | IID %in% sibs[, ID2])])
        # Move all sib data to target
        dat[Base == 0 &
                (IID %in% sibs[, ID1] | IID %in% sibs[, ID2]), Base := 1]
        # Randomly move the same amount of non-sib data to base
        move <- dat[Base == 1 &
                    !IID %in% sibs[, ID1] &
                    !IID %in% sibs[, ID2] & FLAG == FALSE][sample(.N, num.sib.in.base)]
        dat[IID %in% move[,IID], Base := 0]
        # Don't include the siblings in the PRS regression
        dat[Base == 1 & IID %in% sibs[,ID2], Phenotype := NA]

        #Paul requested only retain indivi with repeat visit in the target
        if("${followUp_type}" != "all"){
            dat[Base==1 & FLAG == FALSE, Base := NA]
        }

        # Now we can output the data
        dat %>%
            .[Base == 0] %>%
            .[, -c("Base")] %>%
            fwrite(., "${fieldID}.base", sep = "\\t")
        dat %>%
            .[Base == 1] %>%
            .[, -c("Base")] %>%
            fwrite(., "${fieldID}.target", sep = "\\t", quote = F, na = "NA")
    }
    """
}
