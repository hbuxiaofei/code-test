# cargo +nightly install cargo-expand

all:
	cargo run
	cargo expand > expand.rs

clean:
	rm -f expand.rs

dist-clean: clean
	rm -rf target Cargo.lock
