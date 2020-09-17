build:
	cargo build
	cargo bootimage

xbuild:
	rustup default nightly
	cargo xbuild --target x86_64-rinux.json || true

qemu-run:
	/usr/libexec/qemu-kvm -drive format=raw,file=target/x86_64-rinux/debug/bootimage-rinux.bin \
		-vnc 0.0.0.0:1 -m 32m -smp 1 \
		-device isa-debug-exit,iobase=0xf4,iosize=0x04
		-serial stdio

all: xbuild build

clean:
	rm -f Cargo.lock
	rm -rf target
