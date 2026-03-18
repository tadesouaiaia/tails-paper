#!/usr/bin/env python3
from pathlib import Path
import csv
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
RV_DIR = ROOT / 'local_outputs' / 'rv_prs'
BURDEN_DIR = ROOT / 'local_outputs' / 'burden_prs'
COMMON_DIR = ROOT / 'local_outputs' / 'common_prs'
OUT_DIR = ROOT / 'local_outputs' / 'merged_prs'
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Expected local files per trait:
#   rv_prs/<trait>.rare1.sscore
#   rv_prs/<trait>.rare2.sscore
#   burden_prs/<trait>.burden.sscore or burden table with IID/FID/SCORE
#   common_prs/<trait>.common.sscore

for common in sorted(COMMON_DIR.glob('*.common.sscore')):
    trait = common.name.replace('.common.sscore', '')
    files = {
        'common': common,
        'rare1': RV_DIR / f'{trait}.rare1.sscore',
        'rare2': RV_DIR / f'{trait}.rare2.sscore',
        'burden': BURDEN_DIR / f'{trait}.burden.sscore',
    }
    rows = defaultdict(lambda: {'FID': None, 'IID': None, 'common': 0.0, 'rare1': 0.0, 'rare2': 0.0, 'burden': 0.0})
    for label, path in files.items():
        if not path.exists():
            continue
        with path.open() as fh:
            header = fh.readline().strip().split()
            idx = {c: i for i, c in enumerate(header)}
            fid_i = idx.get('FID', 0)
            iid_i = idx.get('IID', 1)
            score_i = idx.get('SCORE1_SUM', idx.get('SCORE', len(header)-1))
            for line in fh:
                vals = line.strip().split()
                if len(vals) <= score_i:
                    continue
                fid, iid = vals[fid_i], vals[iid_i]
                key = (fid, iid)
                rows[key]['FID'] = fid
                rows[key]['IID'] = iid
                rows[key][label] = float(vals[score_i])
    out = OUT_DIR / f'{trait}.merged_prs.tsv'
    with out.open('w') as fw:
        fw.write('FID\tIID\tPRS_common\tPRS_rare1\tPRS_rare2\tPRS_burden\tPRS_total\n')
        for (fid, iid), d in sorted(rows.items()):
            total = d['common'] + d['rare1'] + d['rare2'] + d['burden']
            fw.write(f"{fid}\t{iid}\t{d['common']}\t{d['rare1']}\t{d['rare2']}\t{d['burden']}\t{total}\n")
    print(out)
