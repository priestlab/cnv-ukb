import sys
import gzip
from numpy import mean
from scipy.stats import ttest_ind

def assess_pathway(gene_map, go_list=[], out_file='pathway_comp.txt'):
	# resources
	goAns="/oak/stanford/groups/jpriest/cnv_ukb/resources/go/goa_human.gaf.gz"
	goRel="/oak/stanford/groups/jpriest/cnv_ukb/resources/go/go.obo"
	# get genes associated with go pathway id
	go_to_gene = {}
	with gzip.open(goAns, 'r') as f:
		for line in f:
			if line[0] == '!': continue
			x = line.split()
			if x[2] not in gene_map: continue
			if go_list and x[3] not in go_list: continue
			if x[3] not in go_to_gene:
				go_to_gene[x[3]] = [x[2]]
			else:
				go_to_gene[x[3]].append(x[2])
	# get go names
	go_to_name = {}
	with open(goRel, 'r') as f:
		next_line = False
		for line in f:
			if line[:3] == 'id:':
				go = line.rstrip()[4:]
				if go in go_to_gene:
					next_line = True
			elif next_line:
				go_to_name[go] = line.rstrip()[6:]
				next_line = False	
	# format: go_id, mean_constraint, p_value, go_name
	with open(out_file, 'w') as f:
		for go in list(set(go_to_gene.keys()) & set(go_to_name.keys())):
			try:
				tstat, p = ttest_ind([s for g,s in gene_map.items() if g in go_to_gene[go]],
				                     [s for g,s in gene_map.items() if g not in go_to_gene[go]])
			except:
				tstat, p = "NA","NA"
			f.write('\t'.join([go, 
			                   str(mean([gene_to_score[gene] for gene in go_to_gene[go]])), 
			                   str(p), 
			                   go_to_name[go],
			                   str(len(go_to_gene[go]))])+'\n')
	return


if __name__ == '__main__':
	in_f ='output/cnv_dup_zscores_20190430.tsv'
	out_f='output/cnv_dup_go-enrichment_20190430.tsv'
	with open(in_f, 'r') as f:
		gene_to_score = {line.split()[0]:float(line.split()[1]) for line in f}
	assess_pathway( gene_map=gene_to_score, go_list=[], out_file=out_f )
