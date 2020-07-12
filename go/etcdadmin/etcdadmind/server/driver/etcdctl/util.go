package etcdctl

import (
	"etcdadmind/config"
	"fmt"
	"net"
	"os"
	"path/filepath"
	"sync"
)

var (
	mutexEtcdConfig sync.Mutex
)

func writeEtcdConfig(path string, m map[string]string) error {
	var err error

	dirname := filepath.Dir(path)

	mutexEtcdConfig.Lock()

	_, err = os.Stat(path)
	if err != nil {
		os.MkdirAll(dirname, os.ModePerm)
	}

	f, err := os.OpenFile(path, os.O_CREATE|os.O_TRUNC|os.O_WRONLY, 0666)
	defer f.Close()
	if err != nil {
		goto exit
	}
	for k := range m {
		f.WriteString(fmt.Sprintf("%s=\"%s\"\n", k, m[k]))
	}

exit:
	mutexEtcdConfig.Unlock()

	return err
}
func getEtcdResetMap() map[string]string {

	cfgServer := config.Init()

	lisP := fmt.Sprintf("http://0.0.0.0:%s", cfgServer.Get("ETCD_PEER_PORT"))
	lisC := fmt.Sprintf("http://0.0.0.0:%s", cfgServer.Get("ETCD_CLIENT_PORT"))
	name, err := os.Hostname()
	if err != nil {
		return map[string]string{}
	}
	addrs, err := net.LookupHost(name)
	if err != nil {
		return map[string]string{}
	}
	advP := fmt.Sprintf("http://%s:%s", addrs[0],
		cfgServer.Get("ETCD_PEER_PORT"))

	advC := fmt.Sprintf("http://%s:%s", addrs[0],
		cfgServer.Get("ETCD_CLIENT_PORT"))

	initCluster := fmt.Sprintf("%s=http://%s:%s", name, addrs[0],
		cfgServer.Get("ETCD_PEER_PORT"))

	m := map[string]string{
		"ETCD_DATA_DIR":                    "/var/lib/etcd/default.etcd",
		"ETCD_LISTEN_PEER_URLS":            lisP,
		"ETCD_LISTEN_CLIENT_URLS":          lisC,
		"ETCD_NAME":                        name,
		"ETCD_INITIAL_ADVERTISE_PEER_URLS": advP,
		"ETCD_ADVERTISE_CLIENT_URLS":       advC,
		"ETCD_INITIAL_CLUSTER":             initCluster,
		"ETCD_INITIAL_CLUSTER_STATE":       "new",
		"ETCD_INITIAL_CLUSTER_TOKEN":       "etcd-cluster",
	}

	return m
}

func ResetEtcdConfig() error {
	cfgServer := config.Init()

	cfgEtcdFile := cfgServer.Get("ETCD_CONF_FILE")

	m := getEtcdResetMap()

	return writeEtcdConfig(cfgEtcdFile, m)
}
