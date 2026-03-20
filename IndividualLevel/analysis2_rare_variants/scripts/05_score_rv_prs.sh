#!/usr/bin/env bash
set -eu
source "$(cd "$(dirname "$0")/.." && pwd)/config.sh"

SCORE_LOCAL_DIR="${LOCAL_OUT_ROOT}/rv_scores"
TMP_UPLOAD_DIR="${PROJECT_ROOT}/input/tmp_scores"

while read -r TRAIT; do
  [ -z "${TRAIT}" ] && continue
  for BIN in rare1 rare2; do
    if [ "${BIN}" = "rare1" ]; then
      FILTER_DIR="${RV_FILTER_DIR_RARE1}"
      FILTER_PREFIX="filter_001_01"
      SCORE_FILE="${SCORE_LOCAL_DIR}/${TRAIT}.rare1.score.tsv"
    else
      FILTER_DIR="${RV_FILTER_DIR_RARE2}"
      FILTER_PREFIX="filter_0001_001"
      SCORE_FILE="${SCORE_LOCAL_DIR}/${TRAIT}.rare2.score.tsv"
    fi
    [ -f "${SCORE_FILE}" ] || continue
    SCORE_DXID=$(dx upload "${SCORE_FILE}" --destination "${TMP_UPLOAD_DIR}/" --brief)
    for CHR in ${RV_CHROMS}; do
      dx run "${SAK_APP}" \
        --instance-type "${INSTANCE_SCORE}" \
        -iin="${SCORE_DXID}" \
        -icmd="plink2 \
          --pfile \"${FILTER_DIR}/c${CHR}_${FILTER_PREFIX}\" \
          --keep \"${TARGET_KEEP_DIR}/${TRAIT}.target.keep\" \
          --score $(basename "${SCORE_FILE}") 1 2 3 no-mean-imputation \
          --out ${TRAIT}_c${CHR}_${BIN}_prs" \
        --destination="${RV_PRS_DIR}/${TRAIT}/${BIN}" \
        --name "score_${TRAIT}_c${CHR}_${BIN}" \
        ${DX_YES}
    done
  done
done < "${TRAITS_FILE}"
