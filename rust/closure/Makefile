OBJ = a.out
SRC = ./closure.rs

all: ${OBJ}

${OBJ}: ${SRC}
	rustc $^ -o $@

clean:
	rm -f ${OBJ}
