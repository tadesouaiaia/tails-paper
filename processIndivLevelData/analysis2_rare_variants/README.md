# DNAnexus rare-variant and burden PRS pipeline

This repository contains only the DNAnexus portion of the Tails analysis.
It starts after phenotype normalization. The phenotype files are not included here because they are private. The user must provide phenotype files on DNAnexus.

## Important points

- The phenotype files used here are already normalized / residualized for all desired covariates.
- No covariate file is used anywhere in this pipeline.
- Common-variant PRS generation is not part of this repository.
- This pipeline adds three rare-derived scores to a pre-existing common PRS:
  - rare PRS 1: `0.1% < MAF < 1%`
  - rare PRS 2: `0.01% < MAF < 0.1%`
  - burden PRS from WES REGENIE analysis

## Trait list

- `templates/traits.txt` is the single trait list used by this pipeline.
- By default it contains the 45 traits used in the paper:
  `20015, 20256, 23105, 23106, 23129, 30000, 30010, 30020, 30040, 30060, 30070, 30090, 30120, 30130, 30140, 30150, 30180, 30190, 30200, 30210, 30240, 30250, 30260, 30270, 30280, 30600, 30630, 30680, 30690, 30700, 30740, 30750, 30770, 30810, 30830, 30850, 30860, 30870, 30890, 3143, 3144, 3148, 3581, 46, 50`
- Users can replace this file with their own trait IDs if they want to run the same workflow on a different set of traits.

## Setup

1. Copy `config.example.sh` to `config.sh` if needed and edit the paths.
2. Put your phenotype files on DNAnexus. This pipeline assumes files like:
   - `${BASE_PHENO_DIR}/TRAIT.base`
   - `${TARGET_PHENO_DIR}/TRAIT.target`
3. Make sure those phenotype values are already adjusted for age, sex, PCs, and any other covariates you want, because no extra covariates are used here.

## Run order

```bash
bash scripts/01_filter_wgs_bins.sh
bash scripts/02_run_rv_gwas.sh
bash scripts/03_collect_rv_hits.sh
python scripts/04_make_rv_score_files.py
bash scripts/05_score_rv_prs.sh
bash scripts/06_regenie_step0_prune.sh
bash scripts/07_regenie_step1.sh
bash scripts/08_regenie_step2.sh
python scripts/09_select_burden_masks.py
bash scripts/10_reestimate_burden_effects.sh
python scripts/11_build_burden_prs.py
python scripts/12_merge_prs.py
```

## Script summary

- `01_filter_wgs_bins.sh`: make the two WGS rare-variant bins.
- `02_run_rv_gwas.sh`: run PLINK2 GWAS for the traits listed in `templates/traits.txt`.
- `03_collect_rv_hits.sh`: download and collect hits at `P <= 2.18e-11`.
- `04_make_rv_score_files.py`: build score files for the two rare PRSs.
- `05_score_rv_prs.sh`: score rare PRS in the target sample.
- `06_regenie_step0_prune.sh`: prune WES variants for REGENIE Step 1.
- `07_regenie_step1.sh`: run REGENIE Step 1 on the 45 follow-up traits.
- `08_regenie_step2.sh`: run REGENIE Step 2 burden tests.
- `09_select_burden_masks.py`: remove masks overlapping rare-PRS variants and keep the best remaining mask per gene.
- `10_reestimate_burden_effects.sh`: re-estimate burden effects in the base subset.
- `11_build_burden_prs.py`: build burden beta weight tables.
- `12_merge_prs.py`: merge common, rare1, rare2, and burden PRS tables locally.


