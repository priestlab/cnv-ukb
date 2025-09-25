#!/bin/bash
set -xeuo

# IMPORTANT: check that you've already selected n=100 individuals per batch for training!

# Optional: chunk individual files before calling this script
# otherwise leave line 38 uncommented (calls make_one_batch.py)

# assume this is called by an array handler, with 22 * n_batches parellel jobs
taskid=$1

# reference
ind_storage=$SCRATCH/PennCNV/chunked/ # output directory
cnvtools=/scratch/users/aldocp/share/PennCNV-1.0.4 # path to pennCNV
batch_list=batches.lst

# determine batch ID
batch=$(cat $batch_list | awk '{for (i=0; i<22; i++){print}}' | awk -v line=$taskid '(NR==line){print}')
chrom=$(expr $(expr $(expr $taskid + 20) % 22) + 1)
run_id=${batch}_chr${chrom}
ind_storage=$ind_storage/$batch
echo $run_id

# don't run if we already have the files for this batch/chrom
if [ -f ${ind_storage}/${run_id}.rawcnv ]; then 
    echo "Run for batch ${batch}_c${chrom} already done!"; 
    exit 5; 
fi

# directory fun
ind_storage=$ind_storage/$batch
out_dir=$SCRATCH/cnv_ukb/results/$batch
mkdir -p $ind_storage
mkdir -p $out_dir
cd $out_dir

# make individual files
python make_one_batch.py $batch $chrom $ind_storage

# test/train split -- leverage pre-existing split to enumerate files in each grouping
# all
find $ind_storage -type f | grep "_chr${chrom}_" | sort > ${run_id}_fullsignalfilelist.txt 
# train
comm -12 <(sort $SCRATCH/PennCNV/reference/${batch}_trainIndividuals.lst) <(cat ${run_id}_fullsignalfilelist.txt | rev | awk -F'.' '{print $1}' | rev | sort | uniq) | xargs -i find $ind_storage -name "*{}*" | grep "_chr${chrom}_" > ${run_id}_trainsignalfilelist.txt 
# test
comm -23 ${run_id}_fullsignalfilelist.txt ${run_id}_trainsignalfilelist.txt > ${run_id}_testsignalfilelist.txt

# generate pfb, gcmodel
$cnvtools/compile_pfb.pl --listfile ${run_id}_fullsignalfilelist.txt -output ukb_${run_id}.pfb
$cnvtools/cal_gc_snp.pl ${cnvtools}/misc/gc5Base.txt ukb_${run_id}.pfb -output ukb_${run_id}.gcmodel	

# fit model, run evaluations
$cnvtools/detect_cnv.pl -train -hmm ${cnvtools}/gw6/lib/affygw6.hmm -pfb ukb_${run_id}.pfb --listfile ${run_id}_trainsignalfilelist.txt -log train_${run_id}.log -out train_${run_id}.rawcnv
$cnvtools/detect_cnv.pl -test -hmm train_${run_id}.rawcnv.hmm -pfb ukb_${run_id}.pfb --listfile ${run_id}_testsignalfilelist.txt -log test_${run_id}.log -out ${run_id}.rawcnv

rm -rf ${ind_storage}/*"_chr${chrom}_"*
