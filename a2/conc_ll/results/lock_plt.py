import numpy as np
import matplotlib.pyplot as plt
import re

outfile = "./lock_kmeans.out"

total = {}
per_loop = {}

threads_regex = r"^Setting OMP_NUM_THREADS=(\d+)"
lock_regex = r"^Running ./kmeans_omp_(\w+)"
timing_regex = r"nloops =\s+\d+\s+\(total =\s+([\d.]+)s\)\s+\(per loop =\s+([\d.]+)s\)"

num_threads = 0
lock = None

with open(outfile, 'r') as f:
    lines = f.readlines()
    for line in lines:
        # Match and extract the number of threads
        threads_match = re.match(threads_regex, line)
        if threads_match:
            num_threads = int(threads_match.group(1))

        lock_match = re.match(lock_regex, line)
        if lock_match:
            lock = lock_match.group(1)
            if lock not in total:
                total[lock] = {}
                per_loop[lock] = {}

        timing_match = re.search(timing_regex, line)
        if timing_match:
            total_time = float(timing_match.group(1))
            per_loop_time = float(timing_match.group(2))
            
            total[lock][num_threads] = total_time
            per_loop[lock][num_threads] = per_loop_time


print("Total Times:", total)
print("Per Loop Times:", per_loop)

color_palette = [
    "#1f77b4",  # Blue
    "#2ca02c",  # Green
    "#9467bd",  # Purple
    "#17becf",  # Cyan
    "#8c564b",  # Muted Purple
    "#7f7f7f",  # Grayish Blue
    "#bcbd22"   # Olive Green
]

threads = [1,2,4,8,16,32,64]

plt.figure(figsize=(10, 7))
plt.gca().set_facecolor("#e6e6fa")  
plt.xscale('log')               
for idx, (lock, times) in enumerate(total.items()):
    y_values = [times.get(t, None) for t in threads]
    plt.plot(
        threads, y_values, marker='o', color=color_palette[idx % len(color_palette)],
        label=lock, linewidth=2)
plt.xticks(threads, [str(t) for t in threads])
plt.title("Configuration = {32, 16, 32, 10}", size=12)
plt.suptitle("Locking Mechanism vs Time", fontstyle='oblique', size=14)
plt.xlabel("Number of Threads", fontsize=12)
plt.ylabel("Total Time (secs)", fontsize=12)
plt.grid(which='major', axis='y', linestyle='--', linewidth=0.7)

plt.legend(title="Lock Type", loc='upper left', fontsize=10)

plt.savefig("locks_total.png", dpi=300)


plt.figure(figsize=(10, 7))
plt.gca().set_facecolor("#e6e6fa")  
plt.xscale('log')               
for idx, (lock, times) in enumerate(total.items()):
    y_values = [times.get(t, None) for t in threads]
    plt.plot(
        threads, y_values, marker='o', color=color_palette[idx % len(color_palette)],
        label=lock, linewidth=2)
plt.xticks(threads, [str(t) for t in threads])
plt.title("Configuration = {32, 16, 32, 10}", size=12)
plt.suptitle("Locking Mechanism vs Time", fontstyle='oblique', size=14)
plt.xlabel("Number of Threads", fontsize=12)
plt.ylabel("Per-Loop Time (secs)", fontsize=12)
plt.grid(which='major', axis='y', linestyle='--', linewidth=0.7)

plt.legend(title="Lock Type", loc='upper left', fontsize=10)

plt.savefig("locks_perloop.png", dpi=300)
