#!/bin/bash

# Quick QC example for the packaged inputs.
# Run from the repository root, or edit paths if running elsewhere.

python3 code/tails.py qc load \
  --in data/namedTraits.txt \
  --qcFiles data/qc/txt/*.txt \
  --out output_qc/qc \
  --showVariables

python3 code/tails.py qc filter \
  --in output_qc/qc.merged.txt \
  --out output_qc/qc \
  --applyFilters "sampleSize-target>50000 h2>0.05 snpmax<0.02 dist-skew<|2| uniq50>2 popQC-pass=True" \
  --dupeFile data/qc/gcorr.mat \
  --configFile data/qc/config.txt


  > ./code/tails.py qc filter --in output_qc/qc.merged.txt --out output_qc/qc --applyFilters "sampleSize-target>50000 h2>0.05 snpmax<0.02 dist-skew<|2| uniq50>2 popQC-pass=True" --dupeFile data/qc/gcorr.mat --configFile data/qc/config.txt --dupeCutoff 0
