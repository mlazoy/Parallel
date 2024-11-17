import numpy as np
import matplotlib.pyplot as plt
import re
import sys

outfile = "omp_gameoflife_all.out" 

thread_pattern = r"Running with OMP_NUM_THREADS=(\d+)"
time_pattern = r"GameOfLife: Size (\d+) Steps 1000 Time ([\d.]+)"

with open (outfile, 'r') as fout:
    data = fout.read()

thread_vals = re.findall(thread_pattern, data)
time_vals = re.findall(time_pattern, data)

#print(thread_vals, time_vals)

results_mapping = {}

for i in range(0, len(thread_vals)):
    omp_num_thredas = int(thread_vals[i])

    for j in range(0,3):
        size = int(time_vals[i*3+j][0])
        time = float(time_vals[i*3+j][1])
        ## print(f"From {i,j} extracted size: {size} with time: {time}")

        if size not in results_mapping :
            results_mapping[size] = {}
        
        results_mapping[size][omp_num_thredas] = time

for idx, (size, omp_times) in enumerate(results_mapping.items()):
    print(f"Size: {size}, results: {omp_times}")
    
    # Create a new figure for each graph
    plt.figure(figsize=(8, 6))
    
    # Plot the original times
    plt.plot(omp_times.keys(), omp_times.values(), color='g', marker='o')
    
    # Plot the inverse times
    plt.plot(omp_times.keys(), [omp_times[1] / i for i in omp_times.keys()], color='lightblue', linestyle='--')
    
    # Add labels and title
    plt.title(f"Grid Size = {size}, Steps = 1000", fontstyle='oblique', size=12)
    plt.xlabel("OMP_NUM_THREADS")
    plt.ylabel("Time (secs)")
    plt.grid()
    
    # Show the plot
    plt.tight_layout()
    plt.savefig(f"grid{size}.svg", format="svg")




