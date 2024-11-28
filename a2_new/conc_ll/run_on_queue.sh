#!/bin/bash

## Give the Job a descriptive name
#PBS -N run_conc_ll

## Output and error files
#PBS -o run_conc_ll.out
#PBS -e run_conc_ll.err

## How many machines should we get? 
#PBS -l nodes=1:ppn=8

##How long should the job run for?
#PBS -l walltime=01:00:00

## Start 
## Run make in the src folder (modify properly)

module load openmp
cd /home/parallel/parlab09/a2_new/a2/conc_ll

choices=(
    "100 0 0"
    "80 10 10"
    "20 40 40"
    "0 50 50"
)

for lsize in 1024 8192; do
	export LSIZE=$lsize
	echo "LSIZE=$LSIZE"
	for choice in "${choices[@]}"; do
		read -r CONTAINS_PCT ADD_PCT REMOVE_PCT <<< "$choice"
		export MT_CONF="0"
		echo "serial"
		./x.serial $LSIZE $CONTAINS_PCT $ADD_PCT $REMOVE_PCT
		for n in 1 2 4 8 16 32 64 128; do
			if [ "$n" -eq 128 ]; then
				# Special case for n=128 for over subscription
				export MT_CONF="$(seq -s, 0 63),$(seq -s, 0 63)"
			else
				# Default case for n=1, 2, 4, ..., 64
				export MT_CONF=$(seq -s, 0 $((n-1)))
			fi
                        echo "coarse-grain"
                        ./x.cgl $LSIZE $CONTAINS_PCT $ADD_PCT $REMOVE_PCT
                        echo "fine-grain"
                        ./x.fgl $LSIZE $CONTAINS_PCT $ADD_PCT $REMOVE_PCT
                        echo "optimistic"
                        ./x.opt $LSIZE $CONTAINS_PCT $ADD_PCT $REMOVE_PCT
                        echo "lazy"
                        ./x.lazy $LSIZE $CONTAINS_PCT $ADD_PCT $REMOVE_PCT
                        echo "non-blocking"
                        ./x.nb $LSIZE $CONTAINS_PCT $ADD_PCT $REMOVE_PCT
		done
	done
done
