
process run_gwas{
    afterScript 'ls * | grep -v .assoc.gz | xargs rm'
    module "plink"
    label "normal"
    publishDir "gwas/${normalize}/${followUp_type}", mode: 'symlink'
    input:
        tuple   val(fieldID),
                val(type),
                val(normalize),
                val(followUp_type),
                path(pheno),
                path(bed),
                path(bim),
                path(fam),
                path(qcSNP)
    output:
        tuple   val(fieldID),
                val(type),
                val(normalize),
                val(followUp_type),
                path("${fieldID}.assoc.gz")
    script:
    base = bed.baseName
    """
    plink   \
        --bfile ${base} \
        --pheno ${pheno} \
        --keep ${pheno} \
        --extract ${qcSNP} \
        --out ${fieldID} \
        --assoc \
        --pheno-name Phenotype \
        --autosome
     
     awk 'NR==FNR{a[\$2]=\$5; b[\$2]=\$6} NR!=FNR && FNR==1{print \$0,"A1 A2"} NR != FNR && FNR!=1 {print \$0,a[\$2],b[\$2]}' ${bim} ${fieldID}.qassoc | gzip > ${fieldID}.assoc.gz
    """
}

process run_freq{

    module "plink"
    label "normal"
    publishDir "gwas/${normalize}/${followUp_type}", mode: 'symlink'
    input:
        tuple   val(fieldID),
                val(type),
                val(normalize),
                val(followUp_type),
                path(pheno),
                path(bed),
                path(bim),
                path(fam),
                path(qcSNP)
    output:
        tuple   val(fieldID),
                val(type),
                val(normalize),
                val(followUp_type),
                path("${fieldID}.frq")
    script:
    base = bed.baseName
    """
    plink   \
        --bfile ${base} \
        --keep ${pheno} \
        --extract ${qcSNP} \
        --out ${fieldID} \
        --freq 

    """
}


process munge_sumstat{
    label 'normal'
    input:
        tuple   val(fieldID),
                val(type),
                val(normalize),
                val(followUp_type),
                path(gwas),
                path(munge)
    output:
        tuple   val(fieldID),
                val(type),
                val(normalize),
                val(followUp_type),
                path("${fieldID}.sumstats.gz")
    script:
    """
    ml purge
    ml python/2.7.17
    python ${munge} \
        --sumstat ${gwas} \
        --N-col NMISS \
        --out ${fieldID}
    """
}

process run_ldsc{
    label 'normal'
    afterScript "rm ${baseName}* ${weightName}*"
    input:
        tuple   val(fieldID),
                val(type),
                val(normalize),
                val(followUp_type),
                path(sumstat),
                path(ldsc),
                val(baseName),
                path(base),
                val(weightName),
                path(weight)
    output:
        tuple   val(fieldID),
                val(type),
                val(normalize),
                val(followUp_type),
                path("${fieldID}-${normalize}-${followUp_type}.herit"),
                env(h2)
    script:
    """
    ml purge
    ml python/2.7.17
    python ${ldsc} \
        --h2 ${sumstat} \
        --ref-ld-chr ${baseName} \
        --w-ld-chr ${weightName} \
        --out ${fieldID}
    h2=`grep "Total Observed" ${fieldID}.log | cut -d " " -f 5`
    echo "Trait Heritability" > ${fieldID}-${normalize}-${followUp_type}.herit
    echo "${fieldID} \${h2}" >> ${fieldID}-${normalize}-${followUp_type}.herit
    """
}
process run_genetic_correlation{
    label 'normal'
    afterScript "rm ${baseName}* ${weightName}*"
    input:
        tuple   val(normalize),
                val(fieldID),
                val(followUp_type),
                path(sumstat),
                path(sumstat2),
                path(ldsc),
                val(baseName),
                path(base),
                val(weightName),
                path(weight)
    output:
        tuple   val(fieldID),
                val(normalize),
                val(followUp_type),
                path("${fieldID}-${normalize}.gc")
    script:
    """
    ml purge
    ml python/2.7.17
    python ${ldsc} \
        --rg ${sumstat},`echo ${sumstat2} | sed 's/ /,/g'` \
        --ref-ld-chr ${baseName} \
        --w-ld-chr ${weightName} \
        --out tmp
    start=`grep -n "Summary of Genetic Correlation Result" tmp.log | cut -f 1 -d ":"`
    end=`grep -n "Analysis finished" tmp.log | cut -f 1 -d ":"`
    sed -n \"\$((start+1)),\$((end-2))p;\" tmp.log > ${fieldID}-${normalize}.gc
    """
}

