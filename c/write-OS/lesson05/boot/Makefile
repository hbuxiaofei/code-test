include ../Makefile.header

LDFLAGS	+= -Ttext 0

.PHONY=clean run all

all: bootsect setup head.o

bootsect: bootsect.s
	@$(AS) -n -g -o bootsect.o bootsect.s
	@$(LD) $(LDFLAGS) -o bootsect bootsect.o
	@cp -f bootsect bootsect.sym
	@$(OBJCOPY) -R .pdr -R .comment -R.note -S -O binary bootsect

setup: setup.s
	@$(AS) -n -g -o setup.o setup.s
	@$(LD) $(LDFLAGS) -o setup setup.o
	@cp -f setup setup.sym
	@$(OBJCOPY) -R .pdr -R .comment -R.note -S -O binary setup

head.o: head.s
	@$(AS) -n -g -o head.o head.s

clean:
	@rm -f *.o *.sym bootsect setup
