package main

import (
	"fmt"

	"file/util"
)

func main() {
	a := 5
	b := 4
	sum := util.GoSum(4, 5)
	fmt.Printf("%d plus %d is: %d\n", a, b, sum)
}