process combine_genetic_correlation{
    module 'R/4.3.0'
    label 'normal'
    publishDir "result/${followUp_type}", mode: 'symlink'
    input:
        tuple   val(normalize),
                val(followUp_type),
                path(gc),
                path(showcase)
    output:
        tuple   val(normalize),
                path ("combined_genetic_correlation.csv")
    script:
    """
    #!/usr/bin/env Rscript
    library(data.table)
    .d <- `[`
    showcase <- fread("${showcase}")[,c("Field", "FieldID")]  |>
        .d(, Field:=gsub(",","", Field)) |>
        .d(,FieldID := as.factor(FieldID))
        
    files <- strsplit("${gc}", split = " ") |>
        unlist()
    res <-NULL
    for(i in files){
        res <- rbind(res, fread(i))
    }
    res[,p1 := gsub(".sumstats.gz", "", p1)]
    res[,p2 := gsub(".sumstats.gz", "", p2)]
    setnames(res, c("p1", "p2"), c("TraitA_ID","TraitB_ID"))
    res <- merge(res, showcase, by.x = "TraitA_ID", by.y = "FieldID")
    setnames(res, "Field", "TraitA")
    res <- merge(res, showcase, by.x = "TraitB_ID", by.y = "FieldID")
    setnames(res, "Field", "TraitB")
    fwrite(res, "combined_genetic_correlation.csv")
    """
}

process run_prsice{
    module "cmake"
    label 'prsice'
    publishDir "prs/${fieldID}/${followUp_type}", mode: 'symlink'
    input:
        tuple   val(fieldID),
                val(type),
                val(normalize),
                val(followUp_type),
                path(gwas),
                path(prsice),
                path(bed),
                path(bim),
                path(fam),
                path(qcSNP),
                path(pheno)
    output:
        tuple   val(fieldID),
                val(type),
                val(normalize),
                val(followUp_type),
                path("${fieldID}-${normalize}.summary"),
                path("${fieldID}-${normalize}.best"), emit: score
        
        tuple   val(fieldID),
                val(type),
                val(normalize),
                val(followUp_type),
                path("${fieldID}-${normalize}.snp"), emit: snps
    script:
    base = bed.baseName
    """
    awk 'NR==1{print} NR != 1 && \$3 != "NA"{print}' ${pheno} > keep
    ./${prsice} \
        --base ${gwas} \
        --target ${base} \
        --extract ${qcSNP} \
        --ld-keep keep \
        --keep ${pheno} \
        --pheno ${pheno} \
        --binary-target F \
        --out ${fieldID}-${normalize} \
        --pheno-col Phenotype \
        --thread ${task.cpus} \
        --print-snp \
	    --score avg \
        --fastscore
    """
}

process modify_prs{
    module 'R/4.3.0'
    label 'tiny'
    input:
        tuple   val(fieldID),
                val(type),
                val(normalize),
                val(followUp_type),
                path(summary),
                path(best)
    output:
        tuple   val(normalize),
                path ("${fieldID}-${normalize}-${followUp_type}-prs")
    script:
    """
    
    #!/usr/bin/env Rscript
    library(magrittr)
    library(data.table)
    fread("${summary}")  %>%
        .[,c("PRS.R2", "P")] %>%
        setnames(., "PRS.R2", "R2") %>%
        .[, Trait := "${fieldID}"] %>%
        .[, TraitType := "${type}"] %>%
        .[, Normalization := "${normalize}"] %>%
        .[, FollowUpType := "${followUp_type}"] %>%
        fwrite("${fieldID}-${normalize}-${followUp_type}-prs")
    """
}
