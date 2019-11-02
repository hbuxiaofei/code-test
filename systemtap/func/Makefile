SRC_DIR := .
Q := @

SOURCE := $(wildcard ${SRC_DIR}/*.c)
OBJECT := $(patsubst %.c,%.o,$(SOURCE))

TARGET := a.out

CC := gcc
LD := gcc
CFLAGS := -g -Wall -I${SRC_DIR}
LDFLAGS := -lncurses

${TARGET}: ${OBJECT}
	$(Q)echo "+ LD $^ -> $@"
	$(Q)$(LD) $(LDFLAGS) -o $@ $^

${SRC_DIR}/%.o: ${SRC_DIR}/%.c
	$(Q)echo "+ CC $^ -> $@"
	$(Q)$(CC) $(CFLAGS) -o $@ -c $^

.PHONY:clean
clean:
	$(Q)rm -f $(TARGET)
	$(Q)rm -f $(OBJECT)
