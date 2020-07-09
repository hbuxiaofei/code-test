package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strings"
	"sync"
)

// config file with key=value
type KvConfig struct {
	FilePath string
	KvMap    map[string]string
	rwMutex  *sync.RWMutex
}

func (kv *KvConfig) Init(path string) error {
	kv.FilePath = path
	kv.rwMutex = new(sync.RWMutex)
	config := make(map[string]string)

	f, err := os.Open(path)
	defer f.Close()
	if err != nil {
		return err
	}

	r := bufio.NewReader(f)
	for {
		b, _, err := r.ReadLine()
		if err != nil {
			if err == io.EOF {
				break
			}
			return err
		}
		s := strings.TrimSpace(string(b))
		index := strings.Index(s, "=")
		if index < 0 || s[0] == '#' {
			continue
		}
		key := strings.TrimSpace(s[:index])
		if len(key) == 0 {
			continue
		}
		value := strings.TrimSpace(s[index+1:])
		if len(value) == 0 {
			continue
		}
		config[key] = value
	}
	kv.KvMap = config
	return nil
}

func (kv *KvConfig) Get(key string) string {
	kv.rwMutex.RLock()
	value := kv.KvMap[key]
	kv.rwMutex.RUnlock()
	return value
}

func (kv *KvConfig) Set(key string, value string) error {
	kv.rwMutex.Lock()
	kv.KvMap[key] = value
	kv.rwMutex.Unlock()
	return nil
}

func main() {
	var kv KvConfig
	kv.Init("test.conf")

	ip := kv.Get("ip")
	port := kv.Get("port")

	fmt.Println("ip =", string(ip), "port =", string(port))
}
