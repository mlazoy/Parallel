.KEEP_STATE:

MPICC = mpicc
CFLAGS = -Wall -Wextra -Wno-unused -O3
CONV=-DTEST_CONV

all: mpi_jacobi mpi_red_black mpi_gauss_seidel mpi_red_black_async mpi_red_black_overlapping

mpi_jacobi: mpi_jacobi.c utils.c
	$(MPICC) $(CFLAGS) $(RES) $(CONV) mpi_jacobi.c utils.c -o mpi_jacobi

mpi_red_black : mpi_red_black.c utils.c 
	$(MPICC) $(CFLAGS) $(RES) $(CONV) mpi_red_black.c utils.c -o mpi_red_black

mpi_gauss_seidel : mpi_gauss_seidel.c utils.c 
	$(MPICC) $(CFLAGS) $(RES) $(CONV) mpi_gauss_seidel.c utils.c -o mpi_gauss_seidel

mpi_red_black_async : mpi_red_black_async.c utils.c 
	$(MPICC) $(CFLAGS) $(RES) $(CONV) mpi_red_black_async.c utils.c -o mpi_red_black_async

mpi_red_black_overlapping : mpi_red_black_overlapping.c utils.c 
	$(MPICC) $(CFLAGS) $(RES) $(CONV) mpi_red_black_overlapping.c utils.c -o mpi_red_black_overlapping

clean:
	rm -rf *.o mpi_jacobi mpi_red_black mpi_gauss_seidel mpi_red_black_async mpi_red_black_overlapping