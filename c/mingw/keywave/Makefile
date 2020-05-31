CC:=x86_64-w64-mingw32-gcc
OBJ:=KeyWave.exe
LIBS:=-lgdi32
SRC:=$(wildcard *.c)
OUT:=keywave-installer.exe


all:${OBJ}
	make -C draw
	/bin/bash build.sh

${OBJ}:${SRC}
	${CC} ${SRC} -o $@ ${LIBS}

clean:
	make -C draw clean
	rm -f ${OUT}
	rm -f ${OBJ}

.PHONY:
	${OUT}
