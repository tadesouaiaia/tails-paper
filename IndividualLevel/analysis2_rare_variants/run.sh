#!/usr/bin/env bash
set -eu

source "$(cd "$(dirname "$0")" && pwd)/config.sh"

# Uncomment the stages you want to run.
# bash scripts/01_filter_wgs_bins.sh
# bash scripts/02_run_rv_gwas.sh
# bash scripts/03_collect_rv_hits.sh
# python scripts/04_make_rv_score_files.py
# bash scripts/05_score_rv_prs.sh
# bash scripts/06_regenie_step0_prune.sh
# bash scripts/07_regenie_step1.sh
# bash scripts/08_regenie_step2.sh
# python scripts/09_select_burden_masks.py
# bash scripts/10_reestimate_burden_effects.sh
# python scripts/11_build_burden_prs.py
# python scripts/12_merge_prs.py
