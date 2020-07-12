package config

import (
	"sync"
)

const (
	configFile = "/etc/etcdadmin/etcdadmind.conf"
)

var (
	once sync.Once
	cfg  *KvConfig
)

func Init() *KvConfig {
	once.Do(func() {
		cfg = Load(configFile)
	})
	return cfg
}
