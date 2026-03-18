# TAILS pipeline package

This package contains the code and bundled example inputs needed to reproduce the **trait QC** and **figure-generation** steps used for the TAILS manuscript.

The workflow has two stages:

1. **QC pipeline**: merge per-trait QC summaries, inspect available variables, apply filters, and remove near-duplicate traits.
2. **Figure-generation pipeline**: read the QC-passed trait file together with `.vals` / `.pts` analysis outputs and generate manuscript figures, extended-data figures, and CSV tables.

For full documentation please see `tailsManual.pdf` in the docs directory. 

## Package layout

- `code/tails.py` — main command-line entry point
- `code/src/` — pipeline source code
- `data/` — bundled inputs used by the packaged examples
- `docs/manual/manual.pdf` — user manual
- `docs/manual/manual.tex` — LaTeX source for the manual
- `docs/README.qc` — shell example for the QC stage
- `docs/README.gen` — shell example for the figure-generation stage
#- `xtended_latex_src/` — LaTeX source for the compiled extended-data PDF
- `run_all.sh` — example end-to-end script

## Requirements

### System requirements

- Linux or macOS shell environment 
- Python 3.10+ recommended [See Packages Below] 
- `bash` (if you want to use the runall.sh single command script) 

### Python packages

The figure-generation code checks for the following Python modules:

- `matplotlib`
- `numpy`
- `scipy`
- `statsmodels`

Notes:
- The QC stage is lighter, but in practice it is simplest to install the same environment for both stages.

A minimal install is typically:

```bash
python3 -m pip install matplotlib numpy scipy statsmodels 
```

## Quick start

### 1. Run QC

```bash
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
```

This produces `output_qc/qc.pass.txt`, which is the standard input for figure generation.

### 2. Generate figures

```bash
python3 code/tails.py gen all \
  --in output_qc/qc.pass.txt \
  --vals data/trait_data/vals/*.vals \
  --pts data/trait_data/pts/*.pts \
  --simPath data/trait_sims/ \
  --out output_figs/
```

## Documentation

The main manual is here:

- `docs/manual/manual.pdf`

The LaTeX source is here:

- `docs/manual/manual.tex`

A short documentation index is also provided at:

- `docs/README.md`

## CLI summary

Top-level commands:

```bash
python3 code/tails.py qc
python3 code/tails.py gen
```

Useful help commands:

```bash
python3 code/tails.py -h
python3 code/tails.py qc -h
python3 code/tails.py qc load -h
python3 code/tails.py qc filter -h
python3 code/tails.py qc run -h
python3 code/tails.py gen help
```

`tails gen -h` is intentionally minimal; `tails gen help` shows the generation targets.

## Notes

- `--out` for the QC stage is an **output prefix**, not a directory. For example, `--out output_qc/qc` creates files such as `output_qc/qc.merged.txt` and `output_qc/qc.pass.txt`.
- `--out` for the figure-generation stage is an output directory or prefix for generated figures and tables.
- The standard QC filter set used by `--useStandardFilters` is:

```text
sampleSize-target>50000 h2>0.05 snpmax<0.02 dist-skew<|2| uniq50>2 popQC-pass=True
```

- The packaged examples assume the input files remain in the bundled `data/` layout.
