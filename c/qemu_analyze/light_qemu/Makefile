OBJ = bootimg light-qemu

all: $(OBJ)

light-qemu: light-qemu.c
	gcc light-qemu.c -o light-qemu


bootimg: boot.s
	as -32 boot.s -o boot.o
	objcopy -O binary boot.o bootimg

clean:
	rm -f *.o

dist-clean: clean
	rm -f $(OBJ)

