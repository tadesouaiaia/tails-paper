#!/usr/bin/env nextflow
nextflow.enable.dsl=2
params.version=false
params.help=false
version='0.0.3'

timestamp='2021-10-26'
if(params.version) {
    System.out.println("")
    System.out.println("Run extreme phenotype analysis - Version: $version ($timestamp)")
    exit 1
}

params.extreme=1
params.normal=5
params.perm=10000
if(params.help){
    System.out.println("")
    System.out.println("Run extreme phenotype analysis - Version: $version ($timestamp)")
    System.out.println("Usage: ")
    System.out.println("    nextflow run extreme_analysis.nf [options]")
    System.out.println("Mandatory arguments:")
    System.out.println("    --prsice          PRSice executable")
    Sysmte.out.println("    --parents         Parent information")
    Sysmte.out.println("    --siblings        Sibling information")
    System.out.println("    --geno            Genotype file prefix ")
    System.out.println("    --fam             QCed fam file ")
    System.out.println("    --snp             QCed SNP file ")
    System.out.println("    --redundent       Redundent trait to be removed")
    System.out.println("    --db              UKB Phenotype database")
    System.out.println("    --ldsc            Folder to LD score software")
    System.out.println("    --score           Folder containing LD Scores. Should have")
    System.out.println("                      format of baseline-chr and weight-chr")
    System.out.println("    --weight          Weight LD score prefix")
    System.out.println("    --fieldFinders    Folder containing the field finders.")
    System.out.println("                      Should have field_finder as suffix")
    System.out.println("    --drop            Samples who withdrawn consent")
    System.out.println("    --cov             Covariate file containing batch and PCs")
    System.out.println("    --showcase        Data showcase, use to select phenotypes")
    System.out.println("    --extreme         Top x percentile we considered as extreme. Default: ${params.extreme}")
    System.out.println("    --normal          x percentiles from top and bottom that we considered")
    System.out.println("                      as normal. Default: ${params.normal}")
    System.out.println("    --perm            Total permutation. Default: ${params.perm}")
    System.out.println("    --blood           Blood phenotypes from Will")
    System.out.println("    --label           Labeling for relationship plot")
    System.out.println("    --tade            Modified python script from tade")
    System.out.println("    --help            Display this help messages")
} 

// include our processes from other file 
include {   extract_quantitative_traits
            extract_phenotype_from_sql
            residualize_phenotype
            extract_fecundity_from_sql
            adjust_fecundity
            split_base_target
            get_blood_trait_name_from_will
            extract_blood_traits
            r_extract_phenotype_from_sql  } from './module/phenotype_extraction'

include {   run_gwas
	        run_freq
            munge_sumstat
            run_ldsc
            run_genetic_correlation
            combine_genetic_correlation
            run_prsice
            modify_prs    }   from './module/prs_analysis'
include {   gather_file as gather_herit
            gather_file as gather_prs_raw
            gather_file as gather_prs_inverse
            gather_file as gather_raw 
            gather_file as gather_plot 
            gather_file as gather_norm
            gather_file as gather_raw_hist}   from './module/misc'
include {   merge_information
            statistical_analysis
            statistical_analysis2
            dichotomize_extreme
            partial_method_correlation
            combine_correlation_results
            qq_plot
            heatmap
            reg_mean_quantile_plots
            sib_reg_quantile_plots
            prune_phenotypes
            prune_phenotypes_sib
            plot_relationship
            reg_mean_quantile_plots_output
            tade_analyses
            tade_new_prs
            organize_tade
            clive_prs
            tade_prs_predictivity
            tade_selection
            tade_health_tail   }   from './module/downstream'

include {   filter_snp
            make_geno
            get_allele_count } from './module/misc2'

