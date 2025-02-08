.KEEP_STATE:

MPICC = mpicc
CFLAGS = -Wall -Wextra -Wno-unused -O3
RES=-DPRINT_RESULTS
CONV=-DTEST_CONV

all: mpi_jacobi

mpi_jacobi: mpi_jacobi.c utils.c
	$(MPICC) $(CFLAGS) $(RES) $(CONV) mpi_jacobi.c utils.c -o mpi_jacobi

clean:
	rm -rf *.o mpi_jacobi 