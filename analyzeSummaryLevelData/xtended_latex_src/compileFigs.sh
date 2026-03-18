#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FIGDIR=$SCRIPT_DIR"/../output_figs" 




ALL=$SCRIPT_DIR"/fullFigs.tex" 
SUP=$SCRIPT_DIR"/supFigs.tex" 


echo "Compiling All Figs : "$ALL"......"  
pdflatex "\def\figdir{$FIGDIR}\input{$ALL}" > allRun.log 

echo "Compiling Sup Figs : "$SUP"......"  
pdflatex "\def\figdir{$FIGDIR}\input{$SUP}" > supRun.log 


echo "Latex Compilation Finished" 
exit 

echo #$

exit 
exit

