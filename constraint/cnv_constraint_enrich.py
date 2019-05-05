import numpy as np
import pandas as pd
from scipy.stats import ttest_ind
import time

zs = pd.read_table('/oak/stanford/groups/jpriest/cnv_ukb/cnv_constraint_zscores_20190430.tsv',
                   names=['Gene','z','pLI'], 
                   index_col='Gene')

sets = pd.read_table('/oak/stanford/groups/jpriest/cnv_ukb/resources/HPO_pheno_to_gene.txt', skiprows=0,
                     names=['hpoID','hpolabel','geneID','Gene'])

load = False
if load:
    hpo_t = pd.read_table("/oak/stanford/groups/jpriest/cnv_ukb/cnv_constraint_hpo_enrichment_20181217.tsv")
else:
    hpo_t = pd.DataFrame()
    t = time.time()
    for hpo in sets['hpoID'].value_counts().index:
        # select rows
        in_set = sets.query('hpoID == @hpo and Gene in @zs.index')
        out_of_set = sets.query('hpoID != @hpo and Gene in @zs.index')
        if in_set.shape[0] == 0 or out_of_set.shape[0] == 0:
            continue
        # select genes
        in_set_z = zs.loc[in_set['Gene'],'z']
        out_of_set_z = zs.loc[out_of_set['Gene'],'z']
        # compute mean shift, t-test p-value
        deltaZ = in_set_z.mean() - out_of_set_z.mean()
        _,p = ttest_ind(in_set_z.values, out_of_set_z.values, equal_var=False, nan_policy='omit')
        # append
        hpo_t = hpo_t.append([[hpo, in_set.iloc[0,:]['hpolabel'], deltaZ, p, in_set_z.shape[0]]])
        if hpo_t.shape[0] % 200 == 0:
            print(hpo_t.shape[0], time.time()-t)
            t=time.time()
    hpo_t.columns = ['hpoID','hpoLabel','deltaZ','pValue','nGenes']

hpo_t['pValue'] = hpo_t['pValue'].astype(float)

if not load:
    hpo_t.to_csv('/oak/stanford/groups/jpriest/cnv_ukb/cnv_constraint_hpo_enrichment_20190430.tsv', 
                 sep='\t', index=False)