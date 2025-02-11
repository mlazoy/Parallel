import re
import numpy as np 
import matplotlib.pyplot as plt 

total_times = []
computation_times = []
communication_times = []
t_serial = [float(13.187065), float(52.874210), float(118.278895)]

with open("red_black_iter.out", "r") as file:
    lines = file.readlines()

for i in range(len(lines)):
    total_time_match = re.search(r"TotalTime:\s*(\d+\.\d+)", lines[i])
    computation_time_match = re.search(r"ComputationTime:\s*(\d+\.\d+)", lines[i])
    communication_time_match = re.search(r"CommunicationTime:\s*(\d+\.\d+)", lines[i])
    
    if total_time_match:
        total_times.append(float(total_time_match.group(1)))
    if computation_time_match:
        computation_times.append(float(computation_time_match.group(1)))
    if communication_time_match:
        communication_times.append(float(communication_time_match.group(1)))

# Output the results
print("Total Times:", total_times)
print("Computation Times:", computation_times)
print("Communication Times:", communication_times)

def split_list(lst):
    size = len(lst)
    part_size = size // 3  # Determine the size of each part
    return lst[:part_size], lst[part_size:2*part_size], lst[2*part_size:]

impl1_total, impl2_total, impl3_total = split_list(total_times)
impl1_comm, impl2_comm, impl3_comm = split_list(communication_times)
impl1_comp, impl2_comp, impl3_comp = split_list(computation_times) 

impl1_total_grid1, impl1_total_grid2, impl1_total_grid3 = split_list(impl1_total)
impl2_total_grid1, impl2_total_grid2, impl2_total_grid3 = split_list(impl2_total)
impl3_total_grid1, impl3_total_grid2, impl3_total_grid3 = split_list(impl3_total)

impl1_comm_grid1, impl1_comm_grid2, impl1_comm_grid3 = split_list(impl1_comm)
impl2_comm_grid1, impl2_comm_grid2, impl2_comm_grid3 = split_list(impl2_comm)
impl3_comm_grid1, impl3_comm_grid2, impl3_comm_grid3 = split_list(impl3_comm)

impl1_comp_grid1, impl1_comp_grid2, impl1_comp_grid3 = split_list(impl1_comp)
impl2_comp_grid1, impl2_comp_grid2, impl2_comp_grid3 = split_list(impl2_comp)
impl3_comp_grid1, impl3_comp_grid2, impl3_comp_grid3 = split_list(impl3_comp)

procs = np.array([1,2,4,8,16,32,64])  
grid_config = [(2048,2048), (4096,4096), (6144,6144)]
version = ["Blocking", "Non-Blocking", "Overlapping"]
types = ["Total", "Communication", "Computation"]
colors = ['#4b0082', 'skyblue', 'salmon']

def add_labels(bars):
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            plt.text(bar.get_x() + bar.get_width()/2, height, f'{height:.2f}', 
                     ha='center', va='bottom', fontsize=10, rotation=45)

def plot_times(time_vecs, grid, type_index):
    plt.figure(figsize=(8, 8))
    plt.gca().set_facecolor("#e6e6fa")
    x = np.linspace(0, 3, 4)
    
    for i in range(0,3):
        bar = plt.bar(x + i * 0.25, time_vecs[i][3:], width=0.25, label=version[i], color=colors[i])
        add_labels(bar)
    
    plt.xlabel("# MPI processes")
    plt.ylabel(f"{types[type_index]} Time (secs)")
    plt.xticks(x,labels = [str(p) for p in procs[3:]])
    plt.title(f"{types[type_index]} Times Comparison for all 3 RedBlackSOR versions\n Grid Size = {grid_config[grid]}")
    plt.legend()
    plt.savefig(f"RB{types[type_index]}_{grid_config[grid]}.png")
    plt.show()

def plot_speedups(time_vecs, grid, type_index):
    plt.figure(figsize=(8, 8))
    plt.gca().set_facecolor("#e6e6fa") 
    x = np.linspace(0, 6, 7)
    for i in range(0,3):
        plt.plot(x, [t_serial[grid]/j for j in time_vecs[i]], marker='o', color=colors[i], label=version[i])
    
    plt.xlabel("# MPI processes")
    plt.ylabel(r"$\frac{t_{\text{serial}}}{t_{\text{mpi}}}$", fontsize=20, fontweight='bold')
    plt.xticks(x,labels = [str(p) for p in procs])
    plt.title(f"Speedup of all 3 RedBlackSOR versions\n Grid Size = {grid_config[grid]}")
    plt.legend()
    plt.grid()
    plt.savefig(f"Speedup_{grid_config[grid]}.png")
    plt.show()   

total_grid1 = [impl1_total_grid1, impl2_total_grid1, impl3_total_grid1]
total_grid2 = [impl1_total_grid2, impl2_total_grid2, impl3_total_grid2]
total_grid3 = [impl1_total_grid3, impl2_total_grid3, impl3_total_grid3]

print("Total Grid 1:", total_grid1)
print("Total Grid 2:", total_grid2)
print("Total Grid 3:", total_grid3)
#plot speedups first
plot_speedups(total_grid1,0,0)
plot_speedups(total_grid2,1,0)
plot_speedups(total_grid3,2,0)

plot_times(total_grid1, 0, 0)
plot_times(total_grid2, 1, 0)
plot_times(total_grid3, 2, 0) 

comm_grid1 = [impl1_comm_grid1, impl2_comm_grid1, impl3_comm_grid1]
comm_grid2 = [impl1_comm_grid2, impl2_comm_grid2, impl3_comm_grid2]
comm_grid3 = [impl1_comm_grid3, impl2_comm_grid3, impl3_comm_grid3]

plot_times(comm_grid1, 0, 1)  
plot_times(comm_grid2, 1, 1)  
plot_times(comm_grid3, 2, 1)  

comp_grid1 = [impl1_comp_grid1, impl2_comp_grid1, impl3_comp_grid1]
comp_grid2 = [impl1_comp_grid2, impl2_comp_grid2, impl3_comp_grid2]
comp_grid3 = [impl1_comp_grid3, impl2_comp_grid3, impl3_comp_grid3]

plot_times(comp_grid1, 0, 2)  
plot_times(comp_grid2, 1, 2)  
plot_times(comp_grid3, 2, 2)  
