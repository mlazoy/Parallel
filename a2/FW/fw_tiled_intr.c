/*
 * Tiled version of the Floyd-Warshall algorithm.
 * command-line arguments: N, B
 * N = size of graph
 * B = size of tile
 * works only when N is a multiple of B
 */
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include "util.h"
#include <omp.h>
#include <immintrin.h>  // For AVX2 intrinsics

inline void FW(int **A, int K, int I, int J, int N);


int main(int argc, char **argv)
{
	int **A;
	int i,j,k;
	struct timeval t1, t2;
	double time;
	int B=64;
	int N=1024;

	if (argc != 3){
		fprintf(stdout, "Usage %s N B\n", argv[0]);
		exit(0);
	}

	N=atoi(argv[1]);
	B=atoi(argv[2]);


    posix_memalign((void**)&A, 32, N * sizeof(int *));  // Align the array of row pointers
    for (i = 0; i < N; i++) {
        posix_memalign((void**)&A[i], 32, N * sizeof(int));  // Align each row
    }


	graph_init_random(A,-1,N,128*N);

	gettimeofday(&t1,0);

        for (k = 0; k < N; k += B) {
            #pragma omp parallel
			{
			#pragma omp single
			{
            FW(A, k, k, k, B);
			}
            #pragma omp for nowait
            for (i = 0; i < k; i += B)
                FW(A, k, i, k, B);

            #pragma omp for nowait
            for (i = k + B; i < N; i += B)
                FW(A, k, i, k, B);

            #pragma omp for nowait
            for (j = 0; j < k; j += B)
                FW(A, k, k, j, B);

            #pragma omp for nowait
            for (j = k + B; j < N; j += B)
                FW(A, k, k, j, B);
        
			#pragma omp barrier
         	
            #pragma omp for collapse(2) nowait
            for (i = 0; i < k; i += B)
                for (j = 0; j < k; j += B)
                    FW(A, k, i, j, B);

            #pragma omp for collapse(2) nowait
            for (i = 0; i < k; i += B)
                for (j = k + B; j < N; j += B)
                    FW(A, k, i, j, B);

            #pragma omp for collapse(2) nowait
            for (i = k + B; i < N; i += B)
                for (j = 0; j < k; j += B)
                    FW(A, k, i, j, B);

            #pragma omp for collapse(2) nowait
            for (i = k + B; i < N; i += B)
                for (j = k + B; j < N; j += B)
                    FW(A, k, i, j, B);

			#pragma omp barrier

        }
    }


	gettimeofday(&t2,0);

	time=(double)((t2.tv_sec-t1.tv_sec)*1000000+t2.tv_usec-t1.tv_usec)/1000000;
	fprintf(stderr,"FW_TILED,%d,%d,%.4f\n", N,B,time);

	
	for(i=0; i<N; i++)
		for(j=0; j<N; j++) fprintf(stdout,"%d\n", A[i][j]);
        
	
	
	// Free memory
    for (i = 0; i < N; i++) {
        free(A[i]);
    }
    free(A);

	return 0;
}

inline void FW(int **A, int K, int I, int J, int N)
{
    int k, i, j;  // Declare all loop variables
    
    for (k = K; k < K + N; k++) {
        for (i = I; i < I + N; i++) {
            // Load 8 integers from A and B into AVX registers
            __m256i A_i_j = _mm256_load_si256((__m256i*)&A[i][J]);

            __m256i A_i_k = _mm256_load_si256((__m256i*)&A[i][k]);
            __m256i A_k_j = _mm256_load_si256((__m256i*)&A[k][J]);
            __m256i A_plus = _mm256_add_epi32(A_i_k, A_k_j);

            // Minimum of A and B element-wise
            __m256i result = _mm256_min_epi32(A_i_j, A_plus);
            // store
            _mm256_store_si256((__m256i*)&A[i][J], result);

            __m256i A_i_j = _mm256_load_si256((__m256i*)&A[i][J+8]);
            __m256i A_i_k = _mm256_load_si256((__m256i*)&A[i][k]);
            __m256i A_k_j = _mm256_load_si256((__m256i*)&A[k][J+8]);
            __m256i A_plus = _mm256_add_epi32(A_i_k, A_k_j);
            // Minimum of A and B element-wise
            __m256i result = _mm256_min_epi32(A_i_j, A_plus);
            // store
            _mm256_store_si256((__m256i*)&A[i][J+8], result);

            __m256i A_i_j = _mm256_load_si256((__m256i*)&A[i][J+16]);
            __m256i A_i_k = _mm256_load_si256((__m256i*)&A[i][k]);
            __m256i A_k_j = _mm256_load_si256((__m256i*)&A[k][J+16]);
            __m256i A_plus = _mm256_add_epi32(A_i_k, A_k_j);
            // Minimum of A and B element-wise
            __m256i result = _mm256_min_epi32(A_i_j, A_plus);
            // store
            _mm256_store_si256((__m256i*)&A[i][J+16], result);

            __m256i A_i_j = _mm256_load_si256((__m256i*)&A[i][J+24]);
            __m256i A_i_k = _mm256_load_si256((__m256i*)&A[i][k]);
            __m256i A_k_j = _mm256_load_si256((__m256i*)&A[k][J+24]);
            __m256i A_plus = _mm256_add_epi32(A_i_k, A_k_j);
            // Minimum of A and B element-wise
            __m256i result = _mm256_min_epi32(A_i_j, A_plus);
            // store
            _mm256_store_si256((__m256i*)&A[i][J+24], result);
	    }
    }
}   
