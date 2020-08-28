package main

import (
	"fmt"
	"unsafe"
)

type TypeStruct1 struct {
	val int
	str string
}

type MyType TypeStruct1

func main() {
	valtest := TypeStruct1{
		val: 100,
		str: "hello",
	}

	var mytest *MyType

	mytest = (*MyType)(unsafe.Pointer(&valtest))

	fmt.Printf("hello world: %v\n", mytest)
}
