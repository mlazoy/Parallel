import matplotlib.pyplot as plt
import numpy as np

#replace with the actual path
file_name = "../results/run_kmeans_1.out"

with open(file_name, "r") as file:
    data = file.read()

t_alloc = {}
t_alloc_gpu = {}
t_get_gpu = {}
t_run = {}
t_loop_avg = {}
t_cpu_avg = {}
t_gpu_avg = {}
t_transfers_avg = {}
t_alloc_seq = 0.0
t_run_seq = 0.0
t_loop_avg_seq = 0.0

runtype = "Sequential"
coordsSize = 32
blocksize = 32
counter = 0
measured_time = 0.0
for line in data.splitlines():
    words = line.split()
    if len(words) > 10 and words[7] == "numCoords":
        coordsSize = int(words[9])
    if len(words) >= 15:
        blocksize = int(words[15])
    if len(words) > 0:
        if words[-1].endswith("Kmeans--------------|"):
            runtype = words[0].split('-')[-1]
        if words[-1] == "ms" and len(words) >= 3 and runtype == "Naive":
            #words[-2] is the measured time
            measured_time = float(words[-2])
            if words[-3] == "t_alloc:": t_alloc[blocksize] = measured_time
            elif words[-3] == "t_alloc_gpu:" : t_alloc_gpu[blocksize] = measured_time
            elif words[-3] == "t_get_gpu:" : t_get_gpu[blocksize] = measured_time
            elif words[-4] == "total": t_run[blocksize] = measured_time
            elif words[-4] == "t_loop_avg": t_loop_avg[blocksize] = measured_time
            elif words[-4] == "t_cpu_avg": t_cpu_avg[blocksize] = measured_time
            elif words[-4] == "t_gpu_avg": t_gpu_avg[blocksize] = measured_time
            elif words[-4] == "t_transfers_avg": t_transfers_avg[blocksize] = measured_time
        elif words[-1] == "ms" and len(words) >= 3 and runtype == "Sequential":
            measured_time = float(words[-2])
            if words[-3] == "t_alloc:": t_alloc_seq = measured_time
            elif words[-4] == "total": t_run_seq = measured_time
            elif words[-4] == "t_loop_avg": t_loop_avg_seq = measured_time
    counter += 1

t_seq_total = t_alloc_seq + t_run_seq
t_total = {}
for key in t_alloc:
    t_total[key] = t_alloc[key] + t_alloc_gpu[key] + t_get_gpu[key] + t_run[key]

#Speedup
plt.figure(figsize=(10, 6))
plt.gca().set_facecolor("#e6e6fa")
plt.plot(t_total.keys(), [t_seq_total/t_total[key] for key in t_total.keys()], label="Speedup", marker='o')
plt.xlabel("Blocksize")
plt.ylabel("Speedup")
plt.xscale('log', base=2)
plt.title("Speedup vs Blocksize Naive Version for coordsSize = 32")
plt.legend()
plt.grid()
plt.savefig("naive_speedup.png")
plt.close()

#Execution Time
x_labels = ["Sequential"] + [str(blocksize) for blocksize in t_total.keys()]
y_values = [t_seq_total] + list(t_total.values())
plt.figure(figsize=(10, 6))
plt.gca().set_facecolor("#e6e6fa")
plt.bar(x_labels, y_values, color='#59118E', edgecolor='black')
plt.xlabel("Execution Type and Block Sizes")
plt.ylabel("Execution Time (ms)")
plt.title("Execution Time: Sequential vs Block Sizes (Naive Version) for coordsSize = 32")
plt.grid(axis='y', linestyle='--', linewidth=0.5)
plt.savefig("naive_exec_time.png")
plt.close()

#Stacked barplots
x_labels = [str(blocksize) for blocksize in t_total.keys()]
t_run_values = [t_gpu_avg[blocksize] * 10 for blocksize in t_total.keys()]
t_transfers_values = [t_transfers_avg[blocksize] * 10 + t_get_gpu[blocksize] for blocksize in t_total.keys()]
t_cpu_values = [t_cpu_avg[blocksize] * 10 for blocksize in t_total.keys()]
plt.figure(figsize=(10, 6))
plt.gca().set_facecolor("#e6e6fa")
plt.bar(x_labels, t_run_values, label="GPU execution time", color='skyblue', edgecolor='black')
plt.bar(x_labels, t_transfers_values, bottom=t_run_values, label="Total transfer time", color='orange', edgecolor='black')
plt.bar(x_labels, t_cpu_values, bottom=[t_run_values[i] + t_transfers_values[i] for i in range(len(t_run_values))],
        label="CPU execution time", color='green', edgecolor='black')
plt.xlabel("Block Sizes")
plt.ylabel("Execution Time (ms)")
plt.title("CPU, Transfer, GPU average time per loop for coordsSize = 32")
plt.legend()
plt.grid(axis='y', linestyle='--', linewidth=0.5)
plt.savefig("naive_stacked_execution_time_blocksizes.png")
plt.close()