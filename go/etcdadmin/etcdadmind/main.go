package main

import (
    "fmt"
    "go.uber.org/zap"
    "etcdadmind/log"
    "etcdadmind/config"
)

const (
    gConfigFile = "etcdadmind.conf"
)

var (
    logger *zap.Logger
)

func main() {
    fmt.Printf("etcdadmind\n")

    var cfg config.KvConfig
    cfg.Init(gConfigFile)

    logCfg := log.Config{
        Level: cfg.Get("LOG_LEVEL"),
        File : cfg.Get("LOG_FILE"),
    }
    log.Init(logCfg)

    logger = log.GetLogger()

    logger.Debug("hello debug")
    logger.Info("hello info")
    logger.Warn("hello warn")
    logger.Error("hello error")
}

