  /* TODO: Transpose dims */
  double **dimObjects = (double**) calloc_2d(numCoords, numObjs, sizeof(double)); //calloc_2d(...) -> [numCoords][numObjs]
  double **dimClusters = (double**) calloc_2d(numCoords, numClusters, sizeof(double));  //calloc_2d(...) -> [numCoords][numClusters]
  double **newClusters = (double**) calloc_2d(numCoords, numClusters, sizeof(double));  //calloc_2d(...) -> [numCoords][numClusters]

  double *deviceObjects;
  double *deviceClusters;
  int *deviceMembership;

  printf("\n|-----------Transpose GPU Kmeans------------|\n\n");

  
  //  TODO: Copy objects given in [numObjs][numCoords] layout to new
  //  [numCoords][numObjs] layout
  for (i = 0; i < numObjs; i++) {
    for (j = 0; j < numCoords; j++) {
      dimObjects[j][i] = objects[i*numCoords+ j];
    }
  }

