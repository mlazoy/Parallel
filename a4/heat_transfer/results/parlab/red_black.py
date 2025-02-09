import re
import matplotlib.pyplot as plt
import numpy as np

# Define regex patterns
grid_pattern = re.compile(r"Grid = \((\d+),(\d+)\)")
implementation_pattern = re.compile(r"RedBlack SOR with (.+):")
total_time_pattern = re.compile(r"TotalTime: ([\d.]+)")
computation_time_pattern = re.compile(r"ComputationTime: ([\d.]+)")
communication_time_pattern = re.compile(r"CommunicationTime: ([\d.]+)")

# Read file content
with open("mpi_red_black.out", "r") as file:  # Change filename if needed
    lines = file.readlines()

# Data structure to store results
results = {}

# Variables to track parsing state
current_grid = None
current_implementation = None

# Process lines
for line in lines:
    line = line.strip()

    # Check for a grid
    grid_match = grid_pattern.search(line)
    if grid_match:
        current_grid = (int(grid_match.group(1)), int(grid_match.group(2)))
        results[current_grid] = {}

    # Check for implementation type
    impl_match = implementation_pattern.search(line)
    if impl_match:
        current_implementation = impl_match.group(1)
        results[current_grid][current_implementation] = {}

    # Extract times
    total_match = total_time_pattern.search(line)
    computation_match = computation_time_pattern.search(line)
    communication_match = communication_time_pattern.search(line)

    if total_match:
        results[current_grid][current_implementation]["total"] = float(total_match.group(1))
    if computation_match:
        results[current_grid][current_implementation]["comp"] = float(computation_match.group(1))
    if communication_match:
        results[current_grid][current_implementation]["comm"] = float(communication_match.group(1))

# Print extracted data (check if it's parsed correctly)
for grid, impls in results.items():
    print(f"\nGrid: {grid}")
    for impl, times in impls.items():
        print(f"  {impl}:")
        print(f"    TotalTime: {times['total']}")
        print(f"    ComputationTime: {times['comp']}")
        print(f"    CommunicationTime: {times['comm']}")

# Set up for plotting
implementations = ["blocking communication", "Non-Blocking communication", "Non-blocking communication and Overlapping"]
colors = ['#4b0082', 'skyblue', 'salmon']

# Ensure the grids are sorted for plotting
sorted_grids = sorted(results.keys())

# Function to add labels on top of bars
def add_labels(bars):
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            plt.text(bar.get_x() + bar.get_width()/2, height, f'{height:.2f}', 
                     ha='center', va='bottom', fontsize=10)

# Plot 1: Total Times
plt.figure(figsize=(10, 5))
plt.gca().set_facecolor("#e6e6fa")
x_labels = [f"{x[0]}x{x[1]}" for x in sorted_grids]
x = np.arange(len(sorted_grids))  # Grid positions

for i, impl in enumerate(implementations):
    total_times = [results[grid].get(impl, {}).get("total", 0) for grid in sorted_grids]
    bars = plt.bar(x + i * 0.25, total_times, width=0.25, label=impl, color=colors[i])
    add_labels(bars)

plt.xticks(x + 0.25, x_labels)
plt.xlabel("Grid Size")
plt.ylabel("Total Time (s)")
plt.title("Total Execution Time for all 3 RedBlackSOR Implementations")
plt.legend()
plt.savefig("red_black_toatl.png")
plt.show()

# Plot 2: Communication Times
plt.figure(figsize=(10, 5))
plt.gca().set_facecolor("#e6e6fa")

for i, impl in enumerate(implementations):
    comm_times = [results[grid].get(impl, {}).get("comm", 0) for grid in sorted_grids]
    bars = plt.bar(x + i * 0.25, comm_times, width=0.25, label=impl, color=colors[i])
    add_labels(bars)

plt.xticks(x + 0.25, x_labels)
plt.xlabel("Grid Size")
plt.ylabel("Communication Time (s)")
plt.title("Communication Time for all 3 RedBlackSOR Implementations")
plt.legend()
plt.savefig("red_black_comm.png")
plt.show()
