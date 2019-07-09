import sys
import gzip
from numpy import mean
from scipy.stats import ttest_ind

def assess_pathway(gene_map, hpo_list=[], out_file='hpo_pathway_comp.txt'):
	# resources
	hpoTs="/oak/stanford/groups/jpriest/cnv_ukb/resources/HPO_pheno_to_gene.txt"
	# get genes and names for hpo terms
	hpo_to_gene, hpo_to_name = {}, {}
	with open(hpoTs, 'r') as f:
		# hpoId, hpoName, nGenes, Gene are the columns
		for line in f:
			x = line.rstrip().split("\t")
			if x[3] not in gene_map: continue
			if hpo_list and x[0] not in hpo_list: continue
			if x[0] not in hpo_to_gene:
				hpo_to_gene[x[0]] = [x[3]]
				hpo_to_name[x[0]] = x[1].replace(" ","_")
			else:
				hpo_to_gene[x[0]].append(x[3])
	# output format: hpo_id, mean_constraint, p_value, hpo_name
	with open(out_file, 'w') as f:
		for hpo in list(set(hpo_to_gene.keys()) & set(hpo_to_name.keys())):
			try:
				tstat, p = ttest_ind([s for g,s in gene_map.items() if g in hpo_to_gene[hpo]],
				                     [s for g,s in gene_map.items() if g not in hpo_to_gene[hpo]])
			except:
				tstat, p = "NA","NA"
			f.write('\t'.join([hpo, 
			                   str(mean([gene_to_score[gene] for gene in hpo_to_gene[hpo]])), 
			                   str(p), 
			                   hpo_to_name[hpo],
			                   str(len(hpo_to_gene[hpo]))])+'\n')
	return


if __name__ == '__main__':
	for kind in ['constraint','dup','del'][:1]:
		in_f ='output/cnv_'+kind+'_zscores_20190430.tsv'
		out_f='output/cnv_'+kind+'_hpo-enrichment_20190430.tsv'
		with open(in_f, 'r') as f:	
			gene_to_score = {line.split()[0]:float(line.split()[1]) for line in f}
		assess_pathway( gene_map=gene_to_score, hpo_list=[], out_file=out_f )
