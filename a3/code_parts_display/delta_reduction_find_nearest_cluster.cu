/*----< find_nearest_cluster() >---------------------------------------------*/
__global__ static
void find_nearest_cluster(int numCoords,
                          int numObjs,
                          int numClusters,
                          double *deviceobjects,           //  [numCoords][numObjs]
                          int *devicenewClusterSize,           //  [numClusters]
                          double *devicenewClusters,    //  [numCoords][numClusters]
                          double *deviceClusters,    //  [numCoords][numClusters]
                          int *deviceMembership,          //  [numObjs]
                          double *devdelta) {
  extern __shared__ double shmem_total[];
  double *shmemClusters = shmem_total;
  double *delta_reduce_buff = shmem_total + numClusters * numCoords;
  /* TODO: copy me from shared version... */
  int no_cluster, i;
  
  //use local_id because shared memory is per thread block
  for (no_cluster = threadIdx.x; no_cluster < numClusters; no_cluster+=blockDim.x) {
    for (i = 0; i < numCoords; i++) {
      shmemClusters[i * numClusters + no_cluster] = deviceClusters[i * numClusters + no_cluster];
    }
  }
  __syncthreads();

  /* Get the global ID of the thread. */
  int tid = get_tid();

  /* TODO: copy me from shared version... */
  if (tid < numObjs) {

    /* TODO: copy me from shared version... */
    int index;
    double dist, min_dist;

    /* find the cluster id that has min distance to object */
    index = 0;
    /* TODO: call min_dist = euclid_dist_2(...) with correct objectId/clusterId using clusters in shmem*/
    min_dist = euclid_dist_2_transpose(numCoords, numObjs, numClusters, deviceobjects, shmemClusters, tid, 0);
    for (i = 1; i < numClusters; i++) {
      /* TODO: call dist = euclid_dist_2(...) with correct objectId/clusterId using clusters in shmem*/
      dist = euclid_dist_2_transpose(numCoords, numObjs, numClusters, deviceobjects, shmemClusters, tid, i);

      /* no need square root */
      if (dist < min_dist) { /* find the min and its array index */
        min_dist = dist;
        index = i;
      }
    }

    if (deviceMembership[tid] != index) {
      delta_reduce_buff[threadIdx.x] = 1.0;
    }
    else {
      delta_reduce_buff[threadIdx.x] = 0.0;
    }

    /* assign the deviceMembership to object objectId */
    deviceMembership[tid] = index;

    /* TODO: Replacing (*devdelta)+= 1.0; with reduction:
      - each thread updates the single element of delta_reduce_buff
      corresponding to its local id (threadIdx.x) -> 1.0 if membership changes, otherwise 0.
      - Then, ensuring delta_reduce_buff is fully updated, its containts must be summed in delta_reduce_buff[0]
      either by one thread (lower perf) or with a tree-based reduction (similar to dot reduction example in slides)
      - Finally, delta_reduce_buff[0] (local value in block) must be added to devdelta (global delta value), ensuring write dependencies!
    */

    /* TODO: additional steps for calculating new centroids in GPU? */
    atomicAdd(&devicenewClusterSize[index], 1);
    for (i = 0; i < numCoords; i++) {
      atomicAdd(&devicenewClusters[i * numClusters + index], deviceobjects[i * numObjs + tid]);
    }

    __syncthreads();
    //after everyone in the block is finished do the tree update of delta
    i = blockDim.x / 2;
    while (i != 0) {
      if (threadIdx.x < i) delta_reduce_buff[threadIdx.x] += delta_reduce_buff[threadIdx.x + i];
      __syncthreads();
      i /= 2;
    }
    if (threadIdx.x == 0) atomicAdd(devdelta, delta_reduce_buff[0]);
  }
}

