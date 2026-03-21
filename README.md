# TAILS: Code and Resources for Tails Paper 

This repository contains all code and resources required to reproduce the analyses and figures presented in the TAILS manuscript.

The repository is divided into two main components:

- Summary-level analysis and figure generation (recommended for most users)
- Individual-level analysis pipelines (UK Biobank / DNAnexus dependent)

---

## Repository Structure

SummaryLevel/
IndividualLevel/

---

## 1. SummaryLevel/ (Primary user-facing component)

This directory contains all code required to:

- Perform summary-level analyses
- Reproduce all main and extended figures
- Run trait QC procedures
- Apply the POPout framework to summary statistics

This is the recommended entry point for users.

Key components:
- code/ — core Python implementation (QC + figure generation)
- data/ — example inputs and processed data used for figures
- docs/ — documentation and manual

Manual:
SummaryLevel/docs/manual/tailsManual.pdf

---

## Requirements

- Python (>=3.8)
- numpy
- scipy
- matplotlib
- statsmodels
- bash

---

## Basic Usage

cd SummaryLevel
../code/tails qc > traitset.out

cd make_figs
../code/tails draw --in ../qc_traits/traitset.out

---

## 2. IndividualLevel/ (Reproducibility pipelines)

Contains pipelines for:
- GWAS
- PRS construction
- Rare variant analyses
- Simulations

Requires:
- UK Biobank access
- DNAnexus / HPC environment

Included for reproducibility and further analysis for readers with biobank access. 

---

## Notes

Some figure inputs are derived from external sources such as:
- Neale Lab GWAS
- Backman et al. 2021 rare variant results

---

## Purpose

- Reproduce figures and analyses
- Provide full workflow transparency
- Separate user-accessible vs protected-data pipelines

---

## Support

See manual:
SummaryLevel/docs/manual/tailsManual.pdf
