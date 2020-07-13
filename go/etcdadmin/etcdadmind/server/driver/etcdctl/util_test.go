package etcdctl

import (
	"fmt"
	"testing"
)

func TestGetEtcdResetMap(t *testing.T) {
	m, _ := getEtcdResetMap()
	m["ETCD_INITIAL_CLUSTER"] = "mofied"
	m["ADD_KEY"] = "add value"
	delete(m, "ETCD_DATA_DIR")
	fmt.Printf("rest map: %v\n", m)

	resetEtcdConfig()
}

func TestEtcdResetWithStart(t *testing.T) {
	t.Skip("skipping: do not reset etcd")
	err := ResetEtcd(true)
	fmt.Printf("ret : %v\n", err)
}
