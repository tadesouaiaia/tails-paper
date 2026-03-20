#!/bin/bash

# STEP 0) make output dirs 

#mkdir -p output_qc 
#mkdir -p output_figs 


# STEP 1) Run QC

./code/tails.py qc run --in data/namedTraits.txt --qcFile data/qc/txt/*.txt --useStandardFilters --dupeFile data/qc/gcorr.mat --configFile data/qc/config.txt --out output_qc/qc 

# STEP 2) Make Figures 


./code/tails.py gen all --in output_qc/qc.pass.txt --vals data/trait_data/vals/*.vals --pts data/trait_data/pts/*.pts  --simPath data/trait_sims/ --out output_figs/

# STEP 3) Make Extended Pdf 

cd xtended_latex_src/
./compileFigs.sh 
cd ..



echo "" 
echo "" 
echo "All Individual Figures and Table FIles can be found in output_figs" 
echo "A Single PDF of all Figures can be found at: xtended_latex_src/fullFigs.pdf" 
echo "A Supplemental Only Pdf Can be found at:     xtended_latex_src/supFigs.pdf" 
exit 


