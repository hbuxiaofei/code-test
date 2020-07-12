package etcdctl

import (
	"fmt"
	"testing"
)

func TestGetEtcdResetMap(t *testing.T) {
	m := getEtcdResetMap()
	fmt.Printf("rest map: %v", m)
}
