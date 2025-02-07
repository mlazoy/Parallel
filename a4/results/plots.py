import re
import matplotlib.pyplot as plt
import numpy as np

def extract_times(log_file):
    total_times = []
    per_loop_times = []
    
    with open(log_file, 'r') as file:
        for line in file:
            match =  re.search(r'total =\s*([\d\.]+)s\)\s*\(per loop =\s*([\d\.]+)s', line)
            if match :
                total_times.append(float(match.group(1)))
                per_loop_times.append(float(match.group(2)))
    
    return total_times, per_loop_times


def plot_times(procs, total_times, per_loop_times):
    x = np.arange(len(procs))
    width = 0.35
    seq_time = total_times[0] if total_times else 1

    fig, ax = plt.subplots(figsize=(10, 6))
    bar1 = ax.bar(x - width/2, total_times, width, label='Total Time (s)', color="#4b0082")
    bar2 = ax.bar(x + width/2, per_loop_times, width, label='Per Loop Time (s)', color='salmon')
    ax.plot(x, [seq_time/t for t in procs], color='g', linestyle='--', label='Ideal Speedup')

    plt.gca().set_facecolor("#e6e6fa")
    #ax.set_xscale('log', base=2)

    ax.set_xlabel('Number of Processes')
    ax.set_ylabel('Time (seconds)')
    ax.set_title('Execution Time vs. Number of Processes')
    ax.set_xticks(x)
    ax.set_xticklabels([str(p) for p in procs])
    ax.legend()

    def add_labels(bars):
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, yval, round(yval, 2), ha='center', va='bottom')
    
    add_labels(bar1)
    add_labels(bar2)

    plt.tight_layout()
    plt.savefig("allreduce.svg")
    plt.savefig("allreduce.png")
    plt.show()

if __name__=="__main__":
    procs = [1,2,4,8,16,32,64]
    total, per_loop = extract_times("allreduction.out")
    print(total, per_loop)
    plot_times(procs, total, per_loop)
    
