all: bootsect


bootsect.o: bootsect.s
	as -o bootsect.o bootsect.s


# ld:
#   -e ADDRESS, --entry ADDRESS   Set start address
#   --oformat TARGET              Specify target of output file
#
# objcopy:
# 	-R --remove-section <name>    Remove section <name> from the output
bootsect: bootsect.o
	# ld --oformat binary -e _start -Ttext 0x7c00 -o bootsect bootsect.o
	ld -Ttext 0 -o bootsect bootsect.o
	cp -f bootsect bootsect.sym
	objcopy -R .pdr -R .comment -R .note -S -O binary bootsect


start: bootsect
	/usr/libexec/qemu-kvm -m 16M -boot a -fda bootsect -vnc 0.0.0.0:1


clean:
	rm bootsect.o bootsect bootsect.sym

.PHONY=clean start all
