# Rust 自定义数据类型主要是通过下面这两个关键字来创建：
#
# - struct： 定义一个结构体
# - enum： 定义一个枚举类型
#
# 而常量的创建可以通过 const 和 static 关键字来创建。


NAME=scope_freeze

all: build test clean

build: ${NAME}.rs
	rustc $^

test:
	./${NAME}

clean:
	@rm -f ${NAME}
