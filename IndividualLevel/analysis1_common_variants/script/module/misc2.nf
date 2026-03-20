
process filter_snp{
    publishDir "extra/${fieldID}", mode: 'symlink'
    module 'R'
    label 'normal'
    input:
        tuple   val(fieldID),
                val(type),
                val(normalize),
                path(summary),
                path(best),
                path(snp)
    output: 
        tuple   val(fieldID),
                val(type),
                val(normalize),
                path("${fieldID}-${normalize}.prsSNP") 
      
    
    """
    #!/usr/bin/env Rscript
    library(data.table)
    sum<-fread("${summary}")
    threshold <- as.numeric(sum[1, Threshold])
    keep_snp <- fread("${snp}")[P<=threshold]
    write.table(data.frame(SNP=keep_snp), "${fieldID}-${normalize}.prsSNP", row.names = FALSE, col.names = FALSE, quote = FALSE)
     """
}


process make_geno{
    publishDir "extra/${fieldID}", mode: 'symlink'
    module 'plink'
    label 'prsice'
    input:
        tuple   val(fieldID),
                val(type),
                val(normalize),
                path(prsSNP),
                path(summary),
                path(best),
                path(bed),
                path(bim),
                path(fam)
    output: 
        tuple   val(fieldID),
                val(type),
                val(normalize),
                path("${fieldID}-${normalize}.raw.gz")
    script:
        base = bed.baseName
    
    """
       plink \
       --bfile ${base} \
       --extract ${prsSNP} \
       --keep ${best} \
       --recode A \
       --out "${fieldID}-${normalize}" &&
        gzip "${fieldID}-${normalize}.raw"
    """
}


process get_allele_count{
    publishDir "extra/${fieldID}", mode: 'symlink'
    module 'R'
    label 'prsice'

    input:
        tuple   val(fieldID),
                val(type),
                val(normalize),
                path(assoc),
                path(pheno),
                path(geno_ct)
    
    output:
        tuple   val(fieldID),
                val(type),
                val(normalize),
                path("${fieldID}-${normalize}.pos.count"),
                path("${fieldID}-${normalize}.neg.count")
    
    
    script:
    """
    #!/usr/bin/env Rscript
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
        
    subtract <- function(x){
        x2 <- ifelse(x == 2, x - 1, x)
        return(x2)
    }

    set_rec <- function(x){
        x2=x-1
        x2[x2 < 0] <- 0
        return(x2)
    }

    genotype=fread("${geno_ct}")
    colnames(genotype) = gsub("_.\$", "", colnames(genotype))

    iid=genotype\$IID
    row.names(genotype) =genotype\$IID
    genotype=genotype[,7:length(genotype)]
    

    sum=fread("${assoc}")
    sum <- sum[SNP %in% colnames(genotype)]
    beta=data.frame(SNP=sum\$SNP,BETA=sum\$BETA)

    # turn the genotype into 2 matrix

    domin=apply(genotype, 2, subtract)
    rec=apply(genotype, 2, set_rec)


    # loop through each SNP in beta

    result_domin <- domin
    result_rec <- rec

    # Loop through each row in dfB
    for (i in 1:nrow(beta)) {
        
        column_name <- beta\$SNP[i]
        
        # Multiply the corresponding column
        result_domin[, column_name] <- result_domin[, column_name] * beta\$BETA[i]
        result_rec[, column_name] <- result_rec[, column_name] * beta\$BETA[i]
    }

    result_domin <- as.data.table(result_domin)
    result_rec <- as.data.table(result_rec)
    result_rec[,IID := rownames(genotype)]
    result_domin[,IID := rownames(genotype)]
    # read the pheno
    pheno=fread("${pheno}")
    pheno[,FID := NULL]
    pheno[,IID := as.character(IID)]
    pheno <- na.omit(pheno)
    pheno[,Pheno_percent:= get_quantile(Phenotype, 100)]
    domin <- merge(pheno, result_domin, by ="IID")
    rec <- merge(pheno, result_rec, by ="IID")
    result <- merge(domin, rec, by=c("IID", "Phenotype", "Pheno_percent"))
    # splite into increasing and decreasing effect size tables
    colnames(result) <- gsub("\\\\.x|\\\\.y", "", colnames(result))
    increase=c(beta\$SNP[beta\$BETA>0], "Phenotype", "Pheno_percent", "IID")
    decrease=c(beta\$SNP[beta\$BETA<0], "Phenotype", "Pheno_percent", "IID")

    pos=result[,colnames(result)%in% increase, with = FALSE]
    neg=result[,colnames(result)%in% decrease, with = FALSE ]


    #create new folder effect size count
    write.table(pos, "${fieldID}-${normalize}.pos.count", row.names=F, col.names=T, sep="\\t", quote=F)
    write.table(neg, "${fieldID}-${normalize}.neg.count", row.names=F, col.names=T, sep="\\t", quote=F)


    """

}






