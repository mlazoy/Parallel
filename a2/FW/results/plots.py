# import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
#import pandas


total_times = []
loop_times = []

with open("sandman.out", 'r') as file:
    for line in file:
        if (line.startswith("omp_num_threads")):
            t = float(line.split(',')[-1])
            if (t is not None):
                total_times.append(t)


print("Total Times:", total_times)
print("Loop Times:", loop_times)

threads = [1,2,4,8,16,32,64]
GridSize = [1024, 2048, 4096]
BSizes = [256, 128, 64, 32, 16]
nthreads = len(threads)

for grid in range (0,len(GridSize)):
    for bsize in range(0,len(BSizes)):
        start_idx = grid*(nthreads*len(BSizes)) + nthreads*bsize
        end_idx = start_idx + nthreads
        x_axis = threads
        y_axis = total_times[start_idx:end_idx]
        print(f"Times for S={GridSize[grid]}, BS={BSizes[bsize]}: ", y_axis)
        plt.figure(figsize=(8,6))
        plt.gca().set_facecolor("#e6e6fa")
        plt.xscale('log')
        widths = 0.6*np.diff(threads, prepend=threads[0] / 2) * 0.8
        plt.bar(x_axis, y_axis, width=widths, color="#4b0082", align="center")
        plt.xticks(x_axis, [str(t) for t in threads])
        plt.plot(x_axis, [y_axis[0]/t for t in threads], color ='g', linestyle='--')
        plt.suptitle("Total Times for Floyd-Warshall Recursive", size = 12)
        plt.title(f"Grid Size = {GridSize[grid]}, Block Size = {BSizes[bsize]}", fontstyle = 'oblique', size = 10)
        plt.xlabel("Number of threads")
        plt.ylabel("Time(secs)")
        plt.grid('y')
        plt.savefig(f"fig{GridSize[grid]}_{BSizes[bsize]}.png")
        plt.clf()