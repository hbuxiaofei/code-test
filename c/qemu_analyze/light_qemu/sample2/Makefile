OBJ = kvmsample bootimg

all: $(OBJ)

kvmsample: main.o
	gcc main.c -o kvmsample -lpthread

bootimg: boot.o
	ld -m elf_i386 --oformat binary -N -e _start -Ttext 0x10000 -o bootimg boot.o

boot.o: boot.s
	as -32 boot.s -o boot.o

clean:
	- @rm -f *.o $(OBJ)
