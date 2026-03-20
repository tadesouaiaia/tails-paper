#BSUB -L /bin/sh
#BSUB -n 1
#BSUB -J extreme
#BSUB -R "span[hosts=1]"
#BSUB -q premium               # target queue for job execution
#BSUB -W 48:00                # wall clock limit for job
#BSUB -P acc_psychgen             # project to charge time
#BSUB -o extreme.o
#BSUB -eo extreme.e
#BSUB -M 30000

ml java
ark=/sc/arion/projects/ukb18177_oreilly/ukb/
geno=${ark}/genotyped
project=/sc/arion/projects/psychgen/projects/prs/extreme_traits/
nextflow run \
	/sc/arion/projects/paul_oreilly/lab/wuh13/tail_paper/script/extreme_prs_analysis.nf \
	--showcase /sc/arion/projects/paul_oreilly/lab/wuh13/tail_paper/input/Toy_Data_Dictionary_Showcase.csv \
	-resume \
	--db /sc/arion/projects/psychgen/projects/ukb_Dec2023/ukb18177-v2.db \
	--cov /sc/arion/projects/psychgen/projects/prs/extreme_traits/sample_filter/baseline_full_covar.txt \
	--fam /sc/arion/projects/psychgen/projects/prs/extreme_traits/sample_filter/ukb18177-qc-noCancer.fam \
	--drop ${ark}/withdrawn/withdraw18177_398_20240119.txt \
	--siblings ${geno}/ukb18177.sibs  \
	--geno ${geno}/ukb18177 \
	--snp ${geno}/ukb18177-qc.snplist \
	--prsice /sc/arion/projects/psychgen/ukb/usr/sam/projects/prs/PRSice/bin/PRSice \
    	--scores /sc/arion/projects/psychgen/projects/prs/sample_overlap/analysis/prepare/data/reference/  \
	--ldsc /sc/arion/projects/psychgen/projects/prs/sample_overlap/software/ldsc/ \
	--label ${project}/data/label.csv \
	--blood ${project}/data/phenotype/Blood.txt	

