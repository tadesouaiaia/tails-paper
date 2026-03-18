process merge_information{
    module 'R'
    label 'normal'
    publishDir "result/pheno/combined", mode: 'symlink', pattern: "*std.csv", overwrite: true
    publishDir "result/pheno/tade", mode: 'symlink', pattern: "*tade.csv", overwrite: true
    input:
        tuple   val(fieldID),
                val(type),
                val(normalize),
                val(followUp_type),
                path(pheno),
                path(sibs),
                path(summary),
                path(best),
                path(paternalAge),
                path(fecundity),
                path(illness),
                val(extreme),
                val(normal)
    output:
        tuple   val(fieldID),
                val(type),
                val(normalize),
                val(followUp_type),
                path("${fieldID}-${normalize}-std.csv"), emit: standard
        tuple   val(fieldID),
                val(type),
                val(normalize),
                val(followUp_type),
                path("${fieldID}-${normalize}-tade.csv"), emit: tade
        tuple   val(fieldID),
                val(type),
                val(normalize),
                val(followUp_type),
                path("${fieldID}-${normalize}-tade-prs.csv"), emit: tadePRS
    script:
    """
    #!/usr/bin/env Rscript
    library(magrittr)
    library(data.table)
    get_quantile <- function(x, num.quant) {
        quant <- as.numeric(cut(
            x,
            breaks = unique(quantile(x, probs = seq(
                0, 1, 1 / num.quant
            ))),
            include.lowest = T
        ))
        return(quant)
    }
    assign.group <- function(x, num.quant, extreme, normal) {
        x[, Pheno.Quant := get_quantile(Phenotype, num.quant)] %>%
            .[, Group := "Normal"] %>%
            .[Pheno.Quant <= normal, Group := "Abnormal"] %>%
            .[Pheno.Quant > num.quant - normal, Group := "Abnormal"] %>%
            .[Pheno.Quant <= extreme, Group := "Lower"] %>%
            .[Pheno.Quant > num.quant - extreme, Group := "Upper"] %>%
            return
    }
    # Read in data ------------------------------------------------------------
    prs <- fread("${best}") 
    pheno <- fread("${pheno}")
    sibs <- fread("${sibs}") %>%
        .[, c("ID1", "ID2")] %>%
        setnames(., "ID2", "IID")
    fecundity <- fread("${fecundity}")
    paternal <- fread("${paternalAge}")
    illness <- fread("${illness}")
    # Include everyone in downstream analysis
    # with exception of the PRS based analysis, 
    # include samples were used for GWAS
    prs.dat <- prs[pheno, on = c("FID", "IID")] %>%
        fecundity[., on = c("FID", "IID")] %>%
        paternal[., on = c("FID", "IID")] %>%
        illness[., on = c("FID", "IID")] %>%
        .[, InBase := is.na(In_Regression)]
    # Assign phenotype quantiles ----------------------------------------------
    prs.dat.quant <- prs.dat[In_Regression == "Yes" & !InBase] %>%
        .[, -c("In_Regression")] %>%
        assign.group(., 100, ${extreme}, ${normal})
    # By separate out sib samples, we don't include the sibling data when we calculate
    # the quantiles
    prs.dat <- prs.dat[IID %in% sibs[,IID]] %>%
        sibs[., on = c("IID")] %>%
        setnames(., "ID1", "Sibling") %>%
        .[, -c("In_Regression")] %>%
        rbind(., prs.dat.quant, fill=T)
        
    fwrite(prs.dat, "${fieldID}-${normalize}-std.csv")
    tade_dat <- prs.dat[,c("IID", "Sibling", "Phenotype")]
    tade_sib <- tade_dat[!is.na(Sibling)]
    setnames(tade_dat, "Phenotype", "Idx.Pheno")
    tade_input<-merge(tade_dat[is.na(Sibling)], tade_sib, by.x = "IID", by.y = "Sibling")[, c("Idx.Pheno", "Phenotype")]
    fwrite(tade_input, "${fieldID}-${normalize}-tade.csv")
    tade_prs <- prs.dat.quant[, c("IID", "PRS", "Phenotype")] %>%
        .[, In_Regression := "Yes"] %>%
        .[, c("IID", "In_Regression", "PRS", "Phenotype")]
    fwrite(tade_prs, "${fieldID}-${normalize}-tade-prs.csv")
    """
}
process tade_analyses{
    label 'normal'
    publishDir "result/fig/tade/vals/${followUp_type}", mode: "symlink", overwrite: true, pattern: "*vals.png" 
    publishDir "result/fig/tade/norm/${followUp_type}", mode: "symlink", overwrite: true, pattern: "*norm.png" 
    errorStrategy 'ignore'
    input:
        tuple   val(fieldID),
                val(type),
                val(normalize),
                val(followUp_type),
                path(tade_input),
                path(tade_python)
    output:
        tuple   val(fieldID),
                val(type),
                val(normalize),
                val(followUp_type),
                path("${fieldID}-${normalize}.h2"), emit: h2
        tuple   val(fieldID),
                val(type),
                val(normalize),
                val(followUp_type),
                path("${fieldID}-${normalize}.tail"), emit: tail
        tuple   val(fieldID),
                val(type),
                val(normalize),
                val(followUp_type),
                path("${fieldID}-${normalize}.data"), emit: data
    script:
    """
    pyenv local 3.7.2
    ./${tade_python} ${tade_input} --out ${fieldID}-${normalize} 
    """
}

