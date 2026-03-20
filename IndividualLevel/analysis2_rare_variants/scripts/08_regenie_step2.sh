#!/usr/bin/env bash
set -eu
source "$(cd "$(dirname "$0")/.." && pwd)/config.sh"

while read -r TRAIT; do
  [ -z "${TRAIT}" ] && continue
  for CHR in ${BURDEN_CHROMS}; do
    args=(dx run "${SAK_APP}" --instance-type "${INSTANCE_STEP2}"
      -iin="${WES_BULK_DIR}/ukb23158_c${CHR}_b0_v1.bed"
      -iin="${WES_BULK_DIR}/ukb23158_c${CHR}_b0_v1.bim"
      -iin="${WES_BULK_DIR}/ukb23158_c${CHR}_b0_v1.fam"
      -iin="${BASE_PHENO_DIR}/${TRAIT}.base"
      -iin="${MASKS_DEF}"
      -iin="${GENE_IDS}"
      -iin="${ANNO_FILE}"
      -iin="${SETS_FILE}"
      -iin="${BURDEN_STEP1_DIR}/${TRAIT}/c${CHR}/step1_${TRAIT}_c${CHR}_pred.list")

    for i in ${LOCO_INDEXES}; do
      args+=( -iin="${BURDEN_STEP1_DIR}/${TRAIT}/c${CHR}/step1_${TRAIT}_c${CHR}_${i}.loco" )
    done

    cmd="cp ${TRAIT}.base phenotypes.tsv && regenie \
      --step 2 \
      --bed ukb23158_c${CHR}_b0_v1 \
      --phenoFile phenotypes.tsv \
      --pred step1_${TRAIT}_c${CHR}_pred.list \
      --set-list $(basename "${SETS_FILE}") \
      --extract-sets $(basename "${GENE_IDS}") \
      --mask-def $(basename "${MASKS_DEF}") \
      --anno-file $(basename "${ANNO_FILE}") \
      --write-mask --write-mask-snplist \
      --out step2_${TRAIT}_c${CHR}_burden_masks"

    args+=( -icmd="$cmd" --destination="${BURDEN_STEP2_DIR}/${TRAIT}/c${CHR}" --name "regenie_step2_${TRAIT}_c${CHR}" ${DX_YES} )
    eval "${args[*]}"
  done
done < "${TRAITS_FILE}"
