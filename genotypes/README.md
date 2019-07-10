# CNV Calling in UK Biobank

In brief, CNVs were called within each UK Biobank genotyping batch, with one round of computation (model building and evaluation) for each chromosome. 

## Steps:

1. **Estimate genomic runs of homozygosity (ROH) for each sample:** <br/>
Log files from the PLINK commands used for computation are in the `roh` subdirectory. See [this paper](https://www.ncbi.nlm.nih.gov/pubmed/21943305) for more info on genomic ROH.

2. **Select training samples to exclude:** `select_train.py`. <br/>
This is a requirement for model building with PennCNV. To reduce the number of samples lost to training, this set was fixed for each batch across all chromosomes.

3. **Call CNV:** `call_cnv_by_batch.sh`. <br/>
Note that the design of this pipeline (i.e. paths to files, and the need to split files from a master file with `make_one_batch.py`) was specific to our lab computing environment. In principle, this script could be reused to call CNV with another setup, provided the paths/resulting split files are amended. 

## Extras

The notebook used to make the CNV [reference panel](https://biobankengine.stanford.edu/downloads) is also included: `cnv_reference_panel.ipynb`

As is the panel itself: `ukb_cnv_reference.tsv.gz`.

Population allele frequencies were computed with PLINK. Each reference population consists of a set of unrelated individuals grouped by genomic principal components and using self-reported ancestry. A manuscript describing these population definitions is forthcoming from the [Rivas Lab](http://med.stanford.edu/rivaslab/publications.html).
