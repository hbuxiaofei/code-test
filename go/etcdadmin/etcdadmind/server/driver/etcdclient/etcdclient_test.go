package etcdclient

import (
	"os"
	"testing"
	"fmt"
)

const (
	etcdIP   = "127.0.0.1"
	etcdPort = "2379"
)

var (
	client *EtcdClient
)

func setup() {
	client = New(etcdIP, etcdPort)
}

func teardown() {
	Release(client)
}

func TestEtcdlientMemberList(t *testing.T) {
	m := client.MemberList()
	for i := range m {
		fmt.Printf("name:%s ip:%s\n", i, m[i])
	}
}

// Test Entry
func TestMain(m *testing.M) {
	setup()
	ret := m.Run()
	teardown()
	os.Exit(ret)
}
