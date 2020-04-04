package main

import (
	"fmt"
)

func main() {
	fmt.Println("Hello World!")

	data, err := Asset("resources/conf.xml")
	if err == nil {
		fmt.Printf("conf:\n%v", string(data))
	} else {
		fmt.Println("Asert file err")
	}

	data, err = Asset("resources/init.xml")
	if err == nil {
		fmt.Printf("init:\n%v", string(data))
	} else {
		fmt.Println("Asert file err")
	}
}
