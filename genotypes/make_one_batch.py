#!/bin/python
import sys
import os
import numpy as np
import pandas as pd
from itertools import izip 

__README__='''
Usage: python make_one_batch.py [Batch ID] [Chrom] [Out dir]

This tool chunks out individual-level data (L2R/BAF) from UK Biobank (shared app13721) for use with PennCNV.

Author: Matthew Aguirre (magu@stanford.edu)
'''

# get args
if len(sys.argv) < 4:
    print(__README__)
    sys.exit(1)
else:
    _,batch,chrom,outDir = sys.argv[:4]

# determine individual list
with open('/oak/stanford/projects/ukbb/genotypes/sample_app1372/ukb1372_cal_chr1_v2_s488374.fam', 'r') as f:
    # sample's row in the fam file is its column in the l2r/baf files
    inds={line.split()[0]:i for i,line in enumerate(f) if line.split()[5] == batch}

ixs = {v:k for k,v in inds.items()[:10]}
print(len(inds.values()), inds.values()[:10])

# get the data
refDir='/oak/stanford/projects/ukbb/genotypes/EGAD00010001226/001/'

# open both input files, store data for each individual 
# (memory-intensive but we only read the large files once
with open(os.path.join(refDir,'ukb_l2r_chr{}_v2.txt'.format(chrom)),'r') as i1:
    with open(os.path.join(refDir,'ukb_baf_chr{}_v2.txt'.format(chrom)),'r') as i2:
        cnv_data = ["\t".join(x) for ll in izip(i1,i2) for x in zip(*list(filter(lambda i: i in ixs, map(lambda x: enumerate(x.split()), ll))))]

# write out files
for iid,ix in inds:
    with open(os.path.join(outDir, '{0}_chr{1}_cnvInfo.app13721.{2}'.format(batch,chrom,iid)), 'w') as o:
        o.write("\t".join(cnv_data[:,ix]))
