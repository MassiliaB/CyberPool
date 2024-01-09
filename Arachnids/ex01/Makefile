CC = gcc
CFLAGS = -Wall -Wextra -g
LDFLAGS = -lcurl
SRC = spider.c request.c download.c

OBJ = $(SRC:.c=.o)

spider: $(OBJ)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f spider $(OBJ)
	rm -f data/*