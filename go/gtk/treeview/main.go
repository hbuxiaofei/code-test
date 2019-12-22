package main

import (
	"fmt"
	"os"

	"github.com/gotk3/gotk3/gtk"

	"virtualware/start"
)

func main() {
	fmt.Println("start main ...")

	gtk.Init(&os.Args)

	start.Entry()

	gtk.Main()
}
