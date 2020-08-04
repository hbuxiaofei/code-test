package main

import "fmt"

type FtpStore struct {
	Url    string
	User   string
	Passwd string
}

func NewFtpStore(url, user, passwd string) *FtpStore {
	fs := &FtpStore{
		Url:    url,
		User:   user,
		Passwd: passwd,
	}
	return fs
}

func (this *FtpStore) Get(id string) (string, error) {
	fmt.Printf("get ftpstore id: xx-xx-xx-xx\n")
	return "ftp store metadata", nil
}

func (this *FtpStore) Put(info string) (string, error) {
	fmt.Printf("put ftpstore ok\n")
	id := "xx-xx-xx-xx"
	return id, nil
}

func (this *FtpStore) List() ([]string, error) {
	ids := []string{"xx-xx-xx-xx", "oo-oo-oo-oo"}
	return ids, nil
}