// helper functions
def fileExists(fn){
   if (fn.exists()){
       return fn;
   }else
       error("\n\n-----------------\nFile $fn does not exist\n\n---\n")
}
def get_prefix(str){
    last = str.split("/").last();
    if(last[-1] == "/" || last[-1] != "."){
        return "./";
    }else{
        return str.split("/").last();
    }
}
def get_prefix_ldsc(str){
    if(str.split('-')[0] == "NA"){
        error("\n\n----------\n$str cannot be tokenized\n")
    }else
        return str.split('-')[0];
}
// Defining variables 
redundent = Channel.fromPath("${params.redundent}")
showcase = Channel.fromPath("${params.showcase}")
label = []
if(params.label){
    label =  Channel.fromPath("${params.label}")
}
db = Channel.fromPath("${params.db}")
qcFam = Channel.fromPath("${params.fam}")
qcSNP = Channel.fromPath("${params.snp}")
siblings = Channel.fromPath("${params.siblings}")
cov = Channel.fromPath("${params.cov}")
withdrawn = Channel.fromPath("${params.drop}")
external_blood = Channel.fromPath("${params.blood}")
genotype = Channel
    .fromFilePairs("${params.geno}.{bed,bim,fam}",size:3, flat : true){ file -> file.baseName }
    .ifEmpty { error "No matching plink files" }        
    .map { a -> [fileExists(a[1]), fileExists(a[2]), fileExists(a[3])] } 
prsice = Channel.fromPath("${params.prsice}")
ldsc = Channel.fromPath("${params.ldsc}/ldsc.py")
munge = Channel.fromPath("${params.ldsc}/munge_sumstats.py")
score = Channel.fromPath("${params.scores}/*") \
    | map { a -> [ get_prefix_ldsc(a.baseName)+"-", file(a)]} \
    | groupTuple()


// The main workflow
workflow{
    // 1. First, we need to select phenotypes of interest
    phenotype_selection()
    // 2. Then we perform the PRS analysis.
    prs_analysis(phenotype_selection.out.phenotype)

}



// This workflow is responsible for selecting and transforming the phenotype
// used in this analysis
workflow phenotype_selection{
    main:
        // 1. Identify valid phenotypes (continuous + >10,000 samples)
        extract_quantitative_traits(showcase)
        // 2. Extract Fecundity and paternal age information from our database
        extract_fecundity_from_sql(db)
        // 3. Adjust fecundity and paternal age based on Sanjak et al (2018)
        adjust_fecundity(extract_fecundity_from_sql.out, withdrawn)
        // 4. Extract phenotypes from database
        nonblood = extract_quantitative_traits.out.nonblood
            .splitCsv(header: true) 
            .map{row -> ["NonBlood", "${row.FieldID}", "${row.Coding}"]} 
        blood = extract_quantitative_traits.out.blood
            .splitCsv(header: true) 
            .map{row -> ["Blood", "${row.FieldID}", "${row.Coding}"]} 
        nonblood \
            | mix(blood) \
            | combine(db) \
            | r_extract_phenotype_from_sql

        // 5. Remove outliers from data (6SD away from mean), then 
        //    either inverse normalize + residualize or just
        //    residualize (Age + Sex + Batch + Centre + 40 PC).
        //    For blood traits, we also include Dilusion factor and fasting time
        //    as covariate and remove samples who take statin
        // data_type= Channel.of("raw", "inverse")
        // speed up a bit here

        data_type= Channel.of("inverse")
        r_extract_phenotype_from_sql.out \
            | combine(Channel.of("all", "base","second", "mean")) \
            | combine(withdrawn) \
            | combine(siblings) \
            | combine(qcFam) \
            | combine(cov) \
            | combine(data_type)\
            | (residualize_phenotype )

        norm = residualize_phenotype.out.junk \
            | filter{ a -> a[0] == "all"} \
            | map{ a -> a[1]} \
            | collect
        gather_norm(norm, "ResidDis.info")
        rawHist = residualize_phenotype.out.junk \
            | filter{ a -> a[0] == "all"} \
            | map{ a -> a[3]} 
            | collect
        gather_raw_hist(rawHist, "RawDis.info")
        get_blood_trait_name_from_will(external_blood) \
            | splitCsv(header: true) \
            | map{ a -> [a.trait, a.type, a.normalize]} \
            | combine(external_blood) \
            | combine(withdrawn) \
            | combine(siblings) \
            | combine(qcFam) \
            | combine(cov) \
            | extract_blood_traits
        
        pheno_out = residualize_phenotype.out.dat \
           | mix(extract_blood_traits.out.dat)
    emit: 
        phenotype = pheno_out
        fecundity = adjust_fecundity.out
}


