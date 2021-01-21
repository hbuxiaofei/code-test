AS=as
LD=ld
OBJCOPY=objcopy
QEMU=/usr/libexec/qemu-kvm

LDFLAGS	+= -Ttext 0


all: bootimg


bootsect: bootsect.s
	$(AS) -n -g -o bootsect.o bootsect.s
	$(LD) $(LDFLAGS) -o bootsect bootsect.o
	cp -f bootsect bootsect.sym
	$(OBJCOPY) -R .pdr -R .comment -R .note -S -O binary bootsect


floppy: floppy.s
	$(AS) -n -g -o floppy.o floppy.s
	$(LD) -Ttext 0 -o floppy floppy.o
	cp -f floppy floppy.sym
	$(OBJCOPY) -R .pdr -R .comment -R .note -S -O binary floppy


bootimg: floppy bootsect
	dd if=bootsect of=bootimg bs=512 count=1
	dd if=floppy of=bootimg bs=512 count=4 seek=1
	echo "Build bootimg done"


start: bootimg
	$(QEMU) -m 16M -boot a -fda bootimg -vnc 0.0.0.0:1


clean:
	rm -f bootsect bootsect.o bootsect.sym floppy floppy.o floppy.sym bootimg

.PHONY=clean start all
