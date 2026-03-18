# Tails Analysis Repository

This repository contains the code necessary to reproduce the UK Biobank protected-data analyses described 
in the *Tails* manuscript.

The repository is organized into three main analysis pipelines. A brief overview of each folder follows.

## 1) Primary analyses (`analysis1_common_variants/`) 
 
The primary pipeline performs the common-variant analyses used throughout the manuscript.  
It is written for an LSF job scheduler with access to the UK Biobank SQL phenotype database.

This pipeline performs the following steps:

- Extraction of quantitative traits from the UK Biobank SQL database
- Phenotype residualization and normalization
- Sample splitting into discovery and target sets
- Genome-wide association studies (GWAS) in the discovery set
- LD Score Regression (LDSC) to estimate SNP-based heritability
- Polygenic risk score (PRS) construction in the target set 
- POPout (And additional analyses) performed on individual PRS-on-phenotype data.  

The normalized phenotype files produced in this pipeline are used as inputs to the secondary analyses.

## 1) Secondary analyses (`analysis2_rare_variants`) 

This pipeline performs rare-variant analyses using the UK Biobank whole-genome sequencing (WGS) and whole-exome sequencing (WES) datasets on the DNAnexus Research Analysis Platform.

Importantly, this workflow assumes that phenotype values have **already been normalized and residualized** in the primary pipeline. No covariates are included in this stage of the analysis.

The workflow includes:

- Rare single-variant GWAS in two minor-allele-frequency bins
- Construction of two rare-variant PRS components
- Gene-based burden testing using REGENIE
- Construction of a burden-based PRS component

These rare-derived scores are then combined with the common-variant PRS produced in the primary pipeline.

## Auxiliary simulations (`analysis3_simulations/`) 

This directory contains forward-time evolutionary simulations implemented in SLiM.  
These simulations model stabilizing selection on a polygenic trait and were used to investigate the enrichment of rare large-effect alleles in the tails of the trait distribution.

## Data availability

UK Biobank genotype and phenotype data used in these analyses are protected and cannot be distributed in this repository.

Users wishing to reproduce the analyses must obtain access to the UK Biobank dataset and provide the required input files locally.

## Notes on figure construction

Some elements used to construct figures in the manuscript are derived from publicly available datasets rather than generated directly within the pipelines in this repository.

Specifically:

- The intermediate common-variant GWAS effects used to produce the gray points in the trumpet plots were taken from publicly available summary statistics released by the Neale Lab.

- The rare-variant and burden-variant signals used in the trumpet plots, as well as in the association analysis between the number of rare variants and 
POPout effect size (Main Figure 4), were obtained from the supplemental data accompanying the exome sequencing analysis of the UK Biobank 
published by Backman et al. (2021).

These external datasets are referenced in the manuscript and can be downloaded from their respective public sources.
