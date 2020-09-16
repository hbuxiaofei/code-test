build:
	cargo build
	cargo bootimage

xbuild:
	rustup default nightly
	cargo xbuild || true

all: xbuild build

clean:
	rm -f Cargo.lock
	rm -rf target
