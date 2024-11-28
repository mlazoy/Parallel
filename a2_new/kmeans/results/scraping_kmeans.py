import os
import matplotlib.pyplot as plt

#replace with the actual path
folder_path = "../"
file_name = "run_kmeans.err"

total_path = os.path.join(folder_path, file_name)

with open(total_path, "r") as file:
    data = file.read()

omp_num_threads = 1
current_running = 'array_lock'
#we need just one the two, but may we need both
results_dict= {}
results_array = {}
for line in data.splitlines():
    words = line.split()
    if len(words) == 0:
        continue
    #set the nthreads, set what is running or the exec time
    if words[0] == 'Setting':
        omp_num_threads = int(words[1].split('=')[-1])
    if words[0] == 'Running':
        temp = words[1].split('_')[2:]
        current_running = '_'.join(temp)
    if words[0] == 'nloops':
        temp_res = float(words[5][0:-2])
        if current_running not in results_dict:
            results_dict[current_running] = {}
            results_array[current_running] = []
        results_dict[current_running][omp_num_threads] = temp_res
        results_array[current_running].append(temp_res)


nthreads = [1, 2, 4, 8, 16, 32, 64]
colours = ['red', 'green', 'blue', 'cyan', 'magenta', 'gray', 'black', 'orange', 'darkGreen']

plt.figure(figsize=(12, 8))
counter = 0
for technique in results_array.keys():
    plt.plot(nthreads, results_array[technique], linewidth=2, color=colours[counter], label=technique)
    counter += 1
plt.xlabel('Number of threads')
plt.xscale('log', base=2)
plt.ylabel('Time for execution (s)')
plt.title("Perfomance of the different techniques")
plt.grid(True)
plt.legend(loc='best')
plt.savefig("kmeans_results.png")
plt.close()