process tade_new_prs {
    label 'normal'
    publishDir "result/pheno/tadePRS/${followUp_type}", mode: 'symlink',  overwite: true
    input:
        tuple   val(fieldID),
                val(type),
                val(normalize),
                val(followUp_type),
                path(tade_input),
                path(tade_python)
    output:
        tuple   val(fieldID),
                val(type), 
                val(normalize),
                val(followUp_type),
                path("${fieldID}-${normalize}-prs-out.csv")
    script:
    """
    pyenv local 3.7.2
    ./${tade_python} ${tade_input} > ${fieldID}-${normalize}-prs-out.csv
    """
}
process organize_tade{
    // in hindsight, should have just modify tade's script to generate the nice output
    // but just really prefer working with R
    label 'normal'
    module 'R'
    publishDir  "result/tade/", overwrite: true 
    input: 
        tuple   val(normalize),
                val(prefix),
                val(followUp_type),
                path(showcase),
                path(input)
    output:
        path("*.csv")
    script:
    """ 
    #!/usr/bin/env Rscript
    library(magrittr)
    library(data.table)
    showcase <- fread("${showcase}") %>%
        .[,c("Field","FieldID")] %>%
        .[,Field:=gsub(",","", Field)] %>%
        .[,FieldID := as.factor(FieldID)]
    h2_files <- strsplit("${input}", split=" ") %>%
        unlist 
    h2 <- NULL
    for(i in h2_files){
        name <- strsplit(i, split="-")[[1]][1]
        h2 <- rbind(h2, fread(i, header = TRUE)[,Trait := name])
    }
    h2 <- merge(h2, showcase, by.x = "Trait", by.y = "FieldID")
    fwrite(h2,  "${prefix}-${followUp_type}.csv")
    """

}
process statistical_analysis{
    module 'R'
    label 'long'
    input:
        tuple   val(fieldID),
                val(type),
                val(normalize),
                path(pheno),
                path(cov),
                path(showcase),
                val(extreme),
                val(normal),
                val(perm)
    output:
        tuple   val(normalize),
                path ("${fieldID}-${normalize}.original.csv"), emit: raw
        tuple   val(normalize), 
                path( "${fieldID}-${normalize}.perm.csv"), emit: perm, optional true
    script:
    """
    #!/usr/bin/env Rscript
    library(magrittr)
    library(data.table)
    get_quantile <- function(x, num.quant) {
        quant <- as.numeric(cut(
            x,
            breaks = unique(quantile(x, probs = seq(
                0, 1, 1 / num.quant
            ))),
            include.lowest = T
        ))
        return(quant)
    }
    # m1, m2: the sample means
    # s1, s2: the sample standard deviations
    # n1, n2: the same sizes
    # m0: the null value for the difference in means to be tested for. Default is 0.
    # equal.variance: whether or not to assume equal variance. Default is FALSE.
    t.test2 <- function(m1,
                        m2,
                        s1,
                        s2,
                        n1,
                        n2,
                        m0 = 0,
                        equal.variance = FALSE,
                        alternative = c("two.sided", "less", "greater"))
    {
      var1 <- s1 ^ 2
      var2 <- s2 ^ 2
      if (equal.variance == FALSE)
      {
        se <- sqrt((var1 / n1) + (var2 / n2))
        # welch-satterthwaite df
        df <-
          ((var1 / n1 + var2 / n2) ^ 2) / ((var1 / n1) ^ 2 / (n1 - 1) + (var2 / n2) ^ 2 / (n2 - 1))
      } else
      {
        # pooled standard deviation, scaled by the sample sizes
        se <-
          sqrt((1 / n1 + 1 / n2) * ((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 +  n2 - 2))
        df <- n1 + n2 - 2
      }
      t <- (m1 - m2 - m0) / se
      p <- pt(-abs(t), df)
      if ((alternative == "less" &
           t > 0) | (alternative == "greater" & t < 0)) {
        p <- 1
      } else if (alternative == "two.sided") {
        p <- 2 * pt(-abs(t), df)    
      }
      data.frame(
        mean = m1 - m2,
        se = se,
        t = t,
        p = p
      ) %>%
        return
    }
    # Regression to mean test -------------------------------------------------
    reg.mean.test <- function(x) {
        x <- x[is.na(Sibling) & !is.na(Phenotype)]
        training <- lm(PRS ~ Phenotype, x[Group == "Normal"])
        group.mean <- x[Group %in% c("Upper", "Lower"), .(Phenotype=mean(Phenotype), N=.N), by=Group] %>%
            .[, SD := predict(training, newdata=.SD, se.fit=T)\$se.fit * sqrt(N), by = Group] %>%
            setnames(., "Group", "group")
        x[Group %in% c("Upper", "Lower"),
        .(Expected = predict(training, newdata = .SD),
            PRS = PRS),
        by = Group] %>%
            .[, {
                tres = t.test2(
                    m1 = mean(PRS),
                    m2 = mean(Expected),
                    s1 = sd(PRS),
                    s2 = group.mean[group==Group, SD],
                    n1 = .N,
                    n2 = .N,
                    alternative = ifelse(Group == "Upper", "less", "greater")
                )
                list(
                    p = tres\$p,
                    t.stat = tres\$t,
                    N = .N,
                    model = coef(summary(training))[2,4],
                    r2 = summary(training)\$r.squared
                )
            }, by = Group] %>%
            .[, Type := "Reg.Mean"] %>%
            return(.)
    }
    # Fecundity tests ---------------------------------------------------------
    fecundity.test <- function(x) {
        # Remove irrelevant columns
        groups <- c("Normal", "Lower", "Upper")
        input <-
            x[Group %in% groups &
                is.na(Sibling)][, -c("FID",
                                    "IID",
                                    "Phenotype",
                                    "PRS",
                                    "Pheno.Quant",
                                    "Sibling",
                                    "Age",
                                    "Sex",
                                    "Centre")]
        fecundity.item <- colnames(input[,-c("Group")])
        res <- NULL
        for (i in fecundity.item) {
            validity.test <- input[, c(i, "Group"), with = F] %>%
                na.omit
            if (nrow(validity.test) != 0) {
                remove.group <- validity.test %>%
                    .[, .N, by = Group] %>%
                    .[N < 10, Group]
                exist.group <- groups %>%
                    .[. %in% validity.test[,Group]] %>%
                    .[!. %in% remove.group]
                if (length(exist.group) > 1) {
                    tmp <- validity.test[Group %in% exist.group & Group != "Normal", {
                        tres = t.test(get(i), input[Group == "Normal", get(i)], 
                                alternative = ifelse(i %in% c("Illness", "PaternalAge", "IllnessEdu", "PaternalAgeEdu", "NumMiscarriages", "LiveBirth"), "greater", "less"))
                        list(
                            p = tres\$p.value,
                            t.stat = tres\$statistic,
                            N = .N
                        )
                    }, by = Group] %>%
                        .[, Type := i]
                    res %<>% rbind(., tmp)
                }
            }
        }
        return(res)
    }
    # Sibling test ------------------------------------------------------------
    sib.reg.test <- function(x){
        # Sibling = index Sib of current sample
        # Samples without Sibling columns are included in other analyses
        # Here, we want the quantile of the index sib, but phenotype of the 
        # observed sib
        groups <- c("Normal", "Lower", "Upper")
        # First, extract the index Sibling's information
        idx.of.sib <- x[Group %in% groups & IID %in% Sibling] %>%
            # We want their group and phenotype quantile
            .[, c("IID", "Group","Pheno.Quant", "Phenotype")] %>%
            setnames(., "Phenotype", "Idx.Pheno") %>%
            # Now, we want the phenotype of the sibling
            merge(., x[,c("Sibling", "Phenotype")], by.x="IID", by.y="Sibling") %>%
            na.omit
        remove.group <- idx.of.sib[, .N, by = Group][N < 10, Group]
        exist.group <- groups %>%
            .[. %in% idx.of.sib[,Group]] %>%
            .[!. %in% remove.group]
        if(length(exist.group) > 1 & "Normal" %in% exist.group){
            # We want to train the model based on the quantile
            training <- lm(Phenotype ~ Idx.Pheno, idx.of.sib[Group == "Normal"])
            group.mean <- idx.of.sib[Group %in% exist.group & Group != "Normal", .(Idx.Pheno=mean(Idx.Pheno), N=.N), by=Group] %>%
                .[, SD := predict(training, newdata=.SD, se.fit=T)\$se.fit * sqrt(N), by = Group] %>%
                setnames(., "Group", "group")
            idx.of.sib[Group %in% exist.group & Group != "Normal",
            .(Expected = predict(training, newdata = .SD),
                Phenotype = Phenotype),
            by = Group] %>%
                .[, {
                    tres = t.test2(
                        m1 = mean(Phenotype),
                        m2 = mean(Expected),
                        s1 = sd(Phenotype),
                        s2 = group.mean[group==Group, SD],
                        n1 = .N,
                        n2 = .N,
                        alternative = ifelse(Group == "Upper", "less", "greater")
                    )
                    list(
                        p = tres\$p,
                        t.stat = tres\$t,
                        N = .N,
                        model = coef(summary(training))[2,4],
                        r2 = summary(training)\$r.squared
                    )
                }, by = Group] %>%
                    .[, Type := "Sib.Reg.Test"] %>%
                    return(.)
        }
    }

    sib.test <- function(x) {
        groups <- c("Normal", "Lower", "Upper")
        sib.of.idx <- x[Group %in% groups & IID %in% Sibling] %>%
            .[, c("IID", "Group")] %>%
            merge(.,x[,c("Sibling", "Phenotype")], by.x="IID", by.y="Sibling") %>%
            na.omit
        remove.group <- sib.of.idx[, .N, by = Group][N < 10, Group]
        exist.group <- groups %>%
            .[. %in% sib.of.idx[,Group]] %>%
            .[!. %in% remove.group]
        if (length(exist.group) > 1) {
            sib.of.idx[Group %in% exist.group & Group != "Normal", {
                tres = t.test(Phenotype,
                            sib.of.idx[Group == "Normal", Phenotype],
                            alternative = ifelse(Group == "Upper", "greater", "less"))
                list(
                    p = tres\$p.value,
                    t.stat = tres\$statistic,
                    N = .N
                    
                )
            }, by = Group]  %>%
                .[, Type := "Sib.Test"] %>%
                return(.)
        }
    }

    sib.var.test <- function(x){
        groups <- c("Lower", "Upper", "Normal")
        sib.of.idx <- x[(Group %in% groups) & IID %in% Sibling] %>%
            .[, c("IID", "Group")] %>%
            merge(.,x[,c("Sibling", "Phenotype")], by.x="IID", by.y="Sibling") %>%
            na.omit
        remove.group <- sib.of.idx[, .N, by = Group][N < 10, Group]
        exist.group <- groups %>%
            .[. %in% sib.of.idx[,Group]] %>%
            .[!. %in% remove.group]
        if(length(exist.group) > 1 & "Normal" %in% exist.group){
            sib.of.idx[Group %in% exist.group & Group != "Normal", {
                fres = var.test(Phenotype, 
                                sib.of.idx[Group=="Normal", Phenotype], 
                                alternative = "greater")
                list(
                    p = fres\$p.value,
                    t.stat = fres\$statistic,
                    N = .N
                )
            }, by = Group]  %>%
                .[, Type := "Sib.Var.Test"] %>%
                return(.)
        }
    }
    # illness test ------------------------------------------------------------
    illness.test <- function(x, cov){
        illness <- merge(x[is.na(Sibling)], cov, by = c("FID", "IID")) %>%
            .[, Batch := as.factor(Batch)] %>%
            .[, Centre := as.factor(Centre)] %>%
            .[, c("IllnessEdu",
                "PRS",
                "Batch",
                "Sex",
                "Centre",
                "Group",
                paste("PC", 1:40, sep = "")), with = F] %>%
            na.omit
        # Need to account for situation where we have too many degree of freedom
        singular.factor <-
            illness[, .(
                Centre = length(unique(Centre)),
                Batch = length(unique(Batch)),
                df = .N - 40 - 2
            ), by = Group] %>%
            .[, Cov := ifelse(Centre == 1, "", "+Centre")] %>%
            .[, Cov := ifelse(Batch == 1 |
                                Batch > df, Cov, paste0(Cov, "+Batch"))] %>%
            .[, c("Group", "Cov")] %>%
            setnames(., "Group", "Type")
        illness[Group %in% c("Upper", "Lower"), {
            model <- paste("PC", 1:40, sep = "", collapse = "+") %>%
                paste("IllnessEdu~PRS+Sex+", .) %>%
                paste(., singular.factor[Type == Group, Cov]) %>%
                as.formula %>%
                lm(., data = .SD) %>%
                summary
            list(
                p = model\$coefficient[2, 4],
                t.stat = model\$coefficient[2, 3],
                N = .N
            )
        }, by = Group] %>%
            .[, Type := "IllnessTest"] %>%
            return(.)
    }
    # Load data and run test
    showcase <- fread("${showcase}") %>%
        .[,c("Field","FieldID")] %>%
        .[,Field:=gsub(",","", Field)] %>%
        .[,FieldID := as.factor(FieldID)]
    name <- showcase[FieldID %in% "${fieldID}", Field]
    prs.dat <- fread("${pheno}")
    cov <- fread("${cov}")
    result <- reg.mean.test(prs.dat) %>%
        rbind(., sib.test(prs.dat), fill=T) %>%
        rbind(., sib.var.test(prs.dat), fill=T) %>%
        rbind(., sib.reg.test(prs.dat), fill=T) %>%
        rbind(., illness.test(prs.dat, cov), fill=T) %>%
        rbind(., fecundity.test(prs.dat), fill=T) %>%
        dcast(., Group ~ Type, value.var = c("p", "t.stat","model", "r2", "N")) %>%
        .[, FieldID := "${fieldID}"] %>%
        .[, Trait := name] %>% 
        .[, Type := "${normalize}"]

    fwrite(result, "${fieldID}-${normalize}.original.csv")
    if(${perm} > 0){
        num.quant <- 100
        result[,Perm:= "Ori"]
        pb <- txtProgressBar(min = 0, max = ${perm}, initial = 0,  style = 3) 
        for(i in 1:${perm}){
            # Shuffle phenotype
            prs.dat[,Phenotype:=sample(Phenotype)] %>%
                .[is.na(Sibling) , Pheno.Quant := get_quantile(Phenotype, num.quant)] %>%
                .[, Group := "Normal"] %>%
                .[Pheno.Quant <= ${normal}, Group := "Abnormal"] %>%
                .[Pheno.Quant > num.quant - ${normal}, Group := "Abnormal"] %>%
                .[Pheno.Quant <= ${extreme}, Group := "Lower"] %>%
                .[Pheno.Quant > num.quant - ${extreme}, Group := "Upper"]

            tmp <- reg.mean.test(prs.dat) %>%
                rbind(., sib.test(prs.dat), fill=T) %>%
                rbind(., sib.var.test(prs.dat), fill=T) %>%
                rbind(., sib.reg.test(prs.dat), fill=T) %>%
                rbind(., illness.test(prs.dat, cov), fill=T) %>%
                rbind(., fecundity.test(prs.dat), fill=T) %>%
                dcast(., Group ~ Type, value.var = c("p", "t.stat", "model", "r2", "N")) %>%
                .[, FieldID := "${fieldID}"] %>%
                .[, Trait := name] %>% 
                .[, Type := "${normalize}"] %>%
                .[, Perm := i]
            setTxtProgressBar(pb, i)
            result %<>% rbind(., tmp, fill=T)
        }
        fwrite(result, "${fieldID}-${normalize}.perm.csv", na="NA", quote=F)
    }
    """
}

