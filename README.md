# UK Biobank CNV Analysis

This is the repository for ["Phenome-wide Burden of Copy Number Variation in UK Biobank"](https://pmc.ncbi.nlm.nih.gov/articles/PMC6699064/) (Aguirre M, Rivas MA, Priest JR, AJHG 2019). Contents are as below, in respective folders:

1. `constraint`: Contains a Jupyter notebook which implements a null model of genic CNV used to estimate selective constraint, as well as scripts used to compute gene set enrichment analysis using the resulting constraint scores.

2. `figures`: Contains notebooks used to generate figures and tables for the manuscript.

3. `genotypes`: Contains scripts used to call CNVs using UK Biobank data, as well as a Jupyter notebook used to make the reference panel (available for download here, or on the [Global Biobank Engine](biobankengine.stanford.edu/downloads)).

4. `gwas`: Contains scripts used for genome-wide association of CNVs, and genic burden tests of CNVs. Summary stats available at the Global Biobank Engine link above.

Correspondence to Matthew Aguirre (magu) and James Priest (jpriest): username -at- stanford -dot- edu.
