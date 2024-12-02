#!/bin/bash

## Give the Job a descriptive name
#PBS -N run_kmeans_locks

## Output and error files
#PBS -o lock_kmeans.out
#PBS -e lock_kmeans.err

## How many machines should we get? 
#PBS -l nodes=1:ppn=8

##How long should the job run for?
#PBS -l walltime=01:00:00

## Start 
## Run make in the src folder (modify properly)

module load openmp
cd /home/parallel/parlab09/kmeans_sync
SIZE=32
COORDS=16
CLUSTERS=32
LOOPS=10

for n in 1 2 4 8 16 32 64; do
    echo -e "\nnum_threads=${n}"
    export OMP_NUM_THREADS=${n}
    export GOMP_CPU_AFFINITY="$(seq -s, 0 &((n - 1)))"
    echo -e "\nnosync_lock"
    ./kmeans_omp_nosync_lock -s <SIZE> -n <COORDS> -c <CLUSTERS> -l <LOOPS>
    echo -e "\npthread_mutex_lock"
    ./kmeans_omp_pthread_mutex_lock -s <SIZE> -n <COORDS> -c <CLUSTERS> -l <LOOPS>
    echo -e "\npthread_spin_lock"
    ./kmeans_omp_pthread_spin_lock -s <SIZE> -n <COORDS> -c <CLUSTERS> -l <LOOPS>
    echo -e "\ntas_lock"
    ./kmeans_omp_tas_lock -s <SIZE> -n <COORDS> -c <CLUSTERS> -l <LOOPS>
    echo -e "\nttas_lock"
    ./kmeans_omp_ttas_lock -s <SIZE> -n <COORDS> -c <CLUSTERS> -l <LOOPS>
    echo -e "\narray_lock"
    ./kmeans_omp_array_lock -s <SIZE> -n <COORDS> -c <CLUSTERS> -l <LOOPS>
    echo -e "\nclh_lock"
    ./kmeans_omp_clh_lock -s <SIZE> -n <COORDS> -c <CLUSTERS> -l <LOOPS>
done