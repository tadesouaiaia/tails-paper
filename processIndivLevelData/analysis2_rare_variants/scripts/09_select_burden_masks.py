#!/usr/bin/env python3
from pathlib import Path
import csv
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
STEP2 = ROOT / "local_outputs" / "burden_step2"
RV_HITS = ROOT / "local_outputs" / "rv_hits"
OUT = ROOT / "local_outputs" / "burden_selected"
OUT.mkdir(parents=True, exist_ok=True)
P_THRESHOLD = 2.18e-11

# This script expects the user to first download per-trait Step 2 .regenie files and
# corresponding *_masks.snplist files into local_outputs/burden_step2/<trait>/.
# It removes masks that contain variants already used by the two rare single-variant PRSs,
# then keeps the lowest-p mask per gene.

def read_rv_variants(trait: str):
    vids = set()
    for path in RV_HITS.glob(f"{trait}.rare*.hits.tsv"):
        with path.open() as fh:
            reader = csv.DictReader(fh, delimiter='\t')
            for row in reader:
                vids.add(row.get('ID') or row.get('Id') or row.get('id'))
    return {v for v in vids if v}

for trait_dir in sorted(STEP2.glob('*')):
    if not trait_dir.is_dir():
        continue
    trait = trait_dir.name
    rv_vars = read_rv_variants(trait)
    mask_to_vars = defaultdict(set)
    for snp_path in trait_dir.glob('*_masks.snplist'):
        with snp_path.open() as fh:
            for line in fh:
                parts = line.strip().split()
                if len(parts) >= 2:
                    mask, variant = parts[0], parts[1]
                    mask_to_vars[mask].add(variant)
    per_gene = {}
    for reg in trait_dir.glob('*.regenie'):
        with reg.open() as fh:
            reader = csv.DictReader(fh, delimiter=' ')
            fields = [f for f in (reader.fieldnames or []) if f]
        if not fields:
            continue
        # Robust second pass with whitespace splitting
        with reg.open() as fh:
            header = fh.readline().strip().split()
            idx = {c: i for i, c in enumerate(header)}
            gene_col = 'GENE' if 'GENE' in idx else header[0]
            mask_col = 'MASK' if 'MASK' in idx else ('ID' if 'ID' in idx else header[1])
            p_col = 'P' if 'P' in idx else ('PVAL' if 'PVAL' in idx else header[-1])
            for line in fh:
                vals = line.strip().split()
                if len(vals) != len(header):
                    continue
                gene = vals[idx[gene_col]]
                mask = vals[idx[mask_col]]
                try:
                    p = float(vals[idx[p_col]])
                except ValueError:
                    continue
                if p > P_THRESHOLD:
                    continue
                if mask_to_vars.get(mask, set()) & rv_vars:
                    continue
                if gene not in per_gene or p < per_gene[gene][1]:
                    per_gene[gene] = (mask, p)
    out = OUT / f"{trait}.selected_masks.tsv"
    with out.open('w') as fw:
        fw.write("GENE\tMASK\tP\n")
        for gene, (mask, p) in sorted(per_gene.items()):
            fw.write(f"{gene}\t{mask}\t{p}\n")
    print(out)
