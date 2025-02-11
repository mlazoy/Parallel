    MPI_Datatype row_bound;
    MPI_Type_contiguous(local[1], MPI_DOUBLE, &row_bound); 
    MPI_Type_commit(&row_bound);

    MPI_Datatype col_bound;
    MPI_Type_vector(local[0], 1, local[1]+2, MPI_DOUBLE, &dummy);
    MPI_Type_create_resized(dummy, 0, sizeof(double), &col_bound);
    MPI_Type_commit(&col_bound);

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

        MPI_Status prev_status[6], curr_status[2]; 
        MPI_Request prev_reqs[6], curr_reqs[2];
        int prev = 0, curr = 0;

        int err;

		if (north != MPI_PROC_NULL) {
            err = MPI_Irecv(&(u_current[0][1]), 1, row_bound, north, MPI_ANY_TAG, MPI_COMM_WORLD, &prev_reqs[prev++]);
            err = MPI_Isend(&(u_previous[1][1]),1, row_bound, north, 0, MPI_COMM_WORLD, &prev_reqs[prev++]);
        }

        if (south != MPI_PROC_NULL) {
            err = MPI_Irecv(&(u_previous[local[0]+1][1]), 1, row_bound, south, MPI_ANY_TAG, MPI_COMM_WORLD, &prev_reqs[prev++]);
        }

        if (east != MPI_PROC_NULL) {
            err = MPI_Irecv(&(u_previous[1][local[1]+1]), 1, col_bound, east, MPI_ANY_TAG, MPI_COMM_WORLD, &prev_reqs[prev++]);
        }

        if (west != MPI_PROC_NULL) {
            err = MPI_Irecv(&(u_current[1][0]), 1, col_bound, west, MPI_ANY_TAG, MPI_COMM_WORLD, &prev_reqs[prev++]);
            err = MPI_Isend(&(u_previous[1][1]),1, col_bound, west, 1, MPI_COMM_WORLD, &prev_reqs[prev++]);
        }

        //only wait for recvs 
        MPI_Waitall(prev, prev_reqs, prev_status);

        // computation starts here
        gettimeofday(&tcs, NULL);
        // Gauss Seidel kernel 
        for (i=i_min;i<i_max;i++)
		    for (j=j_min;j<j_max;j++)
			    u_current[i][j]=u_previous[i][j]+(u_current[i-1][j]+u_previous[i+1][j]+u_current[i][j-1]+u_previous[i][j+1]-4*u_previous[i][j])*omega/4.0;
        // computation ends here
        gettimeofday(&tcf, NULL);
        tcomp += (tcf.tv_sec-tcs.tv_sec)+(tcf.tv_usec-tcs.tv_usec)*0.000001;

        // send rest values 
        if (south != MPI_PROC_NULL){
            err = MPI_Isend(&(u_current[local[0]][1]),1, row_bound, south, 2, MPI_COMM_WORLD, &curr_reqs[curr++]);
        }

        if (east != MPI_PROC_NULL) {
            err = MPI_Isend(&(u_current[1][local[1]]),1, col_bound, east, 3, MPI_COMM_WORLD, &curr_reqs[curr++]);
        }

        // now sends must be complete 
        MPI_Waitall(curr, curr_reqs, curr_status);

		#ifdef TEST_CONV
        if (t%C==0) {
			//*************TODO**************//
			/*Test convergence*/
            gettimeofday(&tcvs, NULL);
            converged = converge(u_previous, u_current, i_min, i_max, j_min, j_max);
            // min takes 0 if some proc has not converged locally 
            MPI_Allreduce(&converged, &global_converged, 1, MPI_INT, MPI_LAND, MPI_COMM_WORLD);
            gettimeofday(&tcvf, NULL);
            tconv += (tcvf.tv_sec-tcvs.tv_sec)+(tcvf.tv_usec-tcvs.tv_usec)*0.000001;
		}		
		#endif

        //barrier not needed, waitall is enough
        //MPI_Barrier(CART_COMM);


		//************************************//
 
         
        
    }