import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba

#replace with the actual path
file_name = "../results/run_kmeans_1.out"
with open(file_name, "r") as file:
    data_naive = file.read()
    
file_name = "../results/run_kmeans_2.out"
with open(file_name, "r") as file:
    data_transpose = file.read()
    
file_name = "../results/run_kmeans_3.out"
with open(file_name, "r") as file:
    data_shared = file.read()

# Concatenating the data
all_data = data_naive + data_transpose + data_shared
methods = ["Naive", "Transpose", "Shared"]
t_alloc = {method: {} for method in methods}
t_alloc_gpu = {method: {} for method in methods}
t_get_gpu = {method: {} for method in methods}
t_run = {method: {} for method in methods}
t_loop_avg = {method: {} for method in methods}
t_cpu_avg = {method: {} for method in methods}
t_gpu_avg = {method: {} for method in methods}
t_transfers_avg = {method: {} for method in methods}
t_alloc_seq = {}
t_run_seq = {}
t_loop_avg_seq = {}

runtype = "Sequential"
coordsSize = 32
blocksize = 32
counter = 0
measured_time = 0.0
for line in all_data.splitlines():
    words = line.split()
    if len(words) > 10 and words[7] == "numCoords":
        coordsSize = int(words[9])
    if len(words) >= 15:
        blocksize = int(words[15])
    if len(words) > 0:
        if words[-1].split('-')[0] == "Kmeans":
            runtype = words[0].split('-')[-1]
        if words[-1] == "ms" and len(words) >= 3 and runtype == "Sequential":
            measured_time = float(words[-2])
            previous_runtype = "Naive" if counter < 50 else "Transpose" if counter < 250 else "Shared" 
            if words[-3] == "t_alloc:": t_alloc_seq[previous_runtype] = measured_time
            elif words[-4] == "total": t_run_seq[previous_runtype] = measured_time
            elif words[-4] == "t_loop_avg": t_loop_avg_seq[previous_runtype] = measured_time
        elif words[-1] == "ms" and len(words) == 3 and runtype in methods:
            #words[-2] is the measured time
            measured_time = float(words[-2])
            if words[-3] == "t_alloc:": t_alloc[runtype][blocksize] = measured_time
            elif words[-3] == "t_alloc_gpu:" : t_alloc_gpu[runtype][blocksize] = measured_time
            elif words[-3] == "t_get_gpu:" : t_get_gpu[runtype][blocksize] = measured_time
        elif words[-1] == "ms" and len(words) > 3 and runtype in methods:
            measured_time = float(words[-2])
            if words[-4] == "total": t_run[runtype][blocksize] = measured_time
            elif words[-4] == "t_loop_avg": t_loop_avg[runtype][blocksize] = measured_time
            elif words[-4] == "t_cpu_avg": t_cpu_avg[runtype][blocksize] = measured_time
            elif words[-4] == "t_gpu_avg": t_gpu_avg[runtype][blocksize] = measured_time
            elif words[-4] == "t_transfers_avg": t_transfers_avg[runtype][blocksize] = measured_time
    counter += 1

t_seq_total = {method: t_alloc_seq[method] + t_run_seq[method] for method in methods}

t_total = {method: {} for method in methods}
for method in methods:
    for key in t_alloc[method]:
        t_total[method][key] = t_alloc[method][key] + t_alloc_gpu[method][key] + t_get_gpu[method][key] + t_run[method][key]

#Speedup
plt.figure(figsize=(10, 6))
plt.gca().set_facecolor("#e6e6fa")
plt.plot(t_total["Naive"].keys(), [t_seq_total["Naive"] / t_total["Naive"][key] for key in t_total["Naive"].keys()], label="Naive", marker='o')
plt.plot(t_total["Transpose"].keys(), [t_seq_total["Transpose"] / t_total["Transpose"][key] for key in t_total["Transpose"].keys()], label="Transpose", marker='o', color='#2CA02C')
plt.plot(t_total["Shared"].keys(), [t_seq_total["Shared"] / t_total["Shared"][key] for key in t_total["Shared"].keys()], label="Shared", marker='o', color='#8B0000')
plt.legend()
plt.xlabel("Blocksize")
plt.ylabel("Speedup")
plt.xscale('log', base=2)
plt.title("Speedup of different implementations for coordsSize = 32")
plt.grid()
plt.savefig("shared_transpose_naive_speedup.png")
plt.close()



#CPU, GPU, CPU-GPU transfers per loop time comparison only because allocation takes too much
block_sizes = list(t_total["Naive"].keys())
x_labels = [str(blocksize) for blocksize in block_sizes]
n_methods = len(methods)
bar_width = 0.2

# Define base colors and create different shades
base_colors = {
    "GPU execution time": "skyblue",
    "Transfer time": "orange",
    "CPU execution time": "green"
}
shades = {method: {} for method in methods}
for i, method in enumerate(methods):
    for component, base_color in base_colors.items():
        alpha = 0.5 + 0.25 * i  # Adjust transparency to create distinct shades
        shades[method][component] = to_rgba(base_color, alpha)

plt.figure(figsize=(12, 8))
plt.gca().set_facecolor("#e6e6fa")

for i, method in enumerate(methods):
    # Compute positions for this method's bars
    method_positions = [x + i * bar_width for x in range(len(block_sizes))]

    # Extract values for the stacked components
    t_gpu_values = [t_gpu_avg[method][blocksize] for blocksize in block_sizes]
    t_transfers_values = [t_transfers_avg[method][blocksize] for blocksize in block_sizes]
    t_cpu_values = [t_cpu_avg[method][blocksize] for blocksize in block_sizes]

    # Plot stacked bars for this method
    bar_gpu = plt.bar(
        method_positions, t_gpu_values, width=bar_width,
        label=f"{method} - GPU execution time", color=shades[method]["GPU execution time"], edgecolor='black'
    )
    bar_transfers = plt.bar(
        method_positions, t_transfers_values, width=bar_width, bottom=t_gpu_values,
        label=f"{method} - Transfer time", color=shades[method]["Transfer time"], edgecolor='black'
    )
    bar_cpu = plt.bar(
        method_positions, t_cpu_values, width=bar_width,
        bottom=[t_gpu_values[j] + t_transfers_values[j] for j in range(len(t_gpu_values))],
        label=f"{method} - CPU execution time", color=shades[method]["CPU execution time"], edgecolor='black'
    )

    # Add method labels on top of the bars
    for j, (gpu, transfers, cpu) in enumerate(zip(t_gpu_values, t_transfers_values, t_cpu_values)):
        total_height = gpu + transfers + cpu
        plt.text(
            method_positions[j], total_height + 2, method, ha='center', va='bottom',
            fontsize=8, rotation=90, color='black'
        )

# Customize x-axis
plt.xlabel("Block Sizes")
plt.xticks(
    ticks=[x + (n_methods - 1) * bar_width / 2 for x in range(len(block_sizes))],
    labels=x_labels,
    rotation=45
)

# Add labels, title, legend, and grid
plt.ylabel("Execution Time (ms)")
plt.title("CPU, Transfer, GPU average time per loop comparison for coordsSize = 32")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small')  # Legend outside the plot
plt.grid(axis='y', linestyle='--', linewidth=0.5)

# Save the plot
plt.tight_layout()
plt.savefig("shared_gpu_cpu_comparison.png")
plt.close()


