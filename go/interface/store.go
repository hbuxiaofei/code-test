package main

type StoreInterface interface {
	Get(id string) (string, error)
	Put(info string) (string, error)
	List() ([]string, error)
}
