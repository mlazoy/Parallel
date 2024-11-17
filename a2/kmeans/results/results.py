import numpy as np
import matplotlib.pyplot as plt
#import pandas
import re

regex_total = r"\(total\s*=\s*([\d.]+)s\)"
regex_loop = r"\(per\s+loop\s*=\s*([\d.]+)s\)"

total_times = []
loop_times = []

with open("results.txt", 'r') as file:
    for line in file:
        match_total = re.search(regex_total, line)
        match_loop = re.search(regex_loop, line)
        if (match_total is not None and match_loop is not None):
            total_times.append(float(match_total.group(1)))
            loop_times.append(float(match_loop.group(1)))


seq_totals = total_times[0:2]
seq_loop = loop_times[0:2]

total_times = total_times[2::]
loop_times = loop_times[2::]

print("Sequential Times: ", seq_totals, seq_loop)
print("Total Times:", total_times)
print("Loop Times:", loop_times)

threads = [1,2,4,8,16,32,64]
nthreads = len(threads)
titles = ["Shared Clusters (naive)", 
          "Shared Clusters with GOMP_CPU_AFFINITY set", 
          "Copied Clusters & Reduction", 
          "Copied Clusters & Reduction", 
          "Copied Clusters & Reduction with First-Touch Policy",
          "Copied Clusters & Reduction with First-Touch Policy & NUMA-aware initialization",
          "Copied Clusters & Reduction with First-Touch Policy & NUMA-aware initialization",
          "Shared Clusters with GOMP_CPU_AFFINITY[0-7][32-40]"]

subtitles = ["{Size, Coords, Clusters, Loops} = {256, 16, 32, 10}",
             "{Size, Coords, Clusters, Loops} = {256, 1, 4, 10}",
             "{Size, Coords, Clusters, Loops} = {256, 16, 32, 10}"]

for i in range(0,8):
    x_axis = threads
    y_axis = total_times[i*nthreads:i*nthreads+nthreads]
    if (i==3 or i==4 or i==5) : seq_time = seq_totals[1]
    else: seq_time = seq_totals[0]
    print(f"Times for version{i}: ", y_axis)
    plt.figure(figsize=(8,6))
    plt.gca().set_facecolor("#e6e6fa")
    plt.xscale('log')
    widths = 0.6*np.diff(threads, prepend=threads[0] / 2) * 0.8
    plt.bar(x_axis, y_axis, width=widths, color="#4b0082", align="center")
    plt.xticks(x_axis, [str(t) for t in threads])
    plt.plot(x_axis, [seq_time/t for t in threads], color ='g', linestyle='--')
    plt.suptitle(titles[i], size = 12)
    plt.title(subtitles[int(i/3)], fontstyle = 'oblique', size = 10)
    plt.xlabel("Number of threads")
    plt.ylabel("Time(secs)")
    plt.grid('y')
    plt.savefig(f"fig{i}.png")
    plt.clf()