process statistical_analysis2{
    module 'R'
    label 'long'
    input:
        tuple   val(fieldID),
                val(type),
                val(normalize),
                path(pheno),
                path(cov),
                path(showcase),
                val(extreme),
                val(normal),
                val(perm)
    output:
        tuple   val(normalize),
                path ("${fieldID}-${normalize}.original.csv"), emit: raw
        tuple   val(normalize), 
                path( "${fieldID}-${normalize}.perm.csv"), emit: perm optional true
    script:
    """
    #!/usr/bin/env Rscript
    library(magrittr)
    library(data.table)
    get_quantile <- function(x, num.quant) {
        quant <- as.numeric(cut(
            x,
            breaks = unique(quantile(x, probs = seq(
                0, 1, 1 / num.quant
            ))),
            include.lowest = T
        ))
        return(quant)
    }
    # m1, m2: the sample means
    # s1, s2: the sample standard deviations
    # n1, n2: the same sizes
    # m0: the null value for the difference in means to be tested for. Default is 0.
    # equal.variance: whether or not to assume equal variance. Default is FALSE.
    t.test2 <- function(m1,
                        m2,
                        s1,
                        s2,
                        n1,
                        n2,
                        m0 = 0,
                        equal.variance = FALSE,
                        alternative = c("two.sided", "less", "greater"))
    {
      var1 <- s1 ^ 2
      var2 <- s2 ^ 2
      if (equal.variance == FALSE)
      {
        se <- sqrt((var1 / n1) + (var2 / n2))
        # welch-satterthwaite df
        df <-
          ((var1 / n1 + var2 / n2) ^ 2) / ((var1 / n1) ^ 2 / (n1 - 1) + (var2 / n2) ^ 2 / (n2 - 1))
      } else
      {
        # pooled standard deviation, scaled by the sample sizes
        se <-
          sqrt((1 / n1 + 1 / n2) * ((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 +  n2 - 2))
        df <- n1 + n2 - 2
      }
      t <- (m1 - m2 - m0) / se
      p <- pt(-abs(t), df)
      if ((alternative == "less" &
           t > 0) | (alternative == "greater" & t < 0)) {
        p <- 1
      } else if (alternative == "two.sided") {
        p <- 2 * pt(-abs(t), df)    
      }
      data.frame(
        mean = m1 - m2,
        se = se,
        t = t,
        p = p
      ) %>%
        return
    }
    # Regression to mean test -------------------------------------------------
    reg.mean.test <- function(x) {
        x <- x[is.na(Sibling) & !is.na(Phenotype)]
        training <- lm(PRS ~ Phenotype, x[Group == "Normal"])
        group.mean <- x[Group %in% c("Upper", "Lower"), .(Phenotype=mean(Phenotype), N=.N), by=Group] %>%
            .[, SD := predict(training, newdata=.SD, se.fit=T)\$se.fit * sqrt(N), by = Group] %>%
            setnames(., "Group", "group")
        x[Group %in% c("Upper", "Lower"),
        .(Expected = predict(training, newdata = .SD),
            PRS = PRS),
        by = Group] %>%
            .[, {
                tres = t.test2(
                    m1 = mean(PRS),
                    m2 = mean(Expected),
                    s1 = sd(PRS),
                    s2 = group.mean[group==Group, SD],
                    n1 = .N,
                    n2 = .N,
                    alternative = ifelse(Group == "Upper", "less", "greater")
                )
                list(
                    p = tres\$p,
                    t.stat = tres\$t,
                    N = .N,
                    model = coef(summary(training))[2,4],
                    r2 = summary(training)\$r.squared
                )
            }, by = Group] %>%
            .[, Type := "Reg.Mean"] %>%
            return(.)
    }
    # Fecundity tests ---------------------------------------------------------
    fecundity.test <- function(x) {
        # Remove irrelevant columns
        groups <- c("Normal", "Lower", "Upper")
        input <-
            x[Group %in% groups &
                is.na(Sibling)][, -c("FID",
                                    "IID",
                                    "Phenotype",
                                    "PRS",
                                    "Pheno.Quant",
                                    "Sibling",
                                    "Age",
                                    "Sex",
                                    "Centre")]
        fecundity.item <- colnames(input[,-c("Group")])
        res <- NULL
        for (i in fecundity.item) {
            validity.test <- input[, c(i, "Group"), with = F] %>%
                na.omit
            if (nrow(validity.test) != 0) {
                remove.group <- validity.test %>%
                    .[, .N, by = Group] %>%
                    .[N < 10, Group]
                exist.group <- groups %>%
                    .[. %in% validity.test[,Group]] %>%
                    .[!. %in% remove.group]
                if (length(exist.group) > 1) {
                    tmp <- validity.test[Group %in% exist.group & Group != "Normal", {
                        tres = t.test(get(i), input[Group == "Normal", get(i)], 
                                alternative = ifelse(i %in% c("Illness", "PaternalAge", "IllnessEdu", "PaternalAgeEdu", "NumMiscarriages", "LiveBirth"), "greater", "less"))
                        list(
                            p = tres\$p.value,
                            t.stat = tres\$statistic,
                            N = .N
                        )
                    }, by = Group] %>%
                        .[, Type := i]
                    res %<>% rbind(., tmp)
                }
            }
        }
        return(res)
    }
    # Sibling test ------------------------------------------------------------
    sib.reg.test <- function(x){
        # Sibling = index Sib of current sample
        # Samples without Sibling columns are included in other analyses
        # Here, we want the quantile of the index sib, but phenotype of the 
        # observed sib
        groups <- c("Normal", "Lower", "Upper")
        # First, extract the index Sibling's information
        idx.of.sib <- x[Group %in% groups & IID %in% Sibling] %>%
            # We want their group and phenotype quantile
            .[, c("IID", "Group","Pheno.Quant", "Phenotype")] %>%
            setnames(., "Phenotype", "Idx.Pheno") %>%
            # Now, we want the phenotype of the sibling
            merge(., x[,c("Sibling", "Phenotype")], by.x="IID", by.y="Sibling") %>%
            na.omit
        remove.group <- idx.of.sib[, .N, by = Group][N < 10, Group]
        exist.group <- groups %>%
            .[. %in% idx.of.sib[,Group]] %>%
            .[!. %in% remove.group]
        if(length(exist.group) > 1 & "Normal" %in% exist.group){
            # We want to train the model based on the quantile
            training <- lm(Phenotype ~ Idx.Pheno, idx.of.sib[Group == "Normal"])
            group.mean <- idx.of.sib[Group %in% exist.group & Group != "Normal", .(Idx.Pheno=mean(Idx.Pheno), N=.N), by=Group] %>%
                .[, SD := predict(training, newdata=.SD, se.fit=T)\$se.fit * sqrt(N), by = Group] %>%
                setnames(., "Group", "group")
            idx.of.sib[Group %in% exist.group & Group != "Normal",
            .(Expected = predict(training, newdata = .SD),
                Phenotype = Phenotype),
            by = Group] %>%
                .[, {
                    tres = t.test2(
                        m1 = mean(Phenotype),
                        m2 = mean(Expected),
                        s1 = sd(Phenotype),
                        s2 = group.mean[group==Group, SD],
                        n1 = .N,
                        n2 = .N,
                        alternative = ifelse(Group == "Upper", "less", "greater")
                    )
                    list(
                        p = tres\$p,
                        t.stat = tres\$t,
                        N = .N,
                        model = coef(summary(training))[2,4],
                        r2 = summary(training)\$r.squared
                    )
                }, by = Group] %>%
                    .[, Type := "Sib.Reg.Test"] %>%
                    return(.)
        }
    }

    sib.test <- function(x) {
        groups <- c("Normal", "Lower", "Upper")
        sib.of.idx <- x[Group %in% groups & IID %in% Sibling] %>%
            .[, c("IID", "Group")] %>%
            merge(.,x[,c("Sibling", "Phenotype")], by.x="IID", by.y="Sibling") %>%
            na.omit
        remove.group <- sib.of.idx[, .N, by = Group][N < 10, Group]
        exist.group <- groups %>%
            .[. %in% sib.of.idx[,Group]] %>%
            .[!. %in% remove.group]
        if (length(exist.group) > 1) {
            sib.of.idx[Group %in% exist.group & Group != "Normal", {
                tres = t.test(Phenotype,
                            sib.of.idx[Group == "Normal", Phenotype],
                            alternative = ifelse(Group == "Upper", "greater", "less"))
                list(
                    p = tres\$p.value,
                    t.stat = tres\$statistic,
                    N = .N
                    
                )
            }, by = Group]  %>%
                .[, Type := "Sib.Test"] %>%
                return(.)
        }
    }

    sib.var.test <- function(x){
        groups <- c("Lower", "Upper", "Normal")
        sib.of.idx <- x[(Group %in% groups) & IID %in% Sibling] %>%
            .[, c("IID", "Group")] %>%
            merge(.,x[,c("Sibling", "Phenotype")], by.x="IID", by.y="Sibling") %>%
            na.omit
        remove.group <- sib.of.idx[, .N, by = Group][N < 10, Group]
        exist.group <- groups %>%
            .[. %in% sib.of.idx[,Group]] %>%
            .[!. %in% remove.group]
        if(length(exist.group) > 1 & "Normal" %in% exist.group){
            sib.of.idx[Group %in% exist.group & Group != "Normal", {
                fres = var.test(Phenotype, 
                                sib.of.idx[Group=="Normal", Phenotype], 
                                alternative = "greater")
                list(
                    p = fres\$p.value,
                    t.stat = fres\$statistic,
                    N = .N
                )
            }, by = Group]  %>%
                .[, Type := "Sib.Var.Test"] %>%
                return(.)
        }
    }
    # illness test ------------------------------------------------------------
    illness.test <- function(x, cov){
        illness <- merge(x[is.na(Sibling)], cov, by = c("FID", "IID")) %>%
            .[, Batch := as.factor(Batch)] %>%
            .[, Centre := as.factor(Centre)] %>%
            .[, c("IllnessEdu",
                "PRS",
                "Batch",
                "Sex",
                "Centre",
                "Group",
                paste("PC", 1:40, sep = "")), with = F] %>%
            na.omit
        # Need to account for situation where we have too many degree of freedom
        singular.factor <-
            illness[, .(
                Centre = length(unique(Centre)),
                Batch = length(unique(Batch)),
                df = .N - 40 - 2
            ), by = Group] %>%
            .[, Cov := ifelse(Centre == 1, "", "+Centre")] %>%
            .[, Cov := ifelse(Batch == 1 |
                                Batch > df, Cov, paste0(Cov, "+Batch"))] %>%
            .[, c("Group", "Cov")] %>%
            setnames(., "Group", "Type")
        illness[Group %in% c("Upper", "Lower"), {
            model <- paste("PC", 1:40, sep = "", collapse = "+") %>%
                paste("IllnessEdu~PRS+Sex+", .) %>%
                paste(., singular.factor[Type == Group, Cov]) %>%
                as.formula %>%
                lm(., data = .SD) %>%
                summary
            list(
                p = model\$coefficient[2, 4],
                t.stat = model\$coefficient[2, 3],
                N = .N
            )
        }, by = Group] %>%
            .[, Type := "IllnessTest2"] %>%
            return(.)
    }
    # illness test 2 ------------------------------------------------------------
illness.test2 <- function(x, cov){
    illness <- merge(x[is.na(Sibling)], cov, by = c("FID", "IID")) %>%
        .[, Batch := as.factor(Batch)] %>%
        .[, Centre := as.factor(Centre)] %>%
        .[, c("Phenotype",
              "PRS",
              "Batch",
              "Sex",
              "Centre",
              "Group",
              paste("PC", 1:40, sep = "")), with = F] %>%
        na.omit
    # Need to account for situation where we have too many degree of freedom
    singular.factor <-
        illness[, .(
            Centre = length(unique(Centre)),
            Batch = length(unique(Batch)),
            df = .N - 40 - 2
        ), by = Group] %>%
        .[, Cov := ifelse(Centre == 1, "", "+Centre")] %>%
        .[, Cov := ifelse(Batch == 1 |
                              Batch > df, Cov, paste0(Cov, "+Batch"))] %>%
        .[, c("Group", "Cov")] %>%
        setnames(., "Group", "Type")
    illness[Group %in% c("Upper", "Lower"), {
        model <- paste("PC", 1:40, sep = "", collapse = "+") %>%
            paste("Phenotype~PRS+Sex+", .) %>%
            paste(., singular.factor[Type == Group, Cov]) %>%
            as.formula %>%
            lm(., data = .SD) %>%
            summary
        list(
            p = model\$coefficient[2, 4],
            t.stat = model\$coefficient[2, 3],
            N = .N
        )
    }, by = Group] %>%
        .[, Type := "IllnessTest"] %>%
        return(.)
}
    # Load data and run test
    showcase <- fread("${showcase}") %>%
        .[,c("Field","FieldID")] %>%
        .[,Field:=gsub(",","", Field)] %>%
        .[,FieldID := as.factor(FieldID)]
    name <- showcase[FieldID %in% "${fieldID}", Field]
    prs.dat <- fread("${pheno}")
    cov <- fread("${cov}")
    result <- reg.mean.test(prs.dat) %>%
        rbind(., sib.test(prs.dat), fill=T) %>%
        rbind(., sib.var.test(prs.dat), fill=T) %>%
        rbind(., sib.reg.test(prs.dat), fill=T) %>%
        rbind(., illness.test(prs.dat, cov), fill=T) %>%
        rbind(., illness.test2(prs.dat, cov), fill=T) %>%
        rbind(., fecundity.test(prs.dat), fill=T) %>%
        dcast(., Group ~ Type, value.var = c("p", "t.stat","model", "r2", "N")) %>%
        .[, FieldID := "${fieldID}"] %>%
        .[, Trait := name] %>% 
        .[, Type := "${normalize}"]

    fwrite(result, "${fieldID}-${normalize}.original.csv")
    if(${perm} > 0){
        num.quant <- 100
        result[,Perm:= "Ori"]
        pb <- txtProgressBar(min = 0, max = ${perm}, initial = 0,  style = 3) 
        for(i in 1:${perm}){
            # Shuffle phenotype
            prs.dat[,Phenotype:=sample(Phenotype)] %>%
                .[is.na(Sibling) , Pheno.Quant := get_quantile(Phenotype, num.quant)] %>%
                .[, Group := "Normal"] %>%
                .[Pheno.Quant <= ${normal}, Group := "Abnormal"] %>%
                .[Pheno.Quant > num.quant - ${normal}, Group := "Abnormal"] %>%
                .[Pheno.Quant <= ${extreme}, Group := "Lower"] %>%
                .[Pheno.Quant > num.quant - ${extreme}, Group := "Upper"]

            tmp <- reg.mean.test(prs.dat) %>%
                rbind(., sib.test(prs.dat), fill=T) %>%
                rbind(., sib.var.test(prs.dat), fill=T) %>%
                rbind(., sib.reg.test(prs.dat), fill=T) %>%
                rbind(., illness.test(prs.dat, cov), fill=T) %>%
                rbind(., illness.test2(prs.dat, cov), fill=T) %>%
                rbind(., fecundity.test(prs.dat), fill=T) %>%
                dcast(., Group ~ Type, value.var = c("p", "t.stat", "model", "r2", "N")) %>%
                .[, FieldID := "${fieldID}"] %>%
                .[, Trait := name] %>% 
                .[, Type := "${normalize}"] %>%
                .[, Perm := i]
            setTxtProgressBar(pb, i)
            result %<>% rbind(., tmp, fill=T)
        }
        fwrite(result, "${fieldID}-${normalize}.perm.csv", na="NA", quote=F)
    }
    """
}
process dichotomize_extreme{
    module 'R'
    label 'long'
    publishDir "result/pheno/dichotomized", mode: 'symlink'
    input:
        tuple   val(fieldID),
                val(type),
                val(normalize),
                path(pheno),
                path(showcase),
                val(extreme),
                val(normal)
    output:
        path("${fieldID}-${normalize}-dichotomize.csv")
script:
    """
    #!/usr/bin/env Rscript
    library(magrittr)
    library(data.table)
    # m1, m2: the sample means
    # s1, s2: the sample standard deviations
    # n1, n2: the same sizes
    # m0: the null value for the difference in means to be tested for. Default is 0.
    # equal.variance: whether or not to assume equal variance. Default is FALSE.
    t.test2 <- function(m1,
                        m2,
                        s1,
                        s2,
                        n1,
                        n2,
                        m0 = 0,
                        equal.variance = FALSE,
                        alternative = c("two.sided", "less", "greater"))
    {
      var1 <- s1 ^ 2
      var2 <- s2 ^ 2
      if (equal.variance == FALSE)
      {
        se <- sqrt((var1 / n1) + (var2 / n2))
        # welch-satterthwaite df
        df <-
          ((var1 / n1 + var2 / n2) ^ 2) / ((var1 / n1) ^ 2 / (n1 - 1) + (var2 / n2) ^ 2 / (n2 - 1))
      } else
      {
        # pooled standard deviation, scaled by the sample sizes
        se <-
          sqrt((1 / n1 + 1 / n2) * ((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 +  n2 - 2))
        df <- n1 + n2 - 2
      }
      t <- (m1 - m2 - m0) / se
      p <- pt(-abs(t), df)
      if ((alternative == "less" &
           t > 0) | (alternative == "greater" & t < 0)) {
        p <- 1
      } else if (alternative == "two.sided") {
        p <- 2 * pt(-abs(t), df)    
      }
      data.frame(
        mean = m1 - m2,
        se = se,
        t = t,
        p = p
      ) %>%
        return
    }
    # Regression to mean test -------------------------------------------------
    reg.mean.test <- function(x) {
        x <- x[is.na(Sibling) & !is.na(Phenotype) & !InBase]
        training <- lm(PRS ~ Phenotype, x[Group == "Normal"])
        group.mean <- x[Group %in% c("Upper", "Lower"), .(Phenotype=mean(Phenotype), N=.N), by=Group] %>%
            .[, SD := predict(training, newdata=.SD, se.fit=T)\$se.fit * sqrt(N), by = Group] %>%
            setnames(., "Group", "group")
        x[Group %in% c("Upper", "Lower"),
        .(Expected = predict(training, newdata = .SD),
            PRS = PRS),
        by = Group] %>%
            .[, {
                tres = t.test2(
                    m1 = mean(PRS),
                    m2 = mean(Expected),
                    s1 = sd(PRS),
                    s2 = group.mean[group==Group, SD],
                    n1 = .N,
                    n2 = .N,
                    alternative = ifelse(Group == "Upper", "less", "greater")
                )
                list(
                    p = tres\$p,
                    t.stat = tres\$t,
                    N = .N
                )
            }, by = Group] %>%
            .[, Type := "Reg.Mean"] %>%
            return(.)
    }
    
    # Load data and run test
    showcase <- fread("${showcase}") %>%
        .[,c("Field","FieldID")] %>%
        .[,Field:=gsub(",","", Field)] %>%
        .[,FieldID := as.factor(FieldID)]
    name <- showcase[FieldID %in% "${fieldID}", Field]
    prs.dat <- fread("${pheno}") %>%
        .[is.na(Sibling) & !is.na(Phenotype)] 
    training <- lm(PRS ~ Phenotype, prs.dat[Group == "Normal"])
    group.mean <- prs.dat[Group %in% c("Upper", "Lower"), .(Phenotype=mean(Phenotype), N=.N), by=Group] %>%
        .[, SE := predict(training, newdata=.SD, se.fit=T)\$se.fit, by = Group] %>%
        setnames(., "Group", "group")
    prs.dat[Group %in% c("Upper", "Lower")] %>%
        .[, Expected := predict(training, newdata = .SD), by = Group] %>%
        .[, Mean := mean(Expected), by = Group ] %>%
        .[, SE := ifelse(Group == "Upper", group.mean[group=="Upper", SE], group.mean[group=="Lower", SE])] %>%
        fwrite("${fieldID}-${normalize}-dichotomize.csv")
    """
}

