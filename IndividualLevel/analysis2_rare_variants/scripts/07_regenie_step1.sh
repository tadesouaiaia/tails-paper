#!/usr/bin/env bash
set -eu
source "$(cd "$(dirname "$0")/.." && pwd)/config.sh"

while read -r TRAIT; do
  [ -z "${TRAIT}" ] && continue
  for CHR in ${BURDEN_CHROMS}; do
    dx run "${SAK_APP}" \
      --instance-type "${INSTANCE_STEP1}" \
      -iin="${WES_BULK_DIR}/ukb23158_c${CHR}_b0_v1.bed" \
      -iin="${WES_BULK_DIR}/ukb23158_c${CHR}_b0_v1.bim" \
      -iin="${WES_BULK_DIR}/ukb23158_c${CHR}_b0_v1.fam" \
      -iin="${BASE_PHENO_DIR}/${TRAIT}.base" \
      -iin="${BURDEN_STEP0_DIR}/c${CHR}.prune.in" \
      -icmd="cp ${TRAIT}.base phenotypes.tsv && regenie \
        --step 1 \
        --bed ukb23158_c${CHR}_b0_v1 \
        --extract c${CHR}.prune.in \
        --phenoFile phenotypes.tsv \
        --bsize ${REGENIE_BSIZE} \
        --threads ${REGENIE_THREADS} \
        --out step1_${TRAIT}_c${CHR}" \
      --destination="${BURDEN_STEP1_DIR}/${TRAIT}/c${CHR}" \
      --name "regenie_step1_${TRAIT}_c${CHR}" \
      ${DX_YES}
  done
done < "${TRAITS_FILE}"