workflow prs_analysis{
    take: pheno
    main:
        // 1. split data into base and target (50/50). We will always put
        //    samples with siblings in the target to maximize sample size
        //    for downstream analyses
        pheno \
            | split_base_target
        // 2. peform GWAS on base
        split_base_target.out.base \
            | combine(genotype) \
            | combine(qcSNP) \
            /* These are phenotypes that we don't want to perform PRS on as they are use for the other test*/
            | filter{ a -> !(a[0] == 137 || a[0] == 135 || a[0] == 2405 || a[0] == 2734)} \
            | (run_gwas  )
        // 3. Extract the ld score to appropriate groups
        baseline = score \
            | filter { a -> (a[0] =~ /baseline/) }
        weight = score \
            | filter { a -> (a[0] =~ /weight/) }
        // 3. Perform LDSC on base GWAS to obtain the SNP heritability
        run_gwas.out \
            | combine(munge) \
            | munge_sumstat \
            | combine(ldsc) \
            | combine(baseline) \
            | combine(weight) \
            | run_ldsc
        
        // 4. Get trait heritability information
        heritRes = run_ldsc.out \
            | map{a -> a[4]} \
            | collect
        
        gather_herit(heritRes, "Herit.info")
        // 5. Only retain Traits with SNP based heritability > 5%
        valid_field = run_ldsc.out
            .filter{ it[5].toFloat() > 0.05 }
            .map{ it -> [it[0].toString(), it[1].toString(), it[2].toString(), it[3].toString()] }
        // 5a. Perform genetic correlation analyses
        valid_munge = munge_sumstat.out \
            | combine(valid_field, by: [0, 1 ,2, 3])

        // 0 ID, 1 Type, 2 normalize, 3 stupid type, 4 file
        // 5     6       7            8              9
        valid_munge \
            | combine(valid_munge) \
            | filter{ a -> ((a[2] == "inverse" || a[2] == "Will_Blood") && 
                a[2] == a[7] // same Normalization
                && a[3] == a[8] // same stupid type
                && a[0].toFloat() < a[5].toFloat())} \
            | map{ it -> [it[2],// normalization
             it[0],     // fieldID
             it[3], // stupid type
             it[4], it[9]]} \
            | groupTuple(by: [0, 1, 2, 3]) \
            | combine(ldsc) \
            | combine(baseline) \
            | combine(weight) \
            | run_genetic_correlation \
            | map{ it -> [it[1], it[2], it[3]]} \
            | groupTuple(by: [0, 1]) \
            | combine(showcase) \
            | combine_genetic_correlation
        // 6. Perform PRS on trait with SNP h2 > 5%
        run_gwas.out \
            | combine(valid_field, by: [0, 1, 2, 3]) \
            | combine(prsice) \
            | combine(genotype) \
            | combine(qcSNP) \
            | combine(split_base_target.out.target, by: [0, 1, 2, 3]) \
            | run_prsice



        run_prsice.out.score \
            | modify_prs
        prsRes = modify_prs.out \
            | groupTuple
        raw = prsRes \
            | filter{ a -> a[0] == "raw"} \
            | map{ a -> a[1]}
        inverse = prsRes \
            | filter { a -> a[0] != "raw"} \
            | map{ a -> a[1]}
            
        inverseRes = gather_prs_inverse(inverse.collect(), "PRS-inverse.info") \
            | map{ a -> ["inverse", a]}


    emit:
        prs = run_prsice.out.score
        summary = prsRes
}








