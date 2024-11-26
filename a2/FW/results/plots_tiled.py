# import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
#import pandas


total_times = {}

with open("smd.out", 'r') as file:
    lines = file.readlines()  # Read all lines at once
    for i, line in enumerate(lines):
        if line.startswith("Number of threads"):
            n = int(line.split(':')[-1].strip())
            
            if i + 1 < len(lines):  # Ensure next line exists
                next_line = lines[i + 1]
                t = float(next_line.split(',')[-1].strip())
                total_times[n] = t


print("Total Times:", total_times)


threads = list(total_times.keys())
times = list(total_times.values())

plt.figure(figsize=(8,6))
plt.gca().set_facecolor("#e6e6fa")
plt.xscale('log')
widths = 0.6*np.diff(threads, prepend=threads[0] / 2) * 0.8
plt.bar(threads, times, width=widths, color="#4b0082", align="center")
plt.xticks(threads, [str(t) for t in threads])
plt.plot(threads, [times[0]/t for t in threads], color ='g', linestyle='--')
plt.suptitle("Total Times for Floyd-Warshall Tiled", size = 12)
plt.title(f"Grid Size = 4096, Block Size = 32", fontstyle = 'oblique', size = 10)
plt.xlabel("Number of threads")
plt.ylabel("Time(secs)")
plt.grid('y')
plt.savefig(f"tiled.png")
plt.clf()