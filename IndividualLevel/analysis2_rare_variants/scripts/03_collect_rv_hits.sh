#!/usr/bin/env bash
set -eu
source "$(cd "$(dirname "$0")/.." && pwd)/config.sh"

mkdir -p "${LOCAL_OUT_ROOT}/rv_hits"

while read -r TRAIT; do
  [ -z "${TRAIT}" ] && continue
  for BIN in rare1 rare2; do
    OUT="${LOCAL_OUT_ROOT}/rv_hits/${TRAIT}.${BIN}.hits.tsv"
    rm -f "${OUT}"
    HEADER_WRITTEN=0
    for CHR in ${RV_CHROMS}; do
      REMOTE="${RV_GWAS_DIR}/${TRAIT}/${BIN}/${TRAIT}_c${CHR}_${BIN}.Phenotype.glm.linear"
      LOCAL="${LOCAL_OUT_ROOT}/rv_hits/${TRAIT}_${BIN}_c${CHR}.glm.linear"
      dx download "${REMOTE}" -o "${LOCAL}" >/dev/null 2>&1 || continue
      if [ "${HEADER_WRITTEN}" -eq 0 ]; then
        awk -v chr="${CHR}" -v p="${GENOME_WIDE_P}" 'BEGIN{FS=OFS="\t"} NR==1{print "CHR",$0} NR>1 && $NF+0 <= p {print chr,$0}' "${LOCAL}" > "${OUT}"
        [ -s "${OUT}" ] && HEADER_WRITTEN=1 || true
      else
        awk -v chr="${CHR}" -v p="${GENOME_WIDE_P}" 'BEGIN{FS=OFS="\t"} NR>1 && $NF+0 <= p {print chr,$0}' "${LOCAL}" >> "${OUT}"
      fi
    done
  done
done < "${TRAITS_FILE}"
