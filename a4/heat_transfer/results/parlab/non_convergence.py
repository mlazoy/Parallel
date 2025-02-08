import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

filename = "outrunjob_serial.txt"
with open(filename, "r") as file:
    data = file.read()
    
methods = ["Jacobi", "GaussSeidelSOR", "RedBlackSOR"]
sizes = [2048, 4096, 6144]
serial_time = {size: {} for size in sizes}


for line in data.splitlines():
    words = line.split()
    if len(words) < 3:
        continue
    method = words[0]
    size = int(words[2])
    if size == 512:
        continue
    time = float(words[8])
    serial_time[size][method] = time
    
processors = [1, 2, 4, 8, 16, 32, 64]
parallel_time = {size: {} for size in sizes}
comp_time = {size: {} for size in sizes}

filename = "outrunjob_no_conv.txt"
with open(filename, "r") as file:
    data = file.read()

for line in data.splitlines():
    words = line.split()
    if len(words) < 15:
        continue
    method = words[0]
    #method name fixing
    if method == "Gauss":
        method = "GaussSeidelSOR"
    elif method == "RedBlack":
        method = "RedBlackSOR"
        
    #size fixing
    if method == "Jacobi":
        size = int(words[2])
    elif method == "GaussSeidelSOR":
        size = int(words[4])
    elif method == "RedBlackSOR":
        size = int(words[3])
    time = float(words[-3])
    if method in parallel_time[size]:
        parallel_time[size][method].append(time)
    else:
        parallel_time[size][method] = [time]
    time = float(words[-5])
    if method == "RedBlackSOR":
        time = float(words[-7])
    if method in comp_time[size]:
        comp_time[size][method].append(time)
    else:
        comp_time[size][method] = [time]
        
for size in sizes:
    colours = ['#000080', '#2CA02C', '#8B0000']
    plt.figure(figsize=(10, 6))
    plt.gca().set_facecolor("#e6e6fa")
    for i, method in enumerate(methods):
        plt.plot(processors, [serial_time[size][method] / time for time in parallel_time[size][method]], marker = 'o',label=method, color=colours[i])
    plt.xlabel("Number of processors")
    plt.ylabel("Speedup")
    plt.title(f"Speedup for array size {size} for the different methods")
    plt.legend()
    plt.xscale('log', base=2)
    plt.yscale('log', base=2)
    plt.grid()
    plt.savefig(f"speedup_{size}.png")
    plt.close()
    
#barplots for each array size for times for 8,16,32,64 processors only
#1 bar for each combination of array size and processors
selected_processors = [8, 16, 32, 64]

transparency = 0.2  # 80% transparent

transparent_colours = [mcolors.to_rgba(c, transparency) for c in colours]

# Create a wider figure
plt.figure(figsize=(12, 8))
plt.gca().set_facecolor("#e6e6fa")

# Define positions for groups
num_sizes = len(sizes)
num_processors = len(selected_processors)
group_width = 0.6  # Space for each (size, processor) group
bar_width = group_width / len(methods)  # Space for each method within a group

# X-axis positions for groups
group_positions = np.arange(num_sizes * num_processors) * 1.5  # Spacing groups apart

# Plot stacked bars
for i, size in enumerate(sizes):
    for j, proc in enumerate(selected_processors):
        group_index = i * num_processors + j  # Position in groups
        for k, method in enumerate(methods):
            x_pos = group_positions[group_index] + (k - 1) * bar_width  # Center methods inside group
            
            total_time = parallel_time[size][method][selected_processors.index(proc)]
            computation_time = comp_time[size][method][selected_processors.index(proc)]
            communication_time = total_time - computation_time  # Remaining part

            # Bottom part (computation)
            plt.bar(x_pos, computation_time, color=colours[k], width=bar_width, label=method if i == 0 and j == 0 else "")

            # Top part (communication)
            plt.bar(x_pos, communication_time, bottom=computation_time, color=transparent_colours[k], width=bar_width, alpha=0.5)

# Adjust x-ticks
plt.xticks(group_positions, 
           [f"{size}, {proc}P" for size in sizes for proc in selected_processors], 
           rotation=45, ha="right")

plt.xlabel("Array size, Number of Processors")
plt.ylabel("Time (s)")
plt.title("Execution Time Breakdown for Different Array Sizes and Processor Counts")
plt.legend()
plt.grid(axis="y")

plt.savefig("execution_time_breakdown.png")
plt.close()