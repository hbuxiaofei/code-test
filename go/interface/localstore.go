package main

import "fmt"

type LocalStore struct {
	Url string
}

func NewLocalStore(url string) *LocalStore {
	s := &LocalStore{
		Url: url,
	}
	return s
}

func (this *LocalStore) Get(id string) (string, error) {
	fmt.Printf("get localstore id: xx-xx-xx-xx\n")
	return "local store metadata", nil
}

func (this *LocalStore) Put(info string) (string, error) {
	fmt.Printf("put localstore ok\n")
	id := "xx-xx-xx-xx"
	return id, nil
}

func (this *LocalStore) List() ([]string, error) {
	ids := []string{"xx-xx-xx-xx", "oo-oo-oo-oo"}
	return ids, nil
}
