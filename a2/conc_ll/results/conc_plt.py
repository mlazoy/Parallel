import re
from collections import defaultdict
import matplotlib.pyplot as plt 
import numpy as np

outfile1 = "./conc_ll_1024.out"
outfile2 = "./conc_ll_8196.out"
size1 = 1024
size2 = 8196

throughputs = defaultdict(dict)

outfile=outfile2
size=size2

mech_regex = r"^(serial|coarse-grain|fine-grain|optimistic|lazy|non-blocking)$"
threads_regex = r"Nthreads:\s+(\d+)"
workload_regex = r"Workload:\s+(\d+/\d+/\d+)"
throughput_regex = r"Throughput\(Kops/sec\):\s+([\d.]+)"

locking_mech = None
workload = None

with open(outfile, 'r') as f:
    lines = f.readlines()
    for line in lines:
        mech_match = re.match(mech_regex, line)
        if mech_match:
            locking_mech = mech_match.group(1)

        workload_match = re.search(workload_regex, line)
        if workload_match:
            workload = workload_match.group(1)

        threads_match = re.search(threads_regex, line)
        throughput_match = re.search(throughput_regex, line)
        if threads_match and throughput_match:
            threads = int(threads_match.group(1))
            throughput = float(throughput_match.group(1))
            
            if locking_mech and workload:
                throughputs[(locking_mech, workload)][threads] = throughput

for key, value in throughputs.items():
    mech, workload = key
    print(f"Mechanism: {mech}, Workload: {workload}")
    for threads, throughput in sorted(value.items()):
        print(f"  Threads: {threads}, Throughput: {throughput}")


mechanisms = sorted(set(pair[0] for pair in throughputs.keys()))
workloads = sorted(set(pair[1] for pair in throughputs.keys()))
threads = [1, 2, 4, 8, 16, 32, 64, 128]

#Line PLot settings 
color_palette = ["#1f77b4", "#2ca02c", "#9467bd", "#17becf", "#bcbd22", "#8c564b"]

for workload in workloads:
    plt.figure(figsize=(10, 7))
    
    for idx, mech in enumerate(mechanisms):
        throughput_values = [throughputs.get((mech, workload), {}).get(n, 0) for n in threads]
        plt.plot(
            threads, throughput_values,
            marker="o",  # Add markers for clarity
            color=color_palette[idx % len(color_palette)],  # Cycle colors
            label=mech
        )
    
    plt.gca().set_facecolor("#e6e6fa")
    plt.xscale("log")  # Log scale for thread counts
    plt.xticks(threads, [str(t) for t in threads])
    plt.xlabel("Number of Threads", fontsize=12)
    plt.ylabel("Throughput (Kops/sec)", fontsize=12)
    plt.title(f"Throughput vs Threads for Workload Pattern:\n Search/Insert/Delete: {workload}, Size={size}", fontsize=14)
    plt.grid(which="major", axis="y", linestyle="--", alpha=0.7)
    plt.legend(title="Locking Mechanism", fontsize=10)
    
    plt.tight_layout()
    plt.savefig(f"line_plt{workload.replace('/', '_')}_{size}.png", dpi=300)


# Bar Plot settings
bar_width = 0.2
x_indices = np.arange(len(mechanisms))

serial = [mech for mech in mechanisms if mech == "serial"]
non_serial_mechanisms = [mech for mech in mechanisms if mech != "serial"]


color_palette = ["#1f77b4", "#2ca02c", "#9467bd", "#17becf"]  # Blue, Green, Purple, Cyan
serial_palette = ["#ff9999", "#ff6666", "#ff3333", "#cc0000"]  # Shades of red for serial

for n in threads:
    plt.figure(figsize=(12, 8))

    # Plot serial bars first
    if serial:
        for idx, workload in enumerate(workloads):
            serial_throughput = throughputs.get((serial[0], workload), {}).get(1, 0)  # Serial only at n=1
            plt.bar(
                x_indices[0] + idx * bar_width,  
                serial_throughput,
                width=bar_width,
                color=serial_palette[idx % len(serial_palette)],
                label=f"Serial: {workload}" 
            )

    throughput_data = {
        mech: [throughputs.get((mech, workload), {}).get(n, 0) for workload in workloads]
        for mech in non_serial_mechanisms
    }

    for idx, workload in enumerate(workloads):
        workload_throughput = [throughput_data[mech][idx] for mech in non_serial_mechanisms]
        workload_norm = np.divide(workload_throughput, n)
        plt.bar(
            x_indices[1:] + idx * bar_width,  # Offset bars for non-serial mechanisms
            workload_norm,
            width=bar_width,
            color=color_palette[idx % len(color_palette)],
            label=f"Search/Insert/Delete {workload}" 
        )

    # Formatting the plot
    plt.gca().set_facecolor("#e6e6fa")
    plt.xticks(
        x_indices + bar_width * (len(workloads) - 1) / 2, 
        ["Serial"] + non_serial_mechanisms,  # Add "Serial" as the first x-axis label
        rotation=45
    )
    plt.xlabel("Locking Mechanism", fontsize=12)
    plt.ylabel("(Kops/sec) per thread", fontsize=12)
    plt.title(f"Throughput Per Thread vs Locking Mechanism\n (Size={size}, Threads={n})", fontsize=14)
    plt.legend(title="Workload", fontsize=10)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    
    # Save the figure
    plt.tight_layout()
    plt.savefig(f"conc_{size}_{n}.png", dpi=300)