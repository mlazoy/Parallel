import os
import matplotlib.pyplot as plt
import numpy as np

#replace with the actual path
folder_path = "../"
file_name = "run_conc_ll.out"
output_dir = "./"

total_path = os.path.join(folder_path, file_name)

with open(total_path, "r") as file:
    data = file.read()

lsize = 1024
current_running = 'serial'
nthreads = 1
workload = '100/0/0'
res_1024 = {}
res_8192 = {}
for line in data.splitlines():
    words = line.split()
    if len(words) == 0:
        continue
    #set lsize 
    if words[0].split('=')[0] == 'LSIZE':
        lsize = int(words[0].split('=')[1])
    #get and save the result 
    if words[0] == 'Nthreads:':
        #only need if we didn't run them in ascending order
        nthreads = int(words[1])
        workload = words[5]
        throughput = float(words[-1])
        if lsize == 1024:
            if current_running not in res_1024.keys():
                res_1024[current_running] = {}
            if workload not in res_1024[current_running].keys():
                res_1024[current_running][workload] = []
            res_1024[current_running][workload].append(throughput)
        elif lsize == 8192:
            if current_running not in res_8192.keys():
                res_8192[current_running] = {}
            if workload not in res_8192[current_running].keys():
                res_8192[current_running][workload] = []
            res_8192[current_running][workload].append(throughput)
    #save the current runner for the next result
    if len(words) == 1 and len(line.split('=')) == 1:
        current_running=words[0]

nthreads = [1, 2, 4, 8, 16, 32, 64, 128]
colours = ['red', 'green', 'blue', 'cyan', 'orange']
workloads = ['100/0/0', '80/10/10', '20/40/40', '0/50/50']

#for a specific size plot all the workloads in a different plot
for i in range(0, len(workloads)):
    plt.figure(figsize=(12,8))
    counter = 0
    for technique in res_1024.keys():
        if technique == 'serial':
            continue
        plt.plot(nthreads, res_1024[technique][workloads[i]], linewidth=2, color=colours[counter], label=technique)
        counter += 1
    
    plt.xlabel('Number of threads')
    plt.xscale('log', base=2)
    plt.ylabel('Throughput(Kops/sec)')
    #plt.yscale('log', base=10)
    plt.title(f"Throughput for workload {workloads[i]} for lsize = 1024")
    plt.grid(True)
    plt.legend(loc='best')
    sanitized_workload = workloads[i].replace('/', '_')
    plt.savefig(f"{output_dir}/conc_ll_1024_{sanitized_workload}.png")
    plt.close()
    
    #plot the normalized perfomance as well
    plt.figure(figsize=(12,8))
    counter = 0
    for technique in res_1024.keys():
        if technique == 'serial':
            continue
        temp = np.array(res_1024[technique][workloads[i]])
        #divide by nthreads so we have kops / thread 
        temp = np.divide(temp, nthreads)
        
        plt.plot(nthreads, temp, linewidth=2, color=colours[counter], label=technique)
        counter += 1
    #add serial for comparison
    serial_res = res_1024['serial'][workloads[i]][0]
    plt.axhline(y=serial_res, color='black', linestyle='--', linewidth=2, label='Serial best case')
    
    plt.xlabel('Number of threads')
    plt.xscale('log', base=2)
    plt.ylabel('Throughput(Kops/sec) per thread')
    #plt.yscale('log', base=10)
    plt.title(f"Throughput for workload {workloads[i]} for lsize = 1024")
    plt.grid(True)
    plt.legend(loc='best')
    sanitized_workload = workloads[i].replace('/', '_')
    plt.savefig(f"{output_dir}/conc_ll_norm_1024_{sanitized_workload}.png")
    plt.close()

#do for 8192 as well  
for i in range(0, len(workloads)):
    plt.figure(figsize=(12,8))
    counter = 0
    for technique in res_8192.keys():
        if technique == 'serial':
            continue
        plt.plot(nthreads, res_8192[technique][workloads[i]], linewidth=2, color=colours[counter], label=technique)
        counter += 1
    
    plt.xlabel('Number of threads')
    plt.xscale('log', base=2)
    plt.ylabel('Throughput(Kops/sec)')
    #plt.yscale('log', base=10)
    plt.title(f"Throughput for workload {workloads[i]} for lsize = 8192")
    plt.grid(True)
    plt.legend(loc='best')
    sanitized_workload = workloads[i].replace('/', '_')
    plt.savefig(f"{output_dir}/conc_ll_8192_{sanitized_workload}.png")
    plt.close()
    
    #plot the normalized perfomance as well
    plt.figure(figsize=(12,8))
    counter = 0
    for technique in res_8192.keys():
        if technique == 'serial':
            continue
        temp = np.array(res_8192[technique][workloads[i]])
        #divide by nthreads so we have kops / thread 
        temp = np.divide(temp, nthreads)
        
        plt.plot(nthreads, temp, linewidth=2, color=colours[counter], label=technique)
        counter += 1
    #add serial for comparison
    serial_res = res_8192['serial'][workloads[i]][0]
    plt.axhline(y=serial_res, color='black', linestyle='--', linewidth=2, label='Serial best case')
    
    plt.xlabel('Number of threads')
    plt.xscale('log', base=2)
    plt.ylabel('Throughput(Kops/sec) per thread')
    #plt.yscale('log', base=10)
    plt.title(f"Throughput for workload {workloads[i]} for lsize = 8192")
    plt.grid(True)
    plt.legend(loc='best')
    sanitized_workload = workloads[i].replace('/', '_')
    plt.savefig(f"{output_dir}/conc_ll_norm_8192_{sanitized_workload}.png")
    plt.close()