#!/bin/bash

# define command line arguments for phenotype, name, app_id, bin/qt (needed?)
# usage: script.sh phe_name app_id path/to/file.phe bin/qt

pheID=$1
appID=$2
pheFile=$3
if [ "$4" == "bin" ]; then
	kind="firth-fallback"
elif [ "$4" == "qt" ]; then
	kind=""
else
	echo "unrecognized gwas type $4"
	exit 2
fi

# useful
dataRoot="/oak/stanford/groups/jpriest/cnv_ukb"
ml load plink2

# plink command
plink2 --bed "${dataRoot}/resources/all.cnv.ac-gt23.af1-20000.bed" \
       --bim "${dataRoot}/resources/all.cnv.ac-gt23.af1-20000.bim" \
       --fam "${dataRoot}/resources/all.cnv.ac-gt23.af1-20000.app${appID}.fam" \
       --glm hide-covar ${kind} \
       --pheno ${pheFile} \
       --covar "${dataRoot}/gwas/resources/ukb${appID}_CNV-GWAS.covar" \
       --covar-name age sex PC1-PC4 \
       --keep "${dataRoot}/gwas/resources/ukb${appID}_CNV-GWAS.wb-unrel.keep.txt" \
       --out "${dataRoot}/gwas/output/${pheID}.cnv.ac-gt23" 
