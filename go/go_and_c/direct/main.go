package main

/*
// C 标志io头文件，你也可以使用里面提供的函数
#include <stdio.h>
int add(int a, int b){
    return a+b;
}
*/
import "C" // 切勿换行再写这个

import "fmt"

func main() {
	var a _Ctype_int = 4
	var b _Ctype_int = 2
	fmt.Printf("%d + %d = %d\n", a, b, C.add(a, b))
}
