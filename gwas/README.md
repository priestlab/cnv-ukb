# CNV GWAS and Burden Test

This directory contains [PLINK2](https://www.cog-genomics.org/plink/2.0/) wrapper scripts used to compute CNV GWAS and genic CNV burden tests.

## Options used for computation:
- **Firth-fallback:** For binary traits, attempt [Firth regression](https://academic.oup.com/biomet/article/80/1/27/228364) if standard gradient descent methods fail to converge.
- **White British population subset:** Compute associations within a subset of ~335,000 unrelated individuals of self-reported white British individuals.
- **Covariates:** Age, sex, 4 genomic principal components (provided by UK Biobank), total length of CNV\*, CNV count\*.

\* Denotes covariates used only for the genic burden test.

## Data availability
All summary stats described in the manuscript are available on the [Global Biobank Engine](biobankengine.stanford.edu/downloads), along with a complete list of phenotypes with data packaged in the release at the time of publication.
