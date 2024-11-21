#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <immintrin.h>  // For SSE2 intrinsics
#include <omp.h>

inline void FW(int **A, int K, int I, int J, int B);

int main(int argc, char **argv)
{
    int **A;
    int i, j, k;
    struct timeval t1, t2;
    double time;
    int B = 64;
    int N = 1024;

    if (argc != 3) {
        fprintf(stdout, "Usage %s N B\n", argv[0]);
        exit(0);
    }

    N = atoi(argv[1]);
    B = atoi(argv[2]);

    // Allocate memory for A with 32-byte alignment
    posix_memalign((void**)&A, 32, N * sizeof(int*));
    for (i = 0; i < N; ++i) {
        posix_memalign((void**)&A[i], 32, N * sizeof(int));
    }

    // Initialize the graph with random values
    graph_init_random(A, -1, N, 128 * N);

    // Start timer
    gettimeofday(&t1, 0);

    // Main loop of the Floyd-Warshall algorithm with tiling
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

    // Stop timer and calculate execution time
    gettimeofday(&t2, 0);
    time = (double)((t2.tv_sec - t1.tv_sec) * 1000000 + t2.tv_usec - t1.tv_usec) / 1000000;
    fprintf(stdout, "FW_TILED,%d,%d,%.4f\n", N, B, time);

    // Free the memory
    for (i = 0; i < N; i++) {
        _mm_free(A[i]);  // Free each row
    }
    _mm_free(A);  // Free the pointer array

    return 0;
}

inline void FW(int **A, int K, int I, int J, int B)
{
    int i, j, k;

    // Iterate over a block of tiles (3D loop over the block)
    for (k = K; k < K + B; k++) {
        for (i = I; i < I + B; i++) {
             __m128i A_i_k = _mm_load_si128((__m128i*)&A[i][k]); 

            for (j=J; j < J + B; j+=16){     
                // prefetch next iteration
                // _mm_prefetch((const char*)&A[i][j + 16], _MM_HINT_T0);
                // _mm_prefetch((const char*)&A[k][j + 16], _MM_HINT_T0); 
                  
                __m128i A_i_j = _mm_load_si128((__m128i*)&A[i][j]);      
                __m128i A_k_j = _mm_load_si128((__m128i*)&A[k][j]);      

                __m128i A_plus = _mm_add_epi32(A_i_k, A_k_j);                 
                __m128i result = _mm_min_epi32(A_i_j, A_plus);                

                _mm_store_si128((__m128i*)&A[i][j], result);

                // next chunk 
                A_i_j = _mm_load_si128((__m128i*)&A[i][j+4]);      
                A_k_j = _mm_load_si128((__m128i*)&A[k][j+4]);      

                A_plus = _mm_add_epi32(A_i_k, A_k_j);                 
                result = _mm_min_epi32(A_i_j, A_plus);                

                _mm_store_si128((__m128i*)&A[i][j+4], result);

                //next chunk
                A_i_j = _mm_load_si128((__m128i*)&A[i][j+8]);      
                A_k_j = _mm_load_si128((__m128i*)&A[k][j+8]);      

                A_plus = _mm_add_epi32(A_i_k, A_k_j);                 
                result = _mm_min_epi32(A_i_j, A_plus);                

                _mm_store_si128((__m128i*)&A[i][j+8], result);

                //next chunk
                A_i_j = _mm_load_si128((__m128i*)&A[i][j+12]);      
                A_k_j = _mm_load_si128((__m128i*)&A[k][j+12]);      

                A_plus = _mm_add_epi32(A_i_k, A_k_j);                 
                result = _mm_min_epi32(A_i_j, A_plus);                

                _mm_store_si128((__m128i*)&A[i][j+12], result);

            }
        }
        // if (k + 1 < K + B) {
        //     _mm_prefetch((const char*)&A[i][k + 1], _MM_HINT_T0);
        // }
    }
}
