__global__ static
void find_nearest_cluster(int numCoords,
                          int numObjs,
                          int numClusters,
                          double *deviceobjects,           //  [numCoords][numObjs]
/*                          
                          TODO: If you choose to do (some of) the new centroid calculation here, you will need some extra parameters here (from "update_centroids").
*/
                          int *devicenewClusterSize,           //  [numClusters]
                          double *devicenewClusters,    //  [numCoords][numClusters]
                          double *deviceClusters,    //  [numCoords][numClusters]
                          int *deviceMembership,          //  [numObjs]
                          double *devdelta) {
  extern __shared__ double shmemClusters[];

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
      /* TODO: Maybe something is missing here... is this write safe? */
      atomicAdd(devdelta, 1.0);
    }

    /* assign the deviceMembership to object objectId */
    deviceMembership[tid] = index;

    /* TODO: additional steps for calculating new centroids in GPU? */
    //we chose to update the size and do the add here
    //the division and the actual new Coords will be in update controids
    atomicAdd(&devicenewClusterSize[index], 1);
    for (i = 0; i < numCoords; i++) 
      atomicAdd(&devicenewClusters[i * numClusters + index], deviceobjects[i * numObjs + tid]);
  }
}

__global__ static
void update_centroids(int numCoords,
                      int numClusters,
                      int *devicenewClusterSize,           //  [numClusters]
                      double *devicenewClusters,    //  [numCoords][numClusters]
                      double *deviceClusters)    //  [numCoords][numClusters])
{

  /* TODO: additional steps for calculating new centroids in GPU? */
  int tid = get_tid();

  if (tid < numCoords * numClusters) {
    /*run through all the elements, just divide by the size of the clusters
    indexing of the 1d colummn based devicenewClusters is i*numClusters + j
    so the index of the current cluster is the j, and i the Coords 
    so the index of the current clusters is (i*numClusters + j) % numClusters
    here the tid runs all the array increasingly so it is i*numClusters + j
    */
    deviceClusters[tid] = devicenewClusters[tid] / devicenewClusterSize[tid % numClusters];
    //reset devicenewClusters after updating deviceClusters
    devicenewClusters[tid] = 0.0;
  }
  __syncthreads();
  //reset devicenewClusterSize as well
  if (tid < numClusters) {
    devicenewClusterSize[tid] = 0;
  }

}

