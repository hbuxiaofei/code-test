all:build run

build:
	cargo build

run:
	cargo run

test:
	cargo test

test-all:
	make -C restaurant test
	cargo test

clean:
	find ./ -name target -type d | xargs rm -rf
