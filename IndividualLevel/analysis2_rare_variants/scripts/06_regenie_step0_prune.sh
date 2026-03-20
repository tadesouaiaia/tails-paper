#!/usr/bin/env bash
set -eu
source "$(cd "$(dirname "$0")/.." && pwd)/config.sh"

for CHR in ${BURDEN_CHROMS}; do
  dx run "${SAK_APP}" \
    --instance-type "${INSTANCE_PRUNE}" \
    -iin="${WES_BULK_DIR}/ukb23158_c${CHR}_b0_v1.bed" \
    -iin="${WES_BULK_DIR}/ukb23158_c${CHR}_b0_v1.bim" \
    -iin="${WES_BULK_DIR}/ukb23158_c${CHR}_b0_v1.fam" \
    -icmd="plink \
      --bfile ukb23158_c${CHR}_b0_v1 \
      --maf 0.01 \
      --indep-pairwise 50 5 0.2 \
      --out c${CHR}" \
    --destination="${BURDEN_STEP0_DIR}" \
    --name "prune_c${CHR}" \
    ${DX_YES}
done
