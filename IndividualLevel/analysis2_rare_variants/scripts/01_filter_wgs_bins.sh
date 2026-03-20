#!/usr/bin/env bash
set -eu
source "$(cd "$(dirname "$0")/.." && pwd)/config.sh"

for CHR in ${RV_CHROMS}; do
  dx run "${SAK_APP}" \
    --instance-type "${INSTANCE_FILTER}" \
    -icmd="plink2 \
      --pfile \"${WGS_BULK_DIR}/ukb24308_c${CHR}_b0_v1\" \
      --maf ${RARE1_MIN_MAF} --max-maf ${RARE1_MAX_MAF} \
      --make-pgen --no-psam-pheno \
      --out c${CHR}_filter_001_01" \
    --destination="${RV_FILTER_DIR_RARE1}" \
    --name "plink2_filter_chr${CHR}_rare1" \
    ${DX_YES}

  dx run "${SAK_APP}" \
    --instance-type "${INSTANCE_FILTER}" \
    -icmd="plink2 \
      --pfile \"${WGS_BULK_DIR}/ukb24308_c${CHR}_b0_v1\" \
      --maf ${RARE2_MIN_MAF} --max-maf ${RARE2_MAX_MAF} \
      --make-pgen --no-psam-pheno \
      --out c${CHR}_filter_0001_001" \
    --destination="${RV_FILTER_DIR_RARE2}" \
    --name "plink2_filter_chr${CHR}_rare2" \
    ${DX_YES}
done
