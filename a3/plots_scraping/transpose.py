import numpy as np
import matplotlib.pyplot as plt

#replace with the actual path
file_name = "../results/run_kmeans_1.out"

with open(file_name, "r") as file:
    data_naive = file.read()
    
file_name = "../results/run_kmeans_2.out"
with open(file_name, "r") as file:
    data_transpose = file.read()
    
t_alloc_naive = {}
t_alloc_gpu_naive = {}
t_get_gpu_naive = {}
t_run_naive = {}
t_loop_avg_naive = {}
t_cpu_avg_naive = {}
t_gpu_avg_naive = {}
t_transfers_avg_naive = {}
t_alloc_seq_naive = 0.0
t_run_seq_naive = 0.0
t_loop_avg_seq_naive = 0.0

runtype = "Sequential"
coordsSize = 32
blocksize = 32
counter = 0
measured_time = 0.0
for line in data_naive.splitlines():
    words = line.split()
    if len(words) > 10 and words[7] == "numCoords":
        coordsSize = int(words[9])
    if len(words) >= 15:
        blocksize = int(words[15])
    if len(words) > 0:
        if words[-1].split('-')[0] == "Kmeans":
            runtype = words[0].split('-')[-1]
        if words[-1] == "ms" and len(words) >= 3 and runtype == "Naive":
            #words[-2] is the measured time
            measured_time = float(words[-2])
            if words[-3] == "t_alloc:": t_alloc_naive[blocksize] = measured_time
            elif words[-3] == "t_alloc_gpu:" : t_alloc_gpu_naive[blocksize] = measured_time
            elif words[-3] == "t_get_gpu:" : t_get_gpu_naive[blocksize] = measured_time
            elif words[-4] == "total": t_run_naive[blocksize] = measured_time
            elif words[-4] == "t_loop_avg": t_loop_avg_naive[blocksize] = measured_time
            elif words[-4] == "t_cpu_avg": t_cpu_avg_naive[blocksize] = measured_time
            elif words[-4] == "t_gpu_avg": t_gpu_avg_naive[blocksize] = measured_time
            elif words[-4] == "t_transfers_avg": t_transfers_avg_naive[blocksize] = measured_time
        elif words[-1] == "ms" and len(words) >= 3 and runtype == "Sequential":
            measured_time = float(words[-2])
            if words[-3] == "t_alloc:": t_alloc_seq_naive = measured_time
            elif words[-4] == "total": t_run_seq_naive = measured_time
            elif words[-4] == "t_loop_avg": t_loop_avg_seq_naive = measured_time
    counter += 1
    
t_seq_total_naive = t_alloc_seq_naive + t_run_seq_naive
t_total_naive = {}
for key in t_alloc_naive:
    t_total_naive[key] = t_alloc_naive[key] + t_alloc_gpu_naive[key] + t_get_gpu_naive[key] + t_run_naive[key]

t_alloc_transpose = {}
t_alloc_gpu_transpose = {}
t_get_gpu_transpose = {}
t_run_transpose = {}
t_loop_avg_transpose = {}
t_cpu_avg_transpose = {}
t_gpu_avg_transpose = {}
t_transfers_avg_transpose = {}
t_alloc_seq_transpose = 0.0
t_run_seq_transpose = 0.0
t_loop_avg_seq_transpose = 0.0

runtype = "Sequential"
coordsSize = 32
blocksize = 32
counter = 0
measured_time = 0.0
for line in data_transpose.splitlines():
    words = line.split()
    if len(words) > 10 and words[7] == "numCoords":
        coordsSize = int(words[9])
    if len(words) >= 15:
        blocksize = int(words[15])
    if len(words) > 0:
        if words[-1].split('-')[0] == "Kmeans":
            runtype = words[0].split('-')[-1]
        if words[-1] == "ms" and len(words) >= 3 and runtype == "Transpose":
            #words[-2] is the measured time
            measured_time = float(words[-2])
            if words[-3] == "t_alloc:": t_alloc_transpose[blocksize] = measured_time
            elif words[-3] == "t_alloc_gpu:": t_alloc_gpu_transpose[blocksize] = measured_time
            elif words[-3] == "t_get_gpu:": t_get_gpu_transpose[blocksize] = measured_time
            elif words[-4] == "total": t_run_transpose[blocksize] = measured_time
            elif words[-4] == "t_loop_avg": t_loop_avg_transpose[blocksize] = measured_time
            elif words[-4] == "t_cpu_avg": t_cpu_avg_transpose[blocksize] = measured_time
            elif words[-4] == "t_gpu_avg": t_gpu_avg_transpose[blocksize] = measured_time
            elif words[-4] == "t_transfers_avg": t_transfers_avg_transpose[blocksize] = measured_time
        elif words[-1] == "ms" and len(words) >= 3 and runtype == "Sequential":
            measured_time = float(words[-2])
            if words[-3] == "t_alloc:": t_alloc_seq_transpose = measured_time
            elif words[-4] == "total": t_run_seq_transpose = measured_time
            elif words[-4] == "t_loop_avg": t_loop_avg_seq_transpose = measured_time
    counter += 1

t_seq_total_tranpose = t_alloc_seq_transpose + t_run_seq_transpose
t_total_transpose = {}
for key in t_alloc_transpose:
    t_total_transpose[key] = t_alloc_transpose[key] + t_alloc_gpu_transpose[key] + t_get_gpu_transpose[key] + t_run_transpose[key]
    
#Speedup
plt.figure(figsize=(10, 6))
plt.gca().set_facecolor("#e6e6fa")
plt.plot(list(t_total_naive.keys()), [t_seq_total_naive/t_total_naive[key] for key in t_total_naive], label="Naive", marker='o')
plt.plot(list(t_total_transpose.keys()), [t_seq_total_tranpose/t_total_transpose[key] for key in t_total_transpose], label="Transpose", marker='o', color='#2CA02C')
plt.legend()
plt.xlabel("Blocksize")
plt.ylabel("Speedup")
plt.xscale('log', base=2)
plt.title("Speedup Naive vs Transpose for coordSize = 32")
plt.grid()
plt.savefig("transpose_naive_speedup.png")
plt.close()