process qq_plot{
    label 'normal'
    module 'R'

    publishDir "result/fig", mode: 'copy', overwrite: 'true'
    input:
        path(raw)
    output:
        path("qq_inverse.png")
    script:
    """
    #!/usr/bin/env Rscript
    library(magrittr)
    library(data.table)
    library(forcats)
    library(ggplot2)
    library(ggsci)
    dat <- fread("${raw}") %>%
        .[Type != "raw"]
    select <-
        c(
            "Group",
            "p_Fecundity.adj",
            "p_Illness",
            "p_IllnessTest",
            "p_PaternalAgeEdu",
            "p_Reg.Mean",
            "p_Sib.Reg.Test"
        )
    dat %<>% .[, ..select] %>%
        melt(., id.vars= c("Group")) %>%
         .[, variable:=gsub( "p_|.adj\$","", variable)] %>%
         na.omit %>%
         .[, P := -log10(value)] %>%
         .[, Expected := -log10((.N + 1 - rank(P, ties.method = "first")-.5)/(.N+1)), by=c("variable", "Group")] %>%
         .[is.finite(P)] %>%
         .[, variable := fct_relevel(variable, "Reg.Mean", "Illness", "Fecundity", "Sib.Reg.Test", "PaternalAgeEdu")] %>%
         .[, variable := fct_recode(variable, `PRS RM`="Reg.Mean", `Sibling RM` = "Sib.Reg.Test", `Paternal Age`="PaternalAgeEdu", `Num of illnesses`="Illness", `PRS Vs Num of illnesses`="IllnessTest")]
    plot <- dat %>%
        ggplot(aes(x = Expected, y = P, color = variable)) +
        geom_point(size = 1.5) +
        theme_classic() +
        facet_wrap(~ Group) +
        labs(x = bquote(Expected~-log[10]~P-value), y = bquote(Observed~-log[10]~P-value)) +
        theme(
            axis.title = element_text(size = 16, face = "bold"),
            axis.text = element_text(size = 14),
            strip.text = element_text(size = 16, face = "bold"),
            legend.title = element_blank(),
            legend.text = element_text(size = 14),
            legend.box.background = element_rect(colour = "black")
        ) +
        geom_hline(yintercept = -log10(0.05), linetype = "dotted") +
        scale_color_npg()
    ggsave("qq_inverse.png", plot, height = 7, width=12)
    """
}
process prune_phenotypes_sib{
    module 'R'
    label 'normal'
    publishDir "result", mode: 'copy', overwrite: 'true'
    afterScript "ls * | grep -v dependent | xargs rm "
    input:
        tuple   val(normalize),
                path(prs),
                val(corThreshold),
                path(showcase),
                path(redundent),
                path(resultSummary),
                path(pheno)
    output: 
        tuple   val(normalize),
                val(corThreshold),
                path("dependent-sib-${corThreshold}")
script:
    """
    #!/usr/bin/env Rscript
    library(magrittr)
    library(data.table)
    
    files <- strsplit("${pheno}", split=" ") %>%
        unlist 
    redundent <- fread("${redundent}", header=F, sep=",")
    ignore.id <- fread("${showcase}") %>%
        .[, c("Field", "FieldID")] %>%
        .[, Field := gsub(",", "", Field)] %>%
        .[Field %in% redundent[, V1], FieldID] %>%
        as.character
    pheno <- NULL

    pb <- txtProgressBar(min = 0, max = length(files), initial = 0,  style = 3) 
    count <- 0
    for(i in files){
        setTxtProgressBar(pb, count)
        count <- count + 1
        name <- strsplit(i, split="\\\\.") %>%
            unlist %>%
            head(n=1) %>%
            as.character 
        if(!name %in% ignore.id){
            if(is.null(pheno)){
                pheno <- fread(i)  %>%
                    .[, c("FID" ,"IID", "Phenotype")]%>%
                    setnames(., "Phenotype", name)
            }else{
                tmp <- fread(i) %>%
                    .[, c("FID" ,"IID", "Phenotype")]%>%
                    setnames(., "Phenotype", name)
                pheno <- merge(pheno, tmp, by=c("FID", "IID"), all=TRUE)
            }
        }
    }
    prs <- fread("${prs}")  %>%
        setnames(., "Trait", "FieldID")
    prioritize<- fread("${resultSummary}") %>%
        .[Type == "${normalize}"]  %>%
        .[, .(N = sum(N_Sib.Reg.Test, na.rm = T)), by=c("FieldID", "Trait")] %>%
        merge(prs, by= c("FieldID")) %>%
        .[order(-N, -R2)]
    # iteratively go through the traits to get the remained & removed phenotypes
    idx.pheno <- NULL
    traits <- prioritize[,FieldID] %>%
        as.character() %>%
        .[. %in% colnames(pheno)]
    removed.pheno <- NULL
    pb <- txtProgressBar(min = 0, max = length(traits), initial = 0,  style = 3) 
    for(i in 1:length(traits)){
        setTxtProgressBar(pb, i)
        if(!traits[i] %in% removed.pheno){
            idx.pheno <- c(idx.pheno, traits[i])
            for(j in (i+1):length(traits)){
                if(!traits[j] %in% removed.pheno & j <= length(traits)){
                    cor <- cor(pheno[,traits[i], with=F], pheno[,traits[j],with=F], use = "pairwise.complete")
                    if(!is.na(cor) & abs(cor) > abs(${corThreshold})){
                        removed.pheno <- c(removed.pheno, traits[j])
                    }
                }
            }
        }
    }
    removed.pheno %<>% unique
    write.table(removed.pheno, "dependent-sib-${corThreshold}")
    """
}
process prune_phenotypes{
    module 'R'
    label 'normal'
    publishDir "result", mode: 'copy', overwrite: 'true'
    afterScript "ls * | grep -v dependent | xargs rm "
    input:
        tuple   val(normalize),
                path(prs),
                val(corThreshold),
                path(showcase),
                path(redundent),
                path(pheno)
    output: 
        tuple   val(normalize),
                val(corThreshold),
                path("dependent-${corThreshold}")
    script:
    """
    #!/usr/bin/env Rscript
    library(magrittr)
    library(data.table)
    files <- strsplit("${pheno}", split=" ") %>%
        unlist 
    redundent <- fread("${redundent}", header=F, sep=",")
    ignore.id <- fread("${showcase}") %>%
        .[, c("Field", "FieldID")] %>%
        .[, Field := gsub(",", "", Field)] %>%
        .[Field %in% redundent[, V1], FieldID] %>%
        as.character
    pheno <- NULL

    pb <- txtProgressBar(min = 0, max = length(files), initial = 0,  style = 3) 
    count <- 0
    for(i in files){
        setTxtProgressBar(pb, count)
        count <- count + 1
        name <- strsplit(i, split="\\\\.") %>%
            unlist %>%
            head(n=1) %>%
            as.character 
        if(!name %in% ignore.id){
            if(is.null(pheno)){
                pheno <- fread(i)  %>%
                    .[, c("FID" ,"IID", "Phenotype")]%>%
                    setnames(., "Phenotype", name)
            }else{
                tmp <- fread(i) %>%
                    .[, c("FID" ,"IID", "Phenotype")]%>%
                    setnames(., "Phenotype", name)
                pheno <- merge(pheno, tmp, by=c("FID", "IID"), all=TRUE)
            }
        }
    }
    prs <- fread("${prs}") %>%
        .[order(-R2)]
    # iteratively go through the traits to get the remained & removed phenotypes
    idx.pheno <- NULL
    traits <- prs[,Trait] %>%
        as.character() %>%
        .[. %in% colnames(pheno)]
    removed.pheno <- NULL
    pb <- txtProgressBar(min = 0, max = length(traits), initial = 0,  style = 3) 
    for(i in 1:length(traits)){
        setTxtProgressBar(pb, i)
        if(!traits[i] %in% removed.pheno){
            idx.pheno <- c(idx.pheno, traits[i])
            for(j in (i+1):length(traits)){
                if(!traits[j] %in% removed.pheno & j <= length(traits)){
                    cor <- cor(pheno[,traits[i], with=F], pheno[,traits[j],with=F], use = "pairwise.complete")
                    if(!is.na(cor) & abs(cor) > abs(${corThreshold})){
                        removed.pheno <- c(removed.pheno, traits[j])
                    }
                }
            }
        }
    }
    removed.pheno %<>% unique
    write.table(removed.pheno, "dependent-${corThreshold}")
    """
}
process partial_method_correlation{
    module 'R'
    label 'normal'
    afterScript "ls * | grep -v cor | xargs rm"
    input:
        tuple   val(normalization),
                val(corThreshold),
                val(prioritize),
                path(dependent),
                val(start),
                val(end),
                val(stat),
                path(permData)
    output:
        tuple   val(normalization),
                val(corThreshold),
                val(prioritize),
                val(stat),
                val("all"),
                path("${end}-${stat}-cor-all-${prioritize}.csv"), emit: all

        tuple   val(normalization),
                val(corThreshold),
                val(prioritize),
                val(stat),
                val("ind"),
                path("${end}-${stat}-cor-ind-${prioritize}.csv"), emit: ind

    script:
    """
    #!/usr/bin/env Rscript
    library(magrittr)
    library(data.table)
    files <- list.files()
    files <- files[!files %in% c("${dependent}")]
    dat <- NULL
    tmp <- NULL
    for(i in files) {
        if ("${end}" != "Ori") {
            tmp <- fread(i) %>%
                .[!Perm %in% c("Ori")] %>%
                .[, Perm  := as.numeric(Perm)] %>%
                .[Perm >= ${start} & Perm <= ${end}]
        }else{
            tmp <- fread(i)
            if(!"Perm" %in% colnames(tmp)){
                tmp[,Perm:= "Ori"]
            }else{
                tmp <- tmp[Perm == "Ori"]
            }
        }
        tmp %<>% 
            .[Type != "raw"] %>%
            .[, .SD, .SDcols = names(.) %like% "Group|FieldID|Perm|Type|Fecundity|Sib.Var.Test|Sib.Reg.Test|PaternalAgeEdu|Illness|Reg.Mean"]
        dat %<>% rbind(., tmp, fill=T)
    }

    dependent <- fread("${dependent}")
    dat %>%
        .[, .SD, .SDcols = names(.) %like% "Group|FieldID|Perm|^${stat}"] %>%
        melt(., id.vars=c("Group", "FieldID", "Perm")) %>%
        .[, variable:=gsub("${stat}_|.adj", "", variable)] %>%
        na.omit %>%
        setkeyv(., c("Group", "Perm", "FieldID")) %>%
        .[., allow.cartesian = T] %>%
        .[, {
            model = cor.test(value, i.value, use = "pairwise.complete")
            list(   r =  model\$estimate,
                    p = model\$p.value,
                    n = sum(!is.na(value) & !is.na(i.value)))
        }, by = c("Group", "Perm", "variable", "i.variable")] %>%
        .[variable != i.variable] %>%
        fwrite(., "${end}-${stat}-cor-all-${prioritize}.csv")

    dat %>%
        .[!FieldID %in% dependent[,x]] %>%
        .[, .SD, .SDcols = names(.) %like% "Group|FieldID|Perm|^${stat}"] %>%
        melt(., id.vars=c("Group", "FieldID", "Perm")) %>%
        .[, variable:=gsub("${stat}_|.adj", "", variable)] %>%
        na.omit %>%
        setkeyv(., c("Group", "Perm", "FieldID")) %>%
        .[., allow.cartesian = T] %>%
        .[, {
            model = cor.test(value, i.value, use = "pairwise.complete")
            list(   r =  model\$estimate,
                    p = model\$p.value,
                    n = sum(!is.na(value) & !is.na(i.value)))
        }, by = c("Group", "Perm", "variable", "i.variable")] %>%
        .[variable != i.variable] %>%
        fwrite(., "${end}-${stat}-cor-ind-${prioritize}.csv")
    """

}


