NAME=formatting

all: build test clean

build: ${NAME}.rs
	rustc $^

test:
	./${NAME}

clean:
	@rm -f ${NAME}
