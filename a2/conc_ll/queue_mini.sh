#!/bin/bash

## Give the Job a descriptive name
#PBS -N run_conc_ll_mini

## Output and error files
#PBS -o conc_ll_mini.out
#PBS -e conc_ll_mini.err

## Limit memory, runtime etc.
#PBS -l walltime=01:00:00

##Number of nodes aka threads 
#PBS -l nodes=1:ppn=8

cd /home/parallel/parlab09/conc_ll

num_threads=(1 8)
list_size=(1024)
operation_perc=("100-0-0" "80-10-10" "20-40-40" "0-50-50")

for l in "${list_size[@]}"; do
    echo -e "\nList Size: ${l}\n"
    for p in "${operation_perc[@]}"; do
        IFS="-" read -r p1 p2 p3 <<< "$p"
        echo -e "\nSearch: ${p1}%, Insert: ${p2}%, Delete: ${p3}%\n"
        # run serial first
        ./x.serial "$l" "$p1" "$p2" "$p3"
        for n in "${num_threads[@]}"; do
            #oversubscription for n=128
            if [ "$n" -eq 128 ]; then 
                export MT_CONF="$(seq -s, 0 63),$(seq -s, 0 63)"
            else 
                export MT_CONF="$(seq -s, 0 $((n - 1)))"
            fi
            echo -e "\nnum_threads=${n}: "
            # run 5 differnets configs
            echo "---cgl---"
            ./x.cgl "$l" "$p1" "$p2" "$p3"
            echo "---fgl---"
            ./x.fgl "$l" "$p1" "$p2" "$p3"
            echo "---lazy---"
            ./x.lazy "$l" "$p1" "$p2" "$p3"
            echo "---nb---"
            ./x.nb "$l" "$p1" "$p2" "$p3"
            echo "---opt---"
            ./x.opt "$l" "$p1" "$p2" "$p3"
        done
    done
done
