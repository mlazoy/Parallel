#!/bin/bash

## Give the Job a descriptive name
#PBS -N run_kmeans

## Output and error files
#PBS -o gomp_hyper_kmeans.out
#PBS -e gomp_hyper_kmeans.err

## How many machines should we get? 
#PBS -l nodes=1:ppn=8

##How long should the job run for?
#PBS -l walltime=00:10:00

## Start 
## Run make in the src folder (modify properly)

module load openmp
cd /home/parallel/parlab09/kmeans

Size=256
Coords=16
Clusters=32
Loops=10 

for i in 1 2 4 8 16 32 64; do
    export OMP_NUM_THREADS=$i
    
    if [[ $i -eq 16 ]]; then
        export GOMP_CPU_AFFINITY="$(seq -s, 0 7),$(seq -s, 32 39)"
    else
        export GOMP_CPU_AFFINITY="$(seq -s, 0 $((i - 1)))"
    fi
    
    ./kmeans_omp_naive -s $Size -n $Coords -c $Clusters -l $Loops
done