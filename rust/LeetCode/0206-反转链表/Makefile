OBJ = a.out
SRC = ./main.rs

all: ${OBJ}

${OBJ}: ${SRC}
	rustc $^ -o $@

clean:
	rm -f ${OBJ}
