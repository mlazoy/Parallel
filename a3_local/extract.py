import re 
import csv
import matplotlib.pyplot as plt

total = []
t_alloc = []
t_alloc_gpu = []
t_get_gpu = []
sequential = {}
version_times = {}

def extract_times(filename):
    with open(filename, 'r') as f:
        for line in f.readlines():
            if (len(sequential) < 2): # extract seqential first
                match = re.search(r't_alloc: ([\d\.]+) ms', line)
                if match:
                    sequential['t_alloc'] = float(match.group(1))
                else: 
                    match = re.search(r'total = ([\d\.]+) ms', line)
                    if match:
                        sequential['total'] = float(match.group(1))
                continue
            if line.startswith("nloops"):
                match = re.search(r'total = ([\d\.]+) ms', line)
                if match:
                    total.append(float(match.group(1)))
            elif line.startswith("t_alloc:"):
                match = re.search(r't_alloc: ([\d\.]+) ms', line)
                if match:
                    t_alloc.append(float(match.group(1)))
            elif line.startswith("t_alloc_gpu:"):
                match = re.search(r't_alloc_gpu: ([\d\.]+) ms', line)
                if match:
                    t_alloc_gpu.append(float(match.group(1)))
            elif line.startswith("t_get_gpu:"):
                match = re.search(r't_get_gpu: ([\d\.]+) ms', line)
                if match:
                    t_get_gpu.append(float(match.group(1)))
    

def split_versions(versions, configs):
    num_versions = len(versions) 
    num_configs = len(configs)
    for b in range(0, num_versions):
        version_times[(versions[b],'total')] = list(total[b*num_configs:b*num_configs+num_configs])
        version_times[(versions[b],'t_alloc')] = list(t_alloc[b*num_configs:b*num_configs+num_configs])
        version_times[(versions[b],'t_alloc_gpu')] = list(t_alloc_gpu[b*num_configs:b*num_configs+num_configs])
        version_times[(versions[b],'t_get_gpu')] = list(t_get_gpu[b*num_configs:b*num_configs+num_configs])

def plot_times(filename, block_sz, version):
    xlabel = list(['sequential'] + [str(b) for b in block_sz])
    ylabel = list([sequential['total']] + version_times[(version, "total")])
    plt.bar(xlabel, ylabel)
    version_name = version.split("_")[2]
    i = 0
    if (filename == "config_big.txt"):
        i = 1
        plt.title(f"Total Times for {version_name} version with CUDA\n configuration = {1024,32,64,10}")
    else :
        i = 2
        plt.title(f"Total Times for {version_name} version with CUDA\n configuration = {1024,2,64,10}")
    plt.xlabel("Block Size")
    plt.ylabel("Time (ms)")
    plt.xticks(xlabel, rotation=45)
    plt.savefig(f"{version_name}_times{i}.png")
    plt.show()

def plot_speedup(filename, block_sz, version):
    version_name = version.split("_")[2]
    xlabel = list([str(b) for b in block_sz])
    ylabel = list([sequential['total']/ i for i in version_times[(version, "total")]])
    plt.plot(xlabel, ylabel, marker='o', linewidth=1.5)
    plt.grid()
    i = 0
    if (filename == "config_big.txt"):
        i = 1
        plt.title(f"Speedup of {version_name} version with CUDA\n configuration = {1024,32,64,10}")
    else :
        i = 2
        plt.title(f"Speedup of {version_name} version with CUDA\n configuration = {1024,2,64,10}")
    plt.xlabel("Block Size")
    plt.ylabel("Sequential Time / GPU Time ")
    plt.xticks(xlabel, rotation=45)
    plt.savefig(f"{version_name}_speedup{i}.png")
    plt.show()

def plot_compare(filename, block_sz):
    xlabel = list([str(b) for b in block_sz])
    for pair_vt in version_times.keys():
        if pair_vt[1] == "total":
            plt.plot(xlabel, list(sequential["total"]/ i for i in version_times[pair_vt]), marker='o', linewidth=1.5, label = pair_vt[0])
    plt.xlabel("Block Size")
    plt.ylabel("Speedup")
    i = 0
    if (filename == "config_big.txt"):
        i = 1
        plt.title("Speedup comparison between Naive, Transpose & Shared Verison\n configuration = {1024, 32, 64, 10}")
    else :
        i = 2
        plt.title("Speedup comparison between Naive, Transpose & Shared Verison\n configuration = {1024, 2, 64, 10}")
    plt.grid()
    plt.savefig(f"comparison{i}.png")
    plt.show()

if __name__=="__main__":
    filename = "config_big.txt"
    #filename = "config_little.txt"
    csvfile = "version_times.csv"
    block_sz = [32, 48, 64, 128, 238, 512, 1024] 
    kmeans_versions = ["cuda_kmeans_naive", "cuda_kmeans_transpose", "cuda_kmeans_shared", "cuda_kmeans_all_gpu"]

    extract_times(filename)
    split_versions(kmeans_versions, block_sz)
    
    with open(csvfile, 'w', newline='') as csv_f:
        writer = csv.writer(csv_f)
        writer.writerow(["Version", "Metric", "BlockSize", "Time(ms)"])
        for pair_vt, times in version_times.items():
            for i in range (0,len(times)):
                writer.writerow([pair_vt[0], pair_vt[1], block_sz[i], times[i]])

    # plot times 
    plot_times(filename, block_sz, "cuda_kmeans_naive")
    plot_times(filename, block_sz, "cuda_kmeans_transpose")
    plot_times(filename, block_sz, "cuda_kmeans_shared")
    plot_times(filename, block_sz, "cuda_kmeans_all_gpu")
    # plot speedups
    plot_speedup(filename, block_sz, "cuda_kmeans_naive")
    plot_speedup(filename, block_sz, "cuda_kmeans_transpose")
    plot_speedup(filename, block_sz, "cuda_kmeans_shared")
    plot_speedup(filename, block_sz, "cuda_kmeans_all_gpu")
    # plot all speedups 
    plot_compare(filename, block_sz)




        

