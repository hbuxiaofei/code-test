NAME = xelatex
OBJ = ${NAME}.pdf
SRC = ${NAME}.tex

all: ${OBJ}

${OBJ}: ${SRC}
	xelatex $^
	xelatex $^

clean:
	rm -f ${NAME}.aux ${NAME}.log ${NAME}.toc ${NAME}.out ${NAME}.dvi

clean-all: clean
	rm -f ${OBJ}