process combine_correlation_results{
    afterScript "ls * | grep -v Empirical | xargs rm"
    label 'normal'
    module 'R'
    publishDir "result", mode: 'copy', overwrite: true
    input:
        tuple   val(normalization),
                val(corThreshold),
                val(prioritize),
                val(stat),
                val(type),
                path(cor)
    output:
        tuple   val(normalization),
                val(corThreshold),
                val(prioritize),
                val(stat),
                val(type),
                path("Empirical-${normalization}-${corThreshold}-${stat}-${type}-${prioritize}.csv")
    script:
    """
    #!/usr/bin/env Rscript
    library(magrittr)
    library(data.table)
    library(forcats)
    files <- list.files()
    res <- NULL
    for(i in files){
        res %<>% rbind(., fread(i))
    }
    ori <- res[Perm=="Ori"] %>%
        setnames(., c("r", "p", "n"),c("obs.r", "obs.p", "obs.n")) %>%
        .[,-c("Perm")]
    perm <- res[Perm != "Ori"]
    if(nrow(perm) == 0){
        # Not running permutation
        ori[, .(  obs.r = unique(obs.r),
                    obs.p = unique(obs.p),
                    emp.r = unique(obs.r),
                    emp.p = unique(obs.p),
                    obs.n = unique(obs.n),
                    emp.n = unique(obs.n)),
                by = c("Group", "variable", "i.variable")] %>%
            .[, variable := fct_relevel(variable, c("Reg.Mean", "Sib.Var.Test", "Sib.Reg.Test", "Fecundity",  "PaternalAgeEdu", "IllnessTest", "IllnessEdu"))] %>%
            .[, i.variable := fct_relevel(i.variable, c("Reg.Mean", "Sib.Var.Test", "Sib.Reg.Test", "Fecundity",  "PaternalAgeEdu", "IllnessTest", "IllnessEdu"))] %>%
            .[as.numeric(variable) < as.numeric(i.variable)] %>%
            fwrite(., "Empirical-${normalization}-${corThreshold}-${stat}-${type}-${prioritize}.csv")
    }else{
        res[Perm != "Ori"] %>%
            merge(., ori) %>%
            .[, .(  obs.r = unique(obs.r),
                    obs.p = unique(obs.p),
                    emp.r = mean(obs.r-r),
                    emp.p = (sum(obs.p > p)+1)/(.N+1)),
                by = c("Group", "variable", "i.variable")] %>%
            .[, variable := fct_relevel(variable, c("Reg.Mean", "Sib.Var.Test", "Sib.Reg.Test", "Fecundity",  "PaternalAgeEdu", "IllnessTest", "IllnessEdu"))] %>%
            .[, i.variable := fct_relevel(i.variable, c("Reg.Mean", "Sib.Var.Test", "Sib.Reg.Test", "Fecundity",  "PaternalAgeEdu", "IllnessTest", "IllnessEdu"))] %>%
            .[as.numeric(variable) < as.numeric(i.variable)] %>%
            fwrite(., "Empirical-${normalization}-${corThreshold}-${stat}-${type}-${prioritize}.csv")
    }
    """
}

