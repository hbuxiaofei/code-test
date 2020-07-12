package main

import (
	"etcdadmind/config"
	"etcdadmind/log"
	"etcdadmind/server"
	"go.uber.org/zap"
)

var (
	logger *zap.Logger
)

func main() {
	cfg := config.Init()

	log.Init(log.Config{
		Level: cfg.Get("LOG_LEVEL"),
		File:  cfg.Get("LOG_FILE"),
	})

	logger = log.GetLogger()

	logger.Debug("hello debug")
	logger.Info("hello info")
	logger.Warn("hello warn")
	logger.Error("hello error")

	server.Init(cfg.Get("GRPC_PORT"))
}
