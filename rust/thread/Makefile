OBJ = a.out
SRC = ./mul_thread.rs


all: ${OBJ}

${OBJ}: ${SRC}
	rustc $^ -o $@

clean:
	rm -f ${OBJ}