process heatmap{
    label 'normal'
    module 'R'

    publishDir "result/fig", mode: 'copy', overwrite: true
    input:
        tuple   val(normalization),
                val(corThreshold),
                val(prioritize),
                val(stat),
                val(type),
                path(dat)
    output:
        path("heatmap-${normalization}-${corThreshold}-${stat}-${type}-${prioritize}.png")
    script:
    """
    #!/usr/bin/env Rscript
    library(magrittr)
    library(data.table)
    library(forcats)
    library(ggplot2)
    library(ggsci)
    tests <- c("Reg.Mean", 
        "Sib.Var.Test", 
        "Sib.Reg.Test", 
        "Fecundity",  
        "PaternalAgeEdu", 
        "IllnessTest", 
        "Illness")
    dat <- fread("${dat}") %>%
        .[variable != "Sib.Var.Test"] %>%
        .[i.variable != "Sib.Var.Test"] %>%
        .[, variable := fct_relevel(variable, tests)] %>%
        .[, i.variable := fct_relevel(i.variable, tests)] %>%
        .[variable %in% tests & i.variable %in% tests] %>%
        .[, variable := fct_recode(variable, `PRS RM`="Reg.Mean", `Sibling RM` = "Sib.Reg.Test", `Paternal Age`="PaternalAgeEdu", `Num of illnesses`="Illness", `PRS Vs Num of illnesses`="IllnessTest")] %>%
        .[, i.variable := fct_recode(i.variable, `PRS RM`="Reg.Mean", `Sibling RM` = "Sib.Reg.Test", `Paternal Age`="PaternalAgeEdu", `Num of illnesses`="Illness", `PRS Vs Num of illnesses`="IllnessTest")] %>%
        .[, r.lab := format(round(obs.r, 2), nsmall=2)] %>%
        .[, Significance := "p >= 0.05"] %>%
        .[obs.p < 0.05, Significance := "p < 0.05" ] %>%
        .[obs.p < 0.05/30, Significance := paste0("p < 0.0017")] %>%
        .[, Significance := fct_relevel(Significance, "p >= 0.05", "p < 0.05")] %>%
        .[, direction := sign(obs.r)] %>%
        .[Group == "Lower" & (variable == "Fecundity" | i.variable == "Fecundity"), direction := -1 *direction] %>%
        .[Group == "Upper" & 
            (   (   variable %in% c("PRS Vs Num of illnesses", "PRS RM", "Fecundity", "Sibling RM") & 
                    !i.variable %in% c("PRS RM", "Fecundity", "PRS Vs Num of illnesses", "Sibling RM")) |
                (   i.variable %in% c("PRS Vs Num of illnesses", "PRS RM", "Fecundity", "Sibling RM") & 
                    !variable %in% c("PRS RM", "Fecundity", "PRS Vs Num of illnesses", "Sibling RM"))
            ), direction := -1 * direction] %>%
        .[, Expected := "Yes"] %>%
        .[direction < 0, Expected := "No"]
    g <- dat %>%
        ggplot(aes(x = variable, y = i.variable, fill = Expected, label = r.lab)) +
        geom_tile(aes(size = Significance), color="black", height = 0.99, width = 0.99) + 
        theme_classic() + 
        geom_text() +
                labs(fill = "Expected Direction") +
                #scale_fill_manual(values = c("#ff8080", "#00bfff"))+
                scale_fill_npg() +
                scale_size_manual(
                    values = c(0, 0.3, 1),
                    breaks = levels(dat[,Significance]),
                    labels = levels(dat[,Significance]),
                    name = "Level of significance",
                    guide = guide_legend(override.aes = list(fill = "grey"))
                )+
                theme(
                    axis.title = element_blank(),
                    axis.text = element_text(size = 14),
                    axis.text.x = element_text(hjust = 1, angle = 45),
                    legend.title = element_text(size = 14, face = "bold"),
                    legend.text = element_text(size = 14),
                    strip.text = element_text(size = 14, face = "bold")
                ) +
                facet_wrap(~Group)
    ggsave("heatmap-${normalization}-${corThreshold}-${stat}-${type}-${prioritize}.png", g, height=7, width=10)
    """

}

process reg_mean_quantile_plots{
    label 'normal'
    module 'R'
    publishDir "result/fig/reg", mode: 'copy', overwrite: true
    input:
        tuple   val(fieldID),
                val(type),
                val(normalize),
                path(info),
                path(showcase)
    output:
        path("${fieldID}-${normalize}-exp.png")
        path("${fieldID}-${normalize}-exp-no-legend.png")
        path("${fieldID}-${normalize}-scatter.png")
        path("${fieldID}-${normalize}.png")
    script:
    """
    #!/usr/bin/env Rscript
    library(magrittr)
    library(data.table)
    library(forcats) 
    library(ggplot2)
    library(ggsci)
    reg.mean.plot <- function(x, title, name="${fieldID}-${normalize}"){
        global.theme <- theme_classic() + theme(
                    axis.title = element_text(face="bold", size=16),
                    axis.text = element_text(size=14, hjust=1, angle = 45),
                    axis.title.y = element_blank(),
                    axis.text.y = element_blank(),
                    axis.ticks.y = element_blank(),
                    legend.title = element_blank(),
                    legend.text = element_text(size=14)
                )

        plot.dat <- x %>%
            .[, .(m=mean(PRS), se=sd(PRS)/sqrt(.N)), by=c("Pheno.Quant", "Group")] %>%
            .[Group %in% "Abnormal", Group:= "Normal"]
        g <- plot.dat %>%
            ggplot(aes( x=Pheno.Quant, 
                        y=m, 
                        ymin=m-1.96*se, 
                        ymax=m+1.96*se, 
                        color=fct_relevel(Group, "Upper", "Normal", "Lower", "Abnormal")))+
                geom_pointrange()+
                global.theme +
                scale_color_manual(values=c("#0E84B4FF","#9E8356FF","#B50A2AFF", "#D1B79EFF"))+
                labs(x="Phenotype Quantile", y="Polygenic Score")+
                ggtitle(title)
        ggsave(paste0(name, ".png"), g)
        g <- x %>%
            copy %>%
            .[Group %in% "Abnormal", Group:= "Normal"] %>%
            ggplot(aes( x=Pheno.Quant, 
                        y=PRS, 
                        color=fct_relevel(Group, "Upper", "Normal", "Lower", "Abnormal")))+
                geom_jitter()+
                global.theme +
                scale_color_manual(values=c("#0E84B4FF","#9E8356FF","#B50A2AFF", "#D1B79EFF"))+
                labs(x="Phenotype Quantile", y="Polygenic Score")+
                ggtitle(title)
        ggsave(paste0(name, "-scatter.png"), g)
        training <- lm(PRS ~ Phenotype, x[Group == "Normal"])
        group.mean <- x[!Group %in% c("Normal"), .(Phenotype=mean(Phenotype), N=.N), by=c("Group", "Pheno.Quant")] %>%
            .[, se := predict(training, newdata=.SD, se.fit=T)\$se.fit, by = c("Group", "Pheno.Quant")] %>%
            .[, -c("N")]
        expected <- x[Group != "Normal",
            .( PRS = predict(training, newdata = .SD)),
                 by=c("Group","Pheno.Quant")] %>%
                .[, Type := "Expected"] %>%
                .[, .(m=mean(PRS)), by=c("Pheno.Quant", "Group", "Type")] %>%
                merge(group.mean)
        plot.dat <- x %>%
            .[, c("Pheno.Quant", "Group", "PRS")] %>%
            .[, Type := "Observed"] %>%
            .[, .(m=mean(PRS), se=sd(PRS)/sqrt(.N)), by=c("Pheno.Quant", "Group", "Type")] %>%
            rbind(., expected[,-c("Phenotype")]) %>%
            .[Group %in% "Abnormal", Group:= "Excluded from Model"]

        g <- plot.dat %>%
            ggplot(aes( x=Pheno.Quant, 
                        y=m, 
                        ymin=m-1.96*se, 
                        ymax=m+1.96*se, 
                        color=fct_relevel(Group, "Upper", "Normal", "Lower", "Excluded from Model"),
                        shape=fct_relevel(Type, "Observed", "Expected")))+
                geom_pointrange()+
                global.theme +
                scale_color_manual(values=c("blue","grey34","red", "grey"))+
                labs(x="Phenotype Quantile", y="Polygenic Score")+
                ggtitle(title) +
                theme(legend.position ="bottom")
        ggsave(paste0(name, "-exp.png"), g, width=10)

        g <- g + theme(legend.position="none")
        ggsave(paste0(name, "-exp-no-legend.png"), g)
    }
    fieldID <- "${fieldID}"
    showcase <- fread("${showcase}") %>%
        .[,c("Field","FieldID")] %>%
        .[,Field:=gsub(",","", Field)] %>%
        .[,FieldID := as.factor(FieldID)]
    name <- fieldID
    name <- showcase[FieldID %in% fieldID, Field]
    dat <- fread("${info}") %>%
        .[is.na(Sibling)]
    reg.mean.plot(dat, name)
    """
}


