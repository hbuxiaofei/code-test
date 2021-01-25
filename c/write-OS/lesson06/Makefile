include Makefile.header

LDFLAGS	+= -Ttext 0 -e startup_32 -nostdlib

.PHONY=clean start all boot/head.o boot/bootsect boot/setup kernel/kernel.o

all: bootimg

OBJS = boot/head.o kernel/kernel.o mm/mm.o

system: $(OBJS)
	@$(LD) $(LDFLAGS) $(OBJS) -o system.sym
	@$(STRIP) system.sym -o system.o
	@$(OBJCOPY) -O binary -R .note -R .comment system.o system

kernel/kernel.o:
	@make -C kernel

boot/head.o:
	@make head.o -C boot

boot/bootsect:
	@make bootsect -C boot

boot/setup:
	@make setup -C boot

mm/mm.o:
	@make -C mm

# Squash the bootimg together
bootimg: boot/setup boot/bootsect system
	@dd if=boot/bootsect of=bootimg bs=512 count=1
	@dd if=boot/setup of=bootimg bs=512 count=4 seek=1
	@dd if=system of=bootimg bs=512 seek=5
	@echo "Build bootimg done"

start:
	$(QEMU) -m 16M -boot a -fda bootimg -vnc 0.0.0.0:1

clean:
	@rm -f bootsect *.o setup *.sym bootimg a.out binary head  system
	@make clean -C boot
	@make clean -C kernel
	@make clean -C mm
