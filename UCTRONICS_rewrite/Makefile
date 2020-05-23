NAME=motordriver
CC=gcc
CFLAGS=-Wall -pthread 
LIBS=-lwiringPi -lrt
ODIR=obj
SDIR=src
DEPS=motordriver.h
%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

$(NAME): $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS) $(LIBS)

.PHONY:	run

.PHONY:	clean

clean:	
	rm -f $(NAME) $(ODIR)/*.o