process reg_mean_quantile_plots_output{
    label 'normal'
    module 'R'
    publishDir "result/fig/quant/inv/${followUp_type}", mode: 'symlink', pattern: "*inverse-quant.csv", overwrite: true
    publishDir "result/fig/quant/raw/${followUp_type}", mode: 'symlink', pattern: "*raw-quant.csv", overwrite: true
    input:
        tuple   val(fieldID),
                val(type),
                val(normalize),
                val(followUp_type),
                path(info),
                path(showcase)
    output:
        path("${fieldID}-${normalize}-quant.csv")
    script:
    """
    #!/usr/bin/env Rscript
    library(magrittr)
    library(data.table)
    library(forcats) 
    reg_mean_dat <- function(x, trait, name="${fieldID}-${normalize}-quant.csv"){
        plot.dat <- x %>%
            .[, .(mean=mean(PRS), se=sd(PRS)/sqrt(.N)), by=c("Pheno.Quant", "Group")] %>%
            .[Group %in% "Abnormal", Group:= "Normal"]
    
        training <- lm(PRS ~ Phenotype, x[Group == "Normal"])
        group.mean <- x[, .(Phenotype=mean(Phenotype), N=.N), by=c("Group", "Pheno.Quant")] %>%
            .[, se := predict(training, newdata=.SD, se.fit=TRUE)\$se.fit, by = c("Group", "Pheno.Quant")] %>%
            .[, -c("N")]
        expected <- x[,
            .( PRS = predict(training, newdata = .SD)),
                 by=c("Group","Pheno.Quant")] %>%
                .[, Type := "Expected"] %>%
                .[, .(mean=mean(PRS)), by=c("Pheno.Quant", "Group", "Type")] %>%
                merge(group.mean)
        x %>%
            .[, c("Pheno.Quant", "Group", "PRS")] %>%
            .[, Type := "Observed"] %>%
            .[, .(mean=mean(PRS), se=sd(PRS)/sqrt(.N)), by=c("Pheno.Quant", "Group", "Type")] %>%
            rbind(., expected[,-c("Phenotype")]) %>%
            .[Group %in% "Abnormal", Group:= "Excluded from Model"] %>%
            .[order(Pheno.Quant)] %>%
            dcast( Pheno.Quant+Group~Type, value.var=c("mean", "se")) %>%
            .[, Trait := trait] %>%
            fwrite(name)
    }
    fieldID <- "${fieldID}"
    showcase <- fread("${showcase}") %>%
        .[,c("Field","FieldID")] %>%
        .[,Field:=gsub(",","", Field)] %>%
        .[,FieldID := as.factor(FieldID)]
    name <- fieldID
    name <- showcase[FieldID %in% fieldID, Field]
    dat <- fread("${info}") %>%
        .[is.na(Sibling)]
    reg_mean_dat(dat, name)
    """
}
process sib_reg_quantile_plots{
    label 'normal'
    module 'R'
    publishDir "result/fig/sib", pattern: "*.png", mode: 'copy', overwrite: true
    publishDir "result/serverOnly", pattern: "*.csv", mode: 'copy', overwrite: true
    input:
        tuple   val(fieldID),
                val(type),
                val(normalize),
                path(info),
                path(showcase)
    output:
        path("${fieldID}-${normalize}-sib-exp.png") optional true
        path("${fieldID}-${normalize}-sib-exp-no-legend.png") optional true
        path("${fieldID}-${normalize}-sib.png")
        path("${fieldID}-${normalize}-sib-scatter.png")
        path("*-sib-plot.csv")
    script:
    """
    #!/usr/bin/env Rscript
    library(magrittr)
    library(data.table)
    library(forcats)
    library(ggplot2)
    library(ggsci)
    sib.reg.plot <- function(x, title, name="${fieldID}-${normalize}-sib"){
        global.theme <- theme_classic() + theme(
                    axis.title = element_text(face="bold", size=16),
                    axis.text = element_text(size=14, hjust=1, angle = 45),
                    axis.title.y = element_blank(),
                    axis.text.y = element_blank(),
                    axis.ticks.y = element_blank(),
                    legend.title = element_blank(),
                    legend.text = element_text(size=14)
                )
        # Sibling = index Sib of current sample
        # Samples without Sibling columns are included in other analyses
        # Here, we want the quantile of the index sib, but phenotype of the 
        # observed sib
        groups <- c("Normal", "Lower", "Upper")
        # First, extract the index Sibling's information
        idx.of.sib <- x[IID %in% Sibling] %>%
            # We want their group and phenotype quantile
            .[, c("IID", "Group", "Pheno.Quant", "Phenotype")] %>%
            setnames(., "Phenotype", "Idx.Pheno") %>%
            # Now, we want the phenotype of the sibling
            merge(., x[,c("Sibling", "Phenotype")], by.x="IID", by.y="Sibling") %>%
            na.omit
        fwrite(idx.of.sib,paste0(name, "-sib-plot.csv"))
        remove.group <- idx.of.sib[, .N, by = Group][N < 10, Group]
        exist.group <- groups %>%
            .[. %in% idx.of.sib[,Group]] %>%
            .[!. %in% remove.group]

        plot.dat <- idx.of.sib %>%
            .[, .(m=mean(Phenotype), se=sd(Phenotype)/sqrt(.N)), by=c("Pheno.Quant", "Group")] %>%
            .[Group %in% "Abnormal", Group:= "Normal"]
        g <- plot.dat %>%
            ggplot(aes( x=Pheno.Quant, 
                        y=m, 
                        ymin=m-1.96*se, 
                        ymax=m+1.96*se, 
                        color=fct_relevel(Group, "Upper", "Normal", "Lower", "Abnormal")))+
                geom_pointrange()+
                global.theme +
                scale_color_manual(values=c("#0E84B4FF","#9E8356FF","#B50A2AFF", "#D1B79EFF"))+
                labs(x="Phenotype Quantile", y="Sibling Phenotype")+
                ggtitle(title)
        ggsave(paste0(name, ".png"), g)
        
        g <- idx.of.sib %>%
            copy %>%
            .[Group %in% "Abnormal", Group:= "Normal"] %>%
            ggplot(aes( x=Pheno.Quant, 
                        y=Phenotype, 
                        color=fct_relevel(Group, "Upper", "Normal", "Lower", "Abnormal")))+
                geom_jitter()+
                global.theme +
                scale_color_manual(values=c("#0E84B4FF","#9E8356FF","#B50A2AFF", "#D1B79EFF"))+
                labs(x="Phenotype Quantile", y="Sibling Phenotype")+
                ggtitle(title)
        ggsave(paste0(name, "-scatter.png"), g)
        if(length(exist.group) > 1 & "Normal" %in% exist.group){
            # We want to train the model based on the quantile
            training <- lm(Phenotype ~ Idx.Pheno, idx.of.sib[Group == "Normal"])
            group.mean <- idx.of.sib[Group %in% exist.group & Group != "Normal", 
                .(Idx.Pheno=mean(Idx.Pheno), N=.N), by=c("Group", "Pheno.Quant")] %>%
                .[, se := predict(training, newdata=.SD, se.fit=T)\$se.fit, by = c("Pheno.Quant", "Group")] 
            
            expected <- idx.of.sib[Group %in% exist.group & Group != "Normal",
                .(Phenotype = predict(training, newdata = .SD)),
                by = c("Group", "Pheno.Quant")] %>%
                # This can be confusing, but in our use case, there should only
                # be one extreme quantile, so Pheno.Quant in Upper / Lower should
                # equal to Group. Type was added so that the Type column
                .[, .(m=mean(Phenotype)), by=c("Pheno.Quant", "Group")] %>%
                .[, Type := "Expected"] %>%
                merge(group.mean) 
            plot.dat <- idx.of.sib %>%
                .[, c("Pheno.Quant", "Group", "Phenotype")] %>%
                .[, .(m=mean(Phenotype), se=sd(Phenotype)/sqrt(.N)), by=c("Pheno.Quant", "Group")] %>%
                .[, Type := "Observed"] %>%
                rbind(., expected[,-c("N", "Idx.Pheno")]) %>%
            .[Group %in% "Abnormal", Group:= "Excluded from Model"]
            
            g <- plot.dat %>%
                ggplot(aes( x = Pheno.Quant, 
                            y = m, 
                            ymin = m - 1.96*se, 
                            ymax = m + 1.96*se, 
                            color=fct_relevel(Group, "Upper", "Normal", "Lower", "Excluded from Model"),
                            shape=fct_relevel(Type, "Observed", "Expected")))+
                    geom_pointrange()+
                    global.theme +
                    scale_color_manual(values=c("blue","grey34","red", "grey"))+
                    labs(x="Phenotype Quantile", y="Sibling Phenotype")+
                    ggtitle(title)
            ggsave(paste0(name, "-exp.png"), g)
            g <- g + theme(legend.position="none")
            ggsave(paste0(name, "-exp-no-legend.png"), g)
        }
    }
    fieldID <- "${fieldID}"
    showcase <- fread("${showcase}") %>%
        .[,c("Field","FieldID")] %>%
        .[,Field:=gsub(",","", Field)] %>%
        .[,FieldID := as.factor(FieldID)]
    name <- fieldID
    name <- showcase[FieldID %in% fieldID, Field]
    dat <- fread("${info}")
    sib.reg.plot(dat, name)
    """
}
process plot_relationship{
    label 'normal'
    module 'R'
    publishDir "result/fig/relationship", pattern: "*png", mode: 'copy', overwrite: true
    publishDir "result/", pattern: "*csv", mode: 'copy', overwrite: true
    input:
        tuple   val(normalization),
                val(corThreshold),
                val(prioritize),
                path(dependent),
                path(showcase),
                val(stat),
                path(permData),
                path(label)
    output:
        path("*.png")
        path("relationship_${prioritize}_${stat}_data.csv")
    script:
    lab = label? label : "NULL"
    """
    #!/usr/bin/env Rscript
    library(magrittr)
    library(data.table)
    library(ggplot2)
    library(ggrepel)
    library(forcats)
    library(ggsci)
    files <- list.files()
    files <- files[!files %in% c("${dependent}", "${showcase}", "${lab}")]

    dat <- NULL
    tmp <- NULL
    for (i in files) {
        tmp <- fread(i)
        if (!"Perm" %in% colnames(tmp)) {
            tmp[, Perm := "Ori"]
        } else{
            tmp <- tmp[Perm == "Ori"]
        }
        tmp %<>%
            .[Type != "raw"] %>%
            .[, .SD, .SDcols = names(.) %like% "Group|FieldID|Perm|Type|Fecundity|Sib.Reg.Test|PaternalAgeEdu|Illness|Reg.Mean"]
        dat %<>% rbind(., tmp, fill = T)
    }
    dependent <- fread("${dependent}")
    showcase <- fread("${showcase}") %>%
        .[, c("Field", "FieldID", "Category", "Path")] %>%
        .[, Field := gsub(",", "", Field)]
    res <- merge(dat, showcase, by = "FieldID") %>%
        .[, CategoryName := Path] %>%
        .[Category %in% c("100009", "100010"), CategoryName := "Anthropometric"] %>%
        .[Category %in% c("17518", "100081"), CategoryName := "Blood assays"] %>%
        .[CategoryName %like% "Brain MRI", CategoryName := "Brain MRI"] %>%
        .[CategoryName %like% "Diet", CategoryName := "Diet"] %>%
        .[CategoryName %like% "Lifestyle and environment",
        CategoryName := "Lifestyle and environment"] %>%
        .[CategoryName %like% "Sex-specific factors", CategoryName := "Sex-specific factors"] %>%
        .[CategoryName %like% "Physical activity measurement", CategoryName :=
            "Physical activity measurement"] %>%
        .[CategoryName %like% "Cognitive function" |
            CategoryName %like% "Process durations", CategoryName := "Cognitive function"] %>%
        .[CategoryName %like% "Eye measures", CategoryName := "Eye measures"] %>%
        .[CategoryName %like% "Physical measures", CategoryName := "Anthropometric"] %>%
        .[CategoryName %like% "Imaging", CategoryName := "Others"] %>%
        .[CategoryName %like% "[M|m]edica" |
            CategoryName %like% "health", CategoryName := "Health and medical history"] %>%
        .[CategoryName %like% "Sociodemographics" |
            CategoryName %like% "Work" |
            CategoryName %like% "Deprivation" |
            CategoryName %like% "Early life factors" , CategoryName := "Sociodemographics"] %>%
        .[CategoryName %like% "Urine", CategoryName := "Others"]
    
    label <- NULL
    melt.id <- c("Group", "FieldID", "CategoryName", "Type", "${stat}_Reg.Mean")
    if("${lab}" != "NULL"){
        label <- fread("${lab}", header = F) %>%
        setnames(., c("V1", "V2", "V3"), c("Group", "FieldID", "lab"))
        res <- merge(res, label, by = c("FieldID", "Group"), all.x = TRUE)
        melt.id <- c(melt.id, "lab")
    }
    res.stat <-
        res[, .SD, .SDcols = names(res) %like% "^${stat}|Group|FieldID|^lab|Type|CategoryName"] %>%
        melt(.,
            id.vars = melt.id) %>%
        .[, variable := gsub("${stat}_", "", variable)] %>%
        .[, variable := gsub(".adj", "", variable)] %>%
        na.omit(cols = "value") %>%
        .[, Statistic := ifelse("${stat}" == "t.stat", "T-statistics", "P-value")] %>%
        .[, Dependence := "All"] %>%
        setnames(., "${stat}_Reg.Mean", "Reg.Mean")
    
    get_plot <- function(x, filter, ytest, stat, suffix){
        dat <- x[variable==filter] 
        if(nrow(dat) == 0){
            return()
        }
        plot <- dat %>%
        ggplot(aes(x=Reg.Mean, y=value, label=FieldID))+
            geom_point(aes(color=CategoryName), size = 1.5)+
            scale_color_igv()+
            theme_classic()+
            theme(  axis.title = element_text(face="bold", size=16),
                    axis.text = element_text(size=14),
                    legend.text = element_text(size=14),
                    legend.title = element_blank(),
                    legend.box.background= element_rect(),
                    legend.position = c("bottom"),
                    strip.text = element_text(size=16, face="bold"))+
            labs(   x = paste0(stat, " of PRS RM Test"),
                    y = paste0(stat, " of ",ytest))+
            guides(color = guide_legend(nrow = 3))+
            geom_smooth( color="black", method='lm', formula=y~x, se=FALSE)+
            facet_wrap(~Group, scales="free")
            ggsave(paste0(ytest, suffix), plot, height=10, width=15 )
            if("lab" %in% colnames(dat)){
                plot <- plot + geom_text_repel(data= dat, aes(label = lab),
                    box.padding = 1, 
                    point.padding = 0.5,
                    segment.size  = 0.5,
                    max.overlaps = 50)
                ggsave(paste0(ytest, "-annot", suffix), plot, height=10, width=15 )
            }
    }
    test.pairs <-
    data.table(
        test = c(
            "Illness",
            "Sib.Var.Test",
            "Sib.Reg.Test",
            "PaternalAgeEdu",
            "IllnessTest",
            "Fecundity"
        ),
        name = c(
            "Num of illnesses Test",
            "Sibling Variance",
            "Sibling RM Test",
            "Paternal Age",
            "PRS Vs Num of illnesses",
            "Fecundity"
        )
    )
    for(i in 1:nrow(test.pairs)){
        get_plot(res.stat, test.pairs[i,test], test.pairs[i,name], 
            ifelse("${stat}" == "t.stat", "T-statistics", "P-value"), "-${stat}-all-${prioritize}.png")
        get_plot(res.stat[!FieldID %in% dependent[,x]], test.pairs[i,test], test.pairs[i,name], 
            ifelse("${stat}" == "t.stat", "T-statistics", "P-value"), "-${stat}-ind-${prioritize}.png")
        
    }
    res.stat[, Independent:=FALSE] %>%
        .[!FieldID %in% dependent[,x], Independent:=TRUE]
    fwrite(res.stat, "relationship_${prioritize}_${stat}_data.csv")
    """
}

process clive_prs{ 
    module 'R'
    label 'normal'
    errorStrategy 'ignore'
    publishDir "result/clive/${followUp_type}", mode: 'symlink', overwrite: true
    input:
        tuple   val(fieldID),
                val(type),
                val(normalize),
                val(followUp_type),
                path(pheno),
                path(sibs),
                path(summary),
                path(best)
    output:
        tuple   val(fieldID),
                val(type),
                val(normalize),
                val(followUp_type),
                path("${fieldID}-${normalize}-clive.csv")
    script:
    """
    #!/usr/bin/env Rscript
    library(data.table)

    assign.to.quants <- function( y, n ){
        q <- quantile( y, 1:(n-1)/n, na.rm=TRUE )
        y.cat <- sapply( lapply( y, '>=', q ), sum )
        return(y.cat)
    }

    prs.test <- function( prs, y, K=0.01 ){# Test for residuals mean=0 in the tail(s)
        fit <- lm( prs ~ y )

        # Test upper tail "regression to mean"
        T <- quantile( y, 1-K, na.rm=TRUE )

        ptr <- which(y>T)
        test <- t.test( fit\$residual[ptr] )#, alternative='less' )
        p2 <- test\$p.value
        effect2 <- test\$estimate
        ci2 <- test\$conf.int
        
        # Test lower tail "regression to mean"
        T <- quantile( y, K, na.rm=TRUE )
        ptr <- which(y<T)
        test <- t.test( fit\$residual[ptr] )#, alternative='greater' )
        p1 <- test\$p.value
        effect1 <- test\$estimate
        ci1 <- test\$conf.int

        ms = sd(prs) 
        ret <- c( effect1, ci1, p1, effect2, ci2, p2, ms, effect1/ms, ci1/ms,effect2/ms, ci2/ms)
        names(ret) <- c( 'effect.lower', 'ci.lower.lower', 'ci.lower.upper', 'p.lower',
                        'effect.upper',' ci.upper.lower',' ci.upper.upper', 'p.upper' ,'sd',
                        're.lower','ri.lower.lower','ri.lower.upper','re.upper','ri.upper.lower','ri.upper.upper')            
                        
        return(ret)
    }
    prs.test.qc <- function( prs, y, n.q=100, K=0.1, K1=0.9 ){
        q <- assign.to.quants( y, n.q )
        ptr <- which( n.q*K <= q&q < n.q*K1 )
        fit <- lm( prs ~ y, subset=ptr )
        p <- vector()
        for( j in unique(q[ptr]) ){
            ptr1 <- which( q[ptr]==j )
            p <- c( p, t.test( fit\$residuals[ptr1] )\$p.value )
        }
        qc.test <- ifelse( min(p) < 0.05/length(unique(q[ptr])), 'FAIL', 'PASS' )
        return(c( qc.test, min(p)*length(unique(q[ptr])) ))
    }
    prs.test.emp <- function( prs, y, n.q=100 ){
        stat <- vector()
        fit <- lm( prs ~ y )

        q <- assign.to.quants( y, n.q )
        for( i in 1:n.q ){
            ptr <- which(q==(i-1))
            test <- t.test( fit\$residual[ptr] )
            stat[i] <- test\$statistic
        }
        r1 <- rank(-stat)
        r2 <- rank(stat)
        p <- c( r1[1]/n.q, r2[100]/n.q )
        return(p)
    }
    prs <- na.omit(fread("${best}"))[In_Regression == "Yes"]
    pheno <- na.omit(fread("${pheno}"))
    ids <- intersect( prs\$IID, pheno\$IID )
    size <- length(ids) 
    prs <- prs[match( ids, prs\$IID ),]
    pheno <- pheno[match( ids, pheno\$IID ),]

    test <- prs.test( prs\$PRS, pheno\$Phenotype )
    test.empirical <- prs.test.emp( prs\$PRS, pheno\$Phenotype )
    qc <- prs.test.qc( prs\$PRS, pheno\$Phenotype )
    t_name = "${fieldID}"
    out <- data.frame( t_name, size, t(c(test, test.empirical, as.numeric(qc[2]))), qc[1] )
    colnames(out) <- c( 'fieldID', 'size', 
                'effect.lower', 'ci.lower.lower', 'ci.lower.upper', 'p.lower',
                'effect.upper','ci.upper.lower','ci.upper.upper', 'p.upper',
                'sd','re.lower','ri.lower.lower','ri.lower.upper','re.upper','ri.upper.lower','ri.upper.upper',       
                'p.emp.lower','p.emp.upper','p.qc','QC')
    setDT(out)
    out[, normalization := "${normalize}"]
    #out <- as.data.table(t(out))
    fwrite(out, "${fieldID}-${normalize}-clive.csv")
    """
}


process tade_prs_predictivity {
    label 'normal'
    publishDir "result/tade/tade_prs_predictive/${followUp_type}", mode: 'symlink',  overwite: true
    input:
        tuple   val(fieldID),
                val(type),
                val(normalize),
                val(followUp_type),
                path(pheno),
                path(sibs),
                path(summary),
                path(best),
                path(tade_predictive)
    output:
        tuple   val(fieldID),
                val(type),
                val(normalize),
                val(followUp_type),
                path("${fieldID}-${normalize}-tade-predictivity.csv")

    script:
    """
    pyenv local 3.7.2
    ./${tade_predictive} ${best} ${pheno} > "${fieldID}-${normalize}-tade-predictivity.csv"
    """
}

process tade_selection{
    label 'normal'
    publishDir "result/tade/tade_selection/${followUp_type}", mode: 'symlink',  overwite: true
    input:
        tuple   val(fieldID),
                val(type),
                val(normalize),
                val(followUp_type),
                path(pheno),
                path(sibs),
                path(paternalAge),
                path(fecundity),
                path(illness),
                path(tade_select)
    output:
        tuple   val(fieldID),
                val(type),
                val(normalize),
                val(followUp_type),
                path("${fieldID}-${normalize}-tade-selection.csv")
    script:
    """
    pyenv local 3.7.2
    ./${tade_select} ${fecundity} ${pheno} > "${fieldID}-${normalize}-tade-selection.csv"
    """
}
process tade_health_tail{
    module 'R'
    label 'normal'
    publishDir "result/tade/health_tail/${followUp_type}", mode: 'symlink',  overwite: true
    input:
        tuple   val(fieldID),
                val(type),
                val(normalize),
                val(followUp_type),
                path(pheno),
                path(sibs),
                path(paternalAge),
                path(fecundity),
                path(illness)
    
    output:
        tuple   val(fieldID),
                val(type),
                val(normalize),
                val(followUp_type),
                path("${fieldID}-${normalize}-health-tail.csv"), optional: true
    script:
    """
    #!/usr/bin/env Rscript
    library(data.table)
    pheno <- fread("${pheno}")
    fecundity <- fread("${fecundity}") |>
        merge(fread("${paternalAge}")) |>
        merge(fread("${illness}"))

    fecundity_variable <- colnames(fecundity[,-c("FID", "IID", "Age","Sex","Centre")])
    dat <- merge(pheno, fecundity, by = c("FID", "IID"))
    tryCatch({
        dat_long <- melt(dat, id.vars =c("FID", "IID", "Phenotype"), measure.vars = fecundity_variable) |>
            na.omit()
        dat_long[,rank := rank(Phenotype)/.N * 100, by = variable]

        mean_variables <- dat_long[,.(pv0 = t.test(.SD[floor(rank)>=5 & floor(rank) < 95, value], .SD[floor(rank)==0, value])\$p.value,
                    pv99 = t.test(.SD[floor(rank)>=5 & floor(rank) < 95, value], .SD[floor(rank)==99, value])\$p.value,
                    mT = mean(.SD[floor(rank) >=5 & floor(rank) < 95, value]), 
                    m0=mean(.SD[floor(rank) == 0, value]), 
                    m99 = mean(.SD[floor(rank)==99, value])), by = variable]
                    
        mean_variables[,fc0 := ifelse(m0 > mT, m0/mT, -1 * mT/m0)]
        mean_variables[,fc99 := ifelse(m99 > mT, m99/mT, -1 * mT/m99)]
        setnames(mean_variables, c("variable", "mT","m0","m99"), c("Fecundity_Trait", "bodyMean", "mean0", "mean1"))
        mean_variables[,Trait := "${fieldID}"]
        fwrite(mean_variables, "${fieldID}-${normalize}-health-tail.csv")
        }, error = function(cond){
        # Do nothing
        NA
    })
    """
}
