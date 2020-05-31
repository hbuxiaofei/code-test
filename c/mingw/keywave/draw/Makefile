CC:=x86_64-w64-mingw32-gcc
OBJ:=Draw.exe
LIBS:=-lgdi32
SRC:=$(wildcard *.c)


${OBJ}:
	${CC} ${SRC} -o $@ ${LIBS}

clean:
	rm -f ${OBJ}
