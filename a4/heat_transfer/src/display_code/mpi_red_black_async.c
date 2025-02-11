    MPI_Datatype RedBlack_row;
    MPI_Type_vector(local[1]/2, 1, 2, MPI_DOUBLE, &dummy);
    MPI_Type_create_resized(dummy, 0, sizeof(double), &RedBlack_row);
    MPI_Type_commit(&RedBlack_row);

    MPI_Datatype RedBlack_col;
    MPI_Type_vector(local[0]/2, 1, 2*(local[1]+2), MPI_DOUBLE, &dummy);
    MPI_Type_create_resized(dummy, 0, sizeof(double), &RedBlack_col);
    MPI_Type_commit(&RedBlack_col);

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

        MPI_Status red_status[8], black_status[8];
        MPI_Request red_reqs[8], black_reqs[8]; 
        int red_cnt = 0, black_cnt = 0;
        int err;

		if (north != MPI_PROC_NULL) {
            MPI_Irecv(&(u_previous[0][1]), 1, RedBlack_row, north, MPI_ANY_TAG, MPI_COMM_WORLD, &red_reqs[red_cnt++]);
            MPI_Isend(&(u_previous[1][2]), 1, RedBlack_row, north, 0, MPI_COMM_WORLD, &red_reqs[red_cnt++]);
        }

        if (south != MPI_PROC_NULL) {
            MPI_Irecv(&(u_previous[local[0]+1][2]), 1, RedBlack_row, south, MPI_ANY_TAG, MPI_COMM_WORLD, &red_reqs[red_cnt++]);
            MPI_Isend(&(u_previous[local[0]][1]), 1, RedBlack_row, south, 1, MPI_COMM_WORLD, &red_reqs[red_cnt++]);
        }

        if (east != MPI_PROC_NULL) {
            MPI_Irecv(&(u_previous[2][local[1]+1]), 1, RedBlack_col, east, MPI_ANY_TAG, MPI_COMM_WORLD, &red_reqs[red_cnt++]);
            MPI_Isend(&(u_previous[1][local[1]]), 1, RedBlack_col, east, 2, MPI_COMM_WORLD, &red_reqs[red_cnt++]);
        }

        if (west != MPI_PROC_NULL) {
            MPI_Irecv(&(u_previous[1][0]), 1, RedBlack_col, west, MPI_ANY_TAG, MPI_COMM_WORLD, &red_reqs[red_cnt++]);
            MPI_Isend(&(u_previous[2][1]), 1, RedBlack_col, west, 3, MPI_COMM_WORLD, &red_reqs[red_cnt++]);
        }

        MPI_Waitall(red_cnt, red_reqs, red_status);

        // computation starts here
        gettimeofday(&tcs, NULL);
        // RED SOR
        // (i+j) is even
        for (i=i_min; i<i_max; i++) {
            if (i & 1) j = (j_min&1) ? j_min : j_min+1;
            else j = (j_min&1) ? j_min+1 : j_min;
            for (j; j<j_max; j+=2)
                u_current[i][j]=u_previous[i][j]+(omega/4.0)*(u_previous[i-1][j]+u_previous[i+1][j]+u_previous[i][j-1]+u_previous[i][j+1]-4*u_previous[i][j]);  
        }  
        // computation ends here
        gettimeofday(&tcf, NULL);

        tcomp += (tcf.tv_sec-tcs.tv_sec)+(tcf.tv_usec-tcs.tv_usec)*0.000001;

        //MPI_Barrier(MPI_COMM_WORLD);

        if (north != MPI_PROC_NULL) {
            MPI_Irecv(&(u_current[0][2]), 1, RedBlack_row, north, MPI_ANY_TAG, MPI_COMM_WORLD, &black_reqs[black_cnt++]);
            MPI_Isend(&(u_current[1][1]), 1, RedBlack_row, north, 0, MPI_COMM_WORLD, &black_reqs[black_cnt++]);
        }

        if (south != MPI_PROC_NULL) {
            MPI_Irecv(&(u_current[local[0]+1][1]), 1, RedBlack_row, south, MPI_ANY_TAG, MPI_COMM_WORLD, &black_reqs[black_cnt++]);
            MPI_Isend(&(u_current[local[0]][2]), 1, RedBlack_row, south, 1, MPI_COMM_WORLD, &black_reqs[black_cnt++]);
        }

        if (east != MPI_PROC_NULL) {
            MPI_Irecv(&(u_current[1][local[1]+1]), 1, RedBlack_col, east, MPI_ANY_TAG, MPI_COMM_WORLD, &black_reqs[black_cnt++]);
            MPI_Isend(&(u_current[2][local[1]]), 1, RedBlack_col, east, 2, MPI_COMM_WORLD, &black_reqs[black_cnt++]);
        }

        if (west != MPI_PROC_NULL) {
            MPI_Irecv(&(u_current[2][0]), 1, RedBlack_col, west, MPI_ANY_TAG, MPI_COMM_WORLD, &black_reqs[black_cnt++]);
            MPI_Isend(&(u_current[1][1]), 1, RedBlack_col, west, 3, MPI_COMM_WORLD, &black_reqs[black_cnt++]);
        }

        MPI_Waitall(black_cnt, black_reqs, black_status);

        // computation starts here
        gettimeofday(&tcs, NULL);
        // BLACK SOR
        // (i+j) is odd
        for (i=i_min; i<i_max; i++) {
            if (i & 1) j = (j_min & 1) ? j_min+1 : j_min;
            else j = (j_min & 1) ? j_min : j_min+1;
		    for (j; j<j_max; j+=2)
				u_current[i][j]=u_previous[i][j]+(omega/4.0)*(u_current[i-1][j]+u_current[i+1][j]+u_current[i][j-1]+u_current[i][j+1]-4*u_previous[i][j]); 
        }
        // computation ends here
        gettimeofday(&tcf, NULL);

        tcomp += (tcf.tv_sec-tcs.tv_sec)+(tcf.tv_usec-tcs.tv_usec)*0.000001;

        //MPI_Barrier(MPI_COMM_WORLD);

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