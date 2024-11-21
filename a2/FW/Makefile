.phony: all clean

all: fw fw_sr fw_tiled fw_smd

CC=gcc-14
CFLAGS= -Wall -O3 -Wno-unused-variable 
SIMDFLAGS= -ftree-vectorize -march=native -fopt-info-vec
MSSEFLAGS= -march=native -mavx -msse4.2
OMPFLAGS= -fopenmp $(CFLAGS)

HDEPS+=%.h

OBJS=util.o

fw: $(OBJS) fw.c 
	$(CC) $(OBJS) fw.c -o fw $(CFLAGS)
fw_sr: fw_sr.c 
	$(CC) $(OBJS) fw_sr.c -o fw_sr $(OMPFLAGS)
fw_tiled: fw_tiled.c 
	$(CC) $(OBJS) fw_tiled.c -o fw_tiled $(OMPFLAGS) $(SIMDFLAGS)
fw_smd: fw_smd.c 
	$(CC) $(OBJS) fw_smd.c -o fw_smd $(OMPFLAGS) $(MSSEFLAGS)

%.o: %.c $(HDEPS)
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f *.o fw fw_sr fw_tiled 