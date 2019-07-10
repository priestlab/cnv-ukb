# UK Biobank CNV constraint

Briefly, gene-level tolerance to CNV is estimated empirically using a linear model based on features relevant to structural mutagenesis (after [Ruderfer et. al., Nat. Gen. 2016](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5042837/)). Given resulting estimates of constraint, perform set enrichment analysis (_t_-test) using terms from the [Gene Ontology Consortium](http://geneontology.org/docs/download-go-annotations/) or [Human Phenotype Ontology](https://hpo.jax.org/app/download/annotation). 

## Steps

1. After calling CNV, estimate null model of genic CNV/deletion/duplication: `model.ipynb`.

2. Given constraint z-scores, perform gene-set enrichment: `enrichment_go.py` and `enrichment_hpo.py`

3. Visualize enrichment results: `enrich.ipynb`

Full tables of constraint scores and enrichment results are in the `output` directory.
