#!/usr/bin/env bash
set -eu

# Required configuration for the DNAnexus rare-variant / burden PRS pipeline.
# Copy this file to config.sh and edit the paths before running anything.

PROJECT_ROOT="/mnt/project"
PIPELINE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOCAL_OUT_ROOT="${PIPELINE_ROOT}/local_outputs"

# UK Biobank bulk data on DNAnexus
WGS_BULK_DIR="${PROJECT_ROOT}/Bulk/DRAGEN WGS/DRAGEN population level WGS variants, PLINK format [500k release]"
WES_BULK_DIR="${PROJECT_ROOT}/Bulk/Exome sequences/Population level exome OQFE variants, PLINK format - final release"
WES_HELPER_DIR="${WES_BULK_DIR}/helper_files"

# User-provided phenotype files.
# These phenotypes must already be normalized / residualized for all desired covariates.
# No covariate file is used anywhere in this pipeline.
BASE_PHENO_DIR="${PROJECT_ROOT}/input/base_phenos"
TARGET_PHENO_DIR="${PROJECT_ROOT}/input/target_phenos"

# Optional keep files and common PRS inputs, if used in your local merge steps
BASE_KEEP_DIR="${PROJECT_ROOT}/input/base_keep"
TARGET_KEEP_DIR="${PROJECT_ROOT}/input/target_keep"
COMMON_PRS_DIR="${PROJECT_ROOT}/input/common_prs"

# Burden helper inputs
BURDEN_INPUT_DIR="${PROJECT_ROOT}/input/burden"
MASKS_DEF="${BURDEN_INPUT_DIR}/masks.def"
GENE_IDS="${BURDEN_INPUT_DIR}/gene_ids.txt"
SETS_FILE="${BURDEN_INPUT_DIR}/ukb23158_500k_OQFE.sets.clean.txt.gz"
ANNO_FILE="${WES_HELPER_DIR}/ukb23158_500k_OQFE.annotations.txt.gz"

# Output directories on DNAnexus
INPUT_ROOT="${PROJECT_ROOT}/input"
RESULTS_ROOT="${PROJECT_ROOT}/results"
RV_FILTER_DIR_RARE1="${INPUT_ROOT}/wgs/rare1"
RV_FILTER_DIR_RARE2="${INPUT_ROOT}/wgs/rare2"
RV_GWAS_DIR="${RESULTS_ROOT}/rv_gwas"
RV_HITS_DIR="${RESULTS_ROOT}/rv_hits"
RV_PRS_DIR="${RESULTS_ROOT}/rv_prs"
BURDEN_STEP0_DIR="${RESULTS_ROOT}/burden_step0"
BURDEN_STEP1_DIR="${RESULTS_ROOT}/burden_step1"
BURDEN_STEP2_DIR="${RESULTS_ROOT}/burden_step2"
BURDEN_REEST_DIR="${RESULTS_ROOT}/burden_reestimate"
BURDEN_PRS_DIR="${RESULTS_ROOT}/burden_prs"
MERGED_PRS_DIR="${RESULTS_ROOT}/merged_prs"

# Trait lists
TRAITS_FILE="${PIPELINE_ROOT}/templates/traits.txt"

# Analysis settings
RV_CHROMS="1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22"
BURDEN_CHROMS="1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 X"
LOCO_INDEXES="1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45"

RARE1_MIN_MAF="0.001"
RARE1_MAX_MAF="0.01"
RARE2_MIN_MAF="0.0001"
RARE2_MAX_MAF="0.001"
GENOME_WIDE_P="2.18e-11"

# DNAnexus job settings
SAK_APP="app-swiss-army-knife"
DX_YES="-y"
INSTANCE_FILTER="mem3_ssd1_v2_x8"
INSTANCE_RV_GWAS="mem2_ssd1_v2_x4"
INSTANCE_PRUNE="mem2_ssd1_v2_x16"
INSTANCE_STEP1="mem2_ssd1_v2_x16"
INSTANCE_STEP2="mem3_ssd1_v2_x32"
INSTANCE_SCORE="mem2_ssd1_v2_x4"

REGENIE_BSIZE="1000"
REGENIE_THREADS="8"
PLINK2_GLM_FLAGS="--glm allow-no-covars"

mkdir -p "${LOCAL_OUT_ROOT}"
