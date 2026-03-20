#!/usr/bin/env python3
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
SELECTED_DIR = ROOT / "local_outputs" / "burden_selected"
REEST_DIR = ROOT / "local_outputs" / "burden_reestimate"
OUT_DIR = ROOT / "local_outputs" / "burden_prs"
OUT_DIR.mkdir(parents=True, exist_ok=True)
P_THRESHOLD = 2.18e-11

# This script expects locally downloaded PLINK2 re-estimation .glm files and
# per-sample additive burden dosage tables from:
#   plink2 --bfile step2_*_burden_masks_masks --recode A --out step2_*_per_sample
# The recode-A table is multiplied by re-estimated betas to produce the burden PRS.

for selected in sorted(SELECTED_DIR.glob('*.selected_masks.tsv')):
    trait = selected.stem.replace('.selected_masks', '')
    betas = {}
    for glm in (REEST_DIR / trait).glob('c*/*.glm.linear'):
        with glm.open() as fh:
            reader = csv.DictReader(fh, delimiter='\t')
            cols = {c.upper(): c for c in (reader.fieldnames or [])}
            id_col = cols.get('ID')
            beta_col = cols.get('BETA')
            p_col = cols.get('P')
            if not all([id_col, beta_col, p_col]):
                continue
            for row in reader:
                try:
                    if float(row[p_col]) <= P_THRESHOLD:
                        betas[row[id_col]] = float(row[beta_col])
                except ValueError:
                    pass
    out = OUT_DIR / f'{trait}.burden_beta_weights.tsv'
    with out.open('w') as fw:
        fw.write('ID\tBETA\n')
        for k, v in sorted(betas.items()):
            fw.write(f'{k}\t{v}\n')
    print(out)
