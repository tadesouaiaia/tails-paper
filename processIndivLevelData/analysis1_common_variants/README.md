# Tail Analysis - Run Guide

## Overview

This `run.sh` script executes a Nextflow-based Polygenic Risk Score (PRS) pipeline for continuous traits. 
The workflow processes genomic and phenotype data from the UK Biobank and performs the following steps:
1. Phenotype extraction from the SQL database.
2. Phenotype residualization, adjusting for relevant covariates.
3. Sample splitting of the genomic dataset into two halves:
	-Discovery set: Used to perform GWAS and LD Score Regression (LDSC) to estimate SNP-based heritability (h²).
	-Target set: Used to compute PRS using PRSice.

Key Outputs
Outputs used in the main quality control (QC) analyses of the paper:
- SNP heritability estimate (h²)
- PRS R²
Outputs used in the POPout test
- Residualized trait values 
- Trait PRS

Similar analyses were conducted in the All of Us dataset as an external validation using the Researcher Workbench (see Methods section of the paper for details).

Corresponding PRS values computed in the target dataset
## Prerequisites
- Access to the LSF (Load Sharing Facility) job scheduler
- Java installed and available via module load
- Nextflow installed
- Input files and databases as specified below

## How to Use

### Basic Execution
Submit the script to the job scheduler:
```bash
bsub < run.sh
```

### Job Configuration
The script is configured with the following LSF parameters (lines 1-10):
- **Job Name**: `tail` 
- **CPUs**: 1 processor
- **Hosts**: Single host execution
- **Queue**: `premium` 
- **Wall Clock Time**: 48 hours maximum runtime
- **Memory**: 30 GB
- **Project Code**: `acc_psychgen` 
- **Output Files**: 
  - `tail.o` - standard output
  - `tail.e` - error output

## What It Does

The script executes the Nextflow pipeline (`extreme_prs_analysis.nf`) which:
1. Loads required Java environment
2. Processes UK Biobank genotypic data
3. Runs GWAS and calculates Polygenic Risk Scores using multiple methods
4. Performs LDSC (LD score regression) analysis
5. Analyzes customized trait file provided separately by the user

## Key Parameters Explained

### Input Data Paths
| Parameter | Purpose |
|-----------|---------|
| `--showcase` | Data dictionary/showcase file provided by UKB; used to extract all the listed traits with ValueType "Integer" or "Continuous" |
| `--db` | UK Biobank phenotype database file in SQL format |
| `--cov` | Covariate file containing baseline covariates |
| `--blood` | Blood cell trait phenotype file, provided separately by the user |
| `--label` | CSV file with phenotype labels, eg. 50 standing_height |

### Genotype Data
| Parameter | Purpose |
|-----------|---------|
| `--geno` | Path to genotype files (prefix for .bed/.bim/.fam) |
| `--fam` | Pedigree file of QC-ed unrelated samples to retain |
| `--snp` | SNP list of QC-ed variants |
| `--siblings` | File listing sibling pairs |
| `--drop` | File with withdrawn participant IDs |

### Analysis Tools
| Parameter | Purpose |
|-----------|---------|
| `--prsice` | Path to PRSice executable |
| `--scores` | Directory containing reference score files for LDSC |
| `--ldsc` | Path to LDSC software |


## Output Files

Results are organized in the following directories:
- `prs/` - Computed Polygenic Risk Scores organized by adjustment type: adjusted (blood traits), normalized (blood traits), and inverse-normalized (all traits extracted from db)
- `result/` - Final analysis results and summaries - PRS-inverse.info for PRS r2 results, ResidDis.info for distribution QC metrics, Herit.info for SNP-based heritability (h²) estimates
- `pheno/` - Phenotype data organized by adjustment type: adjusted (blood traits), normalized (blood traits), and inverse-normalized (all traits extracted from db)
- `gwas/` - GWAS results organized by adjustment type: adjusted (blood traits), normalized (blood traits), and inverse-normalized (all traits extracted from db)

Each trait extracted from the database and processed at different timepoints has its own subdirectories under `gwas/`, `pheno/`, and `prs/` containing:
- `all/` - Baseline measurement for all individuals
- `base/` - Individuals with at least two measurements; uses the baseline measurement at the baseline visit (instance=0)
- `mean/` - Individuals with at least two measurements; uses the mean of baseline and second measurements
- `second/` - Individuals with at least two measurements; uses the second measurement at the repeat visit (instance=1)

## Advanced Options

### Resume Interrupted Runs
The script includes `-resume` flag which:
- Restarts from the last successfully completed task
- Avoids re-computing completed steps
- Useful if the pipeline is interrupted before completion

### Customization
To modify the analysis:
1. Edit the parameter values in this script, or
2. Create a Nextflow config file and reference it

Example to run with custom config:
```bash
nextflow run extreme_prs_analysis.nf -c custom.config -resume
```

## Monitoring

### Check Job Status
```bash
bjobs -J extreme
```

### View Output
```bash
tail -f extreme.o  # Standard output
tail -f extreme.e  # Error messages
```

### Kill Job if Needed
```bash
bkill -J extreme
```

## Common Issues

**Memory Errors**: Increase the LSF memory parameter (`-M`) from 30000 (30GB) to higher if needed

**Timeout**: Extend wall clock time (`-W`) beyond 48:00 if analysis takes longer

**Missing Files**: Verify all input paths exist and are accessible, particularly:
- Genotype files
- Database files
- Reference score files

## Contact
For questions about the analysis or parameters, contact the maintainers or refer to the extreme_prs_analysis.nf Nextflow script for detailed implementation details.
