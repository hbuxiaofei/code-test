package main

import "fmt"

type Phone interface {
	call()
}

type NokiaPhone struct {
}

func (nokiaPhone NokiaPhone) call() {
	fmt.Println("I am Nokia, I can call you!")
}

type ApplePhone struct {
}

func (iPhone ApplePhone) call() {
	fmt.Println("I am Apple Phone, I can call you!")
}

func main() {
	var phone Phone
	phone = new(NokiaPhone)
	phone.call()

	phone = new(ApplePhone)
	phone.call()

	var s StoreInterface
	fmt.Printf("\n\n")
	s = NewLocalStore("/tmp/localstore")
	id, _ := s.Put("localstore metadata")
	metadata, _ := s.Get(id)
	fmt.Printf("localstore: %s\n", metadata)

	fmt.Printf("\n")
	s = NewFtpStore("127.0.0.1:/ftpserver", "root", "root")
	id, _ = s.Put("ftp metadata")
	metadata, _ = s.Get(id)
	fmt.Printf("ftpstore: %s\n", metadata)
}
