package main

import (
	"fmt"

	"study/dir1"
	"study/dir2"
)

// PrintLongString function
func PrintLongString() {
	fmt.Println("This is a long string, This is a long string,",
		"This is a long string, This is a long string,",
		"This is a long string, This is a long string.")
}

func main() {
	fmt.Println("Hello World!")

	PrintLongString()

	dir1.TarPrint1()
	dir1.TarPrint2()

	dir2.RpmPrint1()
}
