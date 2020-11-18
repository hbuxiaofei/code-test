KERNEL_VER=$(shell uname -r)

obj-m += qemu_edu.o

default:
	make -C /lib/modules/$(KERNEL_VER)/build M=$(CURDIR) modules

clean:
	rm -rf modules.order Module.symvers *.mod.c *.o .qemu* .tmp*

dist-clean: clean
	rm -f *.ko
