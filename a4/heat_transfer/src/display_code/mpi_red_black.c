//----Computational core----//   
gettimeofday(&tts, NULL);
#ifdef TEST_CONV
for (t=0;t<T && !global_converged;t++) {
#endif
#ifndef TEST_CONV
#undef T
#define T 256
for (t=0;t<T;t++) {
#endif


     //*************TODO*******************//

    /*Add appropriate timers for computation*/
    
    /*Compute and Communicate*/

    swap=u_previous;
    u_previous=u_current;
    u_current=swap;

    MPI_Status status; 
    int err;
    // communication starts here 
    gettimeofday(&tms, NULL);

    if (north != MPI_PROC_NULL) {
        err = MPI_Sendrecv(&u_previous[1][1], 1, row_bound, north, 0, 
                     &u_previous[0][1], 1, row_bound, north, MPI_ANY_TAG,
                     MPI_COMM_WORLD, &status);
        if (err != MPI_SUCCESS) {
            printf("Process %d failed to communicate with North (rank %d)\n", rank, north);
            MPI_Abort(MPI_COMM_WORLD, err);
        }
    }

    if (south != MPI_PROC_NULL) {
        err = MPI_Sendrecv(&u_previous[local[0]][1], 1, row_bound, south, 1,
                    &u_previous[local[0]+1][1], 1, row_bound, south, MPI_ANY_TAG,
                    MPI_COMM_WORLD, &status);
        if (err != MPI_SUCCESS) {
            printf("Process %d failed to communicate with North (rank %d)\n", rank, south);
            MPI_Abort(MPI_COMM_WORLD, err);
        }
    }

    if (east != MPI_PROC_NULL) {
        err = MPI_Sendrecv(&u_previous[1][local[1]], 1, col_bound, east, 2,
                     &u_previous[1][local[1]+1], 1, col_bound, east, MPI_ANY_TAG,
                     MPI_COMM_WORLD, &status);
        if (err != MPI_SUCCESS) {
            printf("Process %d failed to communicate with North (rank %d)\n", rank, east);
            MPI_Abort(MPI_COMM_WORLD, err);
        }
    }

    if (west != MPI_PROC_NULL) {
        err = MPI_Sendrecv(&u_previous[1][1], 1, col_bound, west, 3,
                    &u_previous[1][0], 1, col_bound, west, MPI_ANY_TAG,
                    MPI_COMM_WORLD, &status);
        if (err != MPI_SUCCESS) {
            printf("Process %d failed to communicate with West (rank %d)\n", rank, west);
            MPI_Abort(MPI_COMM_WORLD, err);
        }
    }

    // communication ends here 
    MPI_Barrier(MPI_COMM_WORLD);
    gettimeofday(&tmf, NULL);

    // computation starts here
    gettimeofday(&tcs, NULL);
    // RED SOR
    // (i+j) is even
    for (i=i_min;i<i_max;i++) 
        for (j=j_min;j<j_max;j++) 
            if ((i+j)%2==0)
                u_current[i][j]=u_previous[i][j]+(omega/4.0)*(u_previous[i-1][j]+u_previous[i+1][j]+u_previous[i][j-1]+u_previous[i][j+1]-4*u_previous[i][j]);		         
    // computation ends here
    gettimeofday(&tcf, NULL);

    tcomm += (tmf.tv_sec-tms.tv_sec)+(tmf.tv_usec-tms.tv_usec)*0.000001;
    tcomp += (tcf.tv_sec-tcs.tv_sec)+(tcf.tv_usec-tcs.tv_usec)*0.000001;

    MPI_Barrier(MPI_COMM_WORLD);
    gettimeofday(&tms, NULL);

    if (north != MPI_PROC_NULL) {
        err = MPI_Sendrecv(&u_current[1][1], 1, row_bound, north, 0, 
                     &u_current[0][1], 1, row_bound, north, MPI_ANY_TAG,
                     MPI_COMM_WORLD, &status);
        if (err != MPI_SUCCESS) {
            printf("Process %d failed to communicate with North (rank %d)\n", rank, north);
            MPI_Abort(MPI_COMM_WORLD, err);
        }
    }

    if (south != MPI_PROC_NULL) {
        err = MPI_Sendrecv(&u_current[local[0]][1], 1, row_bound, south, 1,
                    &u_current[local[0]+1][1], 1, row_bound, south, MPI_ANY_TAG,
                    MPI_COMM_WORLD, &status);
        if (err != MPI_SUCCESS) {
            printf("Process %d failed to communicate with North (rank %d)\n", rank, south);
            MPI_Abort(MPI_COMM_WORLD, err);
        }
    }

    if (east != MPI_PROC_NULL) {
        err = MPI_Sendrecv(&u_current[1][local[1]], 1, col_bound, east, 2,
                     &u_current[1][local[1]+1], 1, col_bound, east, MPI_ANY_TAG,
                     MPI_COMM_WORLD, &status);
        if (err != MPI_SUCCESS) {
            printf("Process %d failed to communicate with North (rank %d)\n", rank, east);
            MPI_Abort(MPI_COMM_WORLD, err);
        }
    }

    if (west != MPI_PROC_NULL) {
        err = MPI_Sendrecv(&u_current[1][1], 1, col_bound, west, 3,
                    &u_current[1][0], 1, col_bound, west, MPI_ANY_TAG,
                    MPI_COMM_WORLD, &status);
        if (err != MPI_SUCCESS) {
            printf("Process %d failed to communicate with West (rank %d)\n", rank, west);
            MPI_Abort(MPI_COMM_WORLD, err);
        }
    }

    MPI_Barrier(MPI_COMM_WORLD);
    gettimeofday(&tmf, NULL);

    // computation starts here
    gettimeofday(&tcs, NULL);
    // BLACK SOR
    // (i+j) is odd
    for (i=i_min;i<i_max;i++)
        for (j=j_min;j<j_max;j++)
            if ((i+j) % 2 == 1)
                u_current[i][j]=u_previous[i][j]+(omega/4.0)*(u_current[i-1][j]+u_current[i+1][j]+u_current[i][j-1]+u_current[i][j+1]-4*u_previous[i][j]); 
     // computation ends here
    gettimeofday(&tcf, NULL);

    tcomm += (tmf.tv_sec-tms.tv_sec)+(tmf.tv_usec-tms.tv_usec)*0.000001;
    tcomp += (tcf.tv_sec-tcs.tv_sec)+(tcf.tv_usec-tcs.tv_usec)*0.000001;

    #ifdef TEST_CONV
    if (t%C==0) {
        //*************TODO**************//
        /*Test convergence*/
        gettimeofday(&tcvs, NULL);
        converged = converge(u_previous, u_current, i_min, i_max, j_min, j_max);
        MPI_Allreduce(&converged, &global_converged, 1, MPI_INT, MPI_LAND, MPI_COMM_WORLD);
        gettimeofday(&tcvf, NULL);
        tconv += (tcvf.tv_sec-tcvs.tv_sec)+(tcvf.tv_usec-tcvs.tv_usec)*0.000001;
    }		
    #endif


    //************************************//

     
    
}