#!/usr/bin/env python3
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
IN_DIR = ROOT / "local_outputs" / "rv_hits"
OUT_DIR = ROOT / "local_outputs" / "rv_scores"
OUT_DIR.mkdir(parents=True, exist_ok=True)

for path in sorted(IN_DIR.glob("*.hits.tsv")):
    with path.open() as fh:
        reader = csv.DictReader(fh, delimiter='\t')
        cols = {c.upper(): c for c in (reader.fieldnames or [])}
        id_col = cols.get('ID')
        a1_col = cols.get('A1')
        beta_col = cols.get('BETA')
        if not all([id_col, a1_col, beta_col]):
            raise SystemExit(f"Missing ID/A1/BETA in {path}")
        out = OUT_DIR / path.name.replace('.hits.tsv', '.score.tsv')
        with out.open('w') as fw:
            for row in reader:
                fw.write(f"{row[id_col]}\t{row[a1_col]}\t{row[beta_col]}\n")
    print(out)
