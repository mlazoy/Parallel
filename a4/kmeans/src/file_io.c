#include <stdio.h>
#include <stdlib.h>
#include <string.h>     /* strtok() */
#include <sys/types.h>  /* open() */
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>     /* read(), close() */
#include <mpi.h>

#include "kmeans.h"

double * dataset_generation(int numObjs, int numCoords, long *rank_numObjs)
{
    double * objects = NULL, * rank_objects = NULL;
    long i, j, k;

    // Random values that will be generated will be between 0 and 10.
    double val_range = 10;

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    /*
     * TODO: Calculate number of objects that each rank will examine (*rank_numObjs)
     */
    if (numObjs % size == 0) *rank_numObjs = numObjs / size; // equally distributed
    else {
        if (rank == size-1)
             *rank_numObjs = numObjs % (size-1);
        else 
            *rank_numObjs = numObjs / (size-1);
    }

    /* allocate space for objects[][] and read all objects */
    int sendcounts[size], displs[size];
    if (rank == 0) {
        objects = (typeof(objects)) malloc(numObjs * numCoords * sizeof(*objects));
        /*
         * TODO: Calculate sendcounts and displs, which will be used to scatter data to each rank.
         * Hint: sendcounts: number of elements sent to each rank
         *       displs: displacement of each rank's data
         */

        int disp_sum = 0;
        for (i = 0; i < size-1; i++){
            sendcounts[i] = (*rank_numObjs) * numCoords;
            displs[i] = disp_sum;
            disp_sum += sendcounts[i];
        } 
        sendcounts[size-1] = (numObjs - (size-1)*(*rank_numObjs)) * numCoords;
        displs[size-1] = disp_sum;
    }

    /* 
     * TODO: Broadcast the sendcounts and displs arrays to other ranks
     */
    MPI_Bcast(sendcounts, size, MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Bcast(displs, size, MPI_INT, 0, MPI_COMM_WORLD);


    /* allocate space for objects[][] (for each rank separately) and read all objects */
    rank_objects = (typeof(rank_objects)) malloc((*rank_numObjs) * numCoords * sizeof(*rank_objects));
    
    /* rank 0 will generate data for the objects array. This array will be used later to scatter data to each rank. */
    if (rank == 0) {
        for (i=0; i<numObjs; i++)
        {
            unsigned int seed = i;
            for (j=0; j<numCoords; j++)
            {
                objects[i*numCoords + j] = (rand_r(&seed) / ((double) RAND_MAX)) * val_range;
                if (_debug && i == 0)
                    printf("object[i=%ld][j=%ld]=%f\n",i,j,objects[i*numCoords + j]);
            }
        }
    }

    /*
     * TODO: Scatter objects to every rank. (hint: each rank may receive different number of objects)
     */
    MPI_Scatterv(objects, sendcounts, displs, MPI_DOUBLE, rank_objects, sendcounts[rank], MPI_DOUBLE, 0, MPI_COMM_WORLD);


    if (rank == 0)
        free(objects);

    return rank_objects;
}
