#!/usr/bin/env bash
set -eu
source "$(cd "$(dirname "$0")/.." && pwd)/config.sh"

while read -r TRAIT; do
  [ -z "${TRAIT}" ] && continue
  for CHR in ${RV_CHROMS}; do
    dx run "${SAK_APP}" \
      --instance-type "${INSTANCE_RV_GWAS}" \
      -icmd="plink2 \
        --pfile \"${RV_FILTER_DIR_RARE1}/c${CHR}_filter_001_01\" \
        --pheno \"${BASE_PHENO_DIR}/${TRAIT}.base\" \
        --pheno-name Phenotype \
        ${PLINK2_GLM_FLAGS} \
        --out ${TRAIT}_c${CHR}_rare1" \
      --destination="${RV_GWAS_DIR}/${TRAIT}/rare1" \
      --name "gwas_${TRAIT}_chr${CHR}_rare1" \
      ${DX_YES}

    dx run "${SAK_APP}" \
      --instance-type "${INSTANCE_RV_GWAS}" \
      -icmd="plink2 \
        --pfile \"${RV_FILTER_DIR_RARE2}/c${CHR}_filter_0001_001\" \
        --pheno \"${BASE_PHENO_DIR}/${TRAIT}.base\" \
        --pheno-name Phenotype \
        ${PLINK2_GLM_FLAGS} \
        --out ${TRAIT}_c${CHR}_rare2" \
      --destination="${RV_GWAS_DIR}/${TRAIT}/rare2" \
      --name "gwas_${TRAIT}_chr${CHR}_rare2" \
      ${DX_YES}
  done
done < "${TRAITS_FILE}"
