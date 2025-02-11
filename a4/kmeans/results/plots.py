import re
import matplotlib.pyplot as plt
import numpy as np

def extract_times(log_file):
    total_times = []
    per_loop_times = []
    
    with open(log_file, 'r') as file:
        for line in file:
            match = re.search(r'total =\s*([\d\.]+)s\)\s*\(per loop =\s*([\d\.]+)s', line)
            if match:
                total_times.append(float(match.group(1)))
                per_loop_times.append(float(match.group(2)))
    
    return total_times, per_loop_times

def plot_execution_time(procs, mpi_times, omp_times):
    x = np.arange(len(procs))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    bar1 = ax.bar(x - width/2, mpi_times, width, label='MPI Time (s)', color="#4b0082")
    bar2 = ax.bar(x + width/2, omp_times, width, label='OpenMP Time (s)', color='salmon')

    plt.gca().set_facecolor("#e6e6fa")

    ax.set_xlabel('Number of Processes')
    ax.set_ylabel('Time (seconds)')
    ax.set_title('Execution Time Comparison (MPI vs OpenMP)')
    ax.set_xticks(x)
    ax.set_xticklabels([str(p) for p in procs])
    ax.legend()

    # Function to add labels on bars
    def add_labels(bars, axis):
        for bar in bars:
            yval = bar.get_height()
            axis.text(bar.get_x() + bar.get_width() / 2, yval, round(yval, 2), ha='center', va='bottom')

    add_labels(bar1, ax)
    add_labels(bar2, ax)

    plt.tight_layout()
    plt.savefig("execution_time_comparison.png")
    plt.savefig("execution_time_comparison.svg")
    plt.show()

def plot_speedup(procs, mpi_times, omp_times, sequential_time):
    x = np.arange(len(procs))

    # Compute speedup
    mpi_speedup = [sequential_time / t for t in mpi_times]
    omp_speedup = [sequential_time / t for t in omp_times]
    ideal_speedup = procs  # Ideal speedup (linear)

    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(x, mpi_speedup, marker='o', linestyle='-', color='b', label='MPI Speedup')
    ax.plot(x, omp_speedup, marker='s', linestyle='--', color='r', label='OpenMP Speedup')
    ax.plot(x, ideal_speedup, linestyle="dotted", color="green", label="Ideal Speedup")

    plt.gca().set_facecolor("#e6e6fa")

    ax.set_xlabel('Number of Processes')
    ax.set_ylabel('Speedup')
    ax.set_title('Speedup Comparison (MPI vs OpenMP)')
    ax.set_xticks(x)
    ax.set_xticklabels([str(p) for p in procs])
    ax.legend()

    plt.tight_layout()
    plt.yscale('log', base=2)
    plt.savefig("speedup_comparison.png")
    plt.savefig("speedup_comparison.svg")
    plt.show()

if __name__=="__main__":
    procs = [1, 2, 4, 8, 16, 32, 64]
    sequential_time = 14.5234
    mpi_total, mpi_per_loop = extract_times("allreduction.out")
    omp_total, omp_per_loop = extract_times("openmp.out")

    print(mpi_total, mpi_per_loop)
    print(omp_total, omp_per_loop)

    # Plot execution time comparison
    plot_execution_time(procs, mpi_total, omp_total)

    # Plot speedup comparison
    plot_speedup(procs, mpi_total, omp_total, sequential_time)
