__host__ __device__ inline static
double euclid_dist_2_transpose(int numCoords,
                               int numObjs,
                               int numClusters,
                               double *objects,     // [numCoords][numObjs]
                               double *clusters,    // [numCoords][numClusters]
                               int objectId,
                               int clusterId) {
  int i;
  double ans = 0.0, diff;

  /* TODO: Calculate the euclid_dist of elem=objectId of objects from elem=clusterId from clusters, but for column-base format!!! */
  for(i = 0; i < numCoords; i++) {
    diff = objects[i*numObjs+ objectId] - clusters[i*numClusters + clusterId];
    ans += diff * diff;
  }

  return (ans);
}
