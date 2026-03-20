#!/usr/bin/env bash
set -eu
source "$(cd "$(dirname "$0")/.." && pwd)/config.sh"

SELECTED_DIR="${LOCAL_OUT_ROOT}/burden_selected"
TMP_UPLOAD_DIR="${PROJECT_ROOT}/input/tmp_selected_masks"

while read -r TRAIT; do
  [ -z "${TRAIT}" ] && continue
  SELECTED="${SELECTED_DIR}/${TRAIT}.selected_masks.tsv"
  [ -f "${SELECTED}" ] || continue
  SELECTED_DXID=$(dx upload "${SELECTED}" --destination "${TMP_UPLOAD_DIR}/" --brief)
  for CHR in ${BURDEN_CHROMS}; do
    dx run "${SAK_APP}" \
      --instance-type "${INSTANCE_SCORE}" \
      -iin="${BURDEN_STEP2_DIR}/${TRAIT}/c${CHR}/step2_${TRAIT}_c${CHR}_burden_masks_masks.bed" \
      -iin="${BURDEN_STEP2_DIR}/${TRAIT}/c${CHR}/step2_${TRAIT}_c${CHR}_burden_masks_masks.bim" \
      -iin="${BURDEN_STEP2_DIR}/${TRAIT}/c${CHR}/step2_${TRAIT}_c${CHR}_burden_masks_masks.fam" \
      -iin="${BASE_PHENO_DIR}/${TRAIT}.base" \
      -iin="${BASE_KEEP_DIR}/${TRAIT}.base.keep" \
      -iin="${SELECTED_DXID}" \
      -icmd="awk 'NR>1{print \$2}' $(basename "${SELECTED}") > selected_mask_ids.txt && \
        cp ${TRAIT}.base phenotypes.tsv && \
        plink2 \
          --bfile step2_${TRAIT}_c${CHR}_burden_masks_masks \
          --extract selected_mask_ids.txt \
          --keep ${TRAIT}.base.keep \
          --pheno phenotypes.tsv \
          --pheno-name Phenotype \
          --glm allow-no-covars \
          --out reest_${TRAIT}_c${CHR}" \
      --destination="${BURDEN_REEST_DIR}/${TRAIT}/c${CHR}" \
      --name "reestimate_${TRAIT}_c${CHR}" \
      ${DX_YES}
  done
done < "${TRAITS_FILE}"
