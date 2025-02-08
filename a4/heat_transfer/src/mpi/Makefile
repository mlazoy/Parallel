.KEEP_STATE:

MPICC = mpicc

CFLAGS = -Wall -Wextra -Wno-unused -O3

all: mpi_jacobi
#mpi_GaussSeidelSOR mpi_RedBlackSOR

jacobi.o: jacobi.c
	$(MPICC) $(CFLAGS) -c $< -o $@

utils.o: utils.c
	$(MPICC) $(CFLAGS) -c $< -o $@

mpi_jacobi: jacobi.o utils.o
	$(MPICC) $(CFLAGS) $^ -o $@ 

clean:
	rm -rf *.o mpi_jacobi 
#mpi_GaussSeidelSOR mpi_RedBlackSOR