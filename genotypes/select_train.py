#!/bin/python
import random

random.seed(a=94019)

fam_file = '/oak/stanford/projects/ukbb/genotypes/sample_app1372/ukb1372_cal_chr1_v2_s488374.fam'
het_runs_reference = 'roh/ukb_ALL_Hom_lLD_65.hom.indiv'

cutoff = 20000 # roh length, in kB
n_train = 100

with open(het_runs_reference, 'r') as ref, open(fam_file, 'r') as fam:
    ind_roh_len = {}
    for i,line in enumerate(ref):
        if i > 0:
            x = line.split()
            ind_roh_len[x[0]] = float(x[4])
    train = {}
    for line in fam:
        x = line.split()
        if x[0] in ind_roh_len and ind_roh_len[x[0]] < cutoff:
            if x[5] not in train:
                train[x[5]] = []
            train[x[5]].append(x[0])

for batch in train:
    train_samples = random.sample(train[batch], 101)
    with open('/scratch/users/magu/PennCNV/reference/' + batch + '_trainIndividuals.lst', 'w') as o:
        o.write('\n'.join(train_samples